# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 17:19:01 2025

@author: vigno
"""

import numpy as np
import rasterio
from rasterio.transform import from_origin


def bin_to_geotiff(lon_file, lat_file, val_file, out_file, res_deg=1/64):
    """
    Convert longitude, latitude, and value .bin files into a single GeoTIFF raster.

    Parameters
    ----------
    lon_file : str
        Path to longitude .bin file (dtype <f4).
    lat_file : str
        Path to latitude .bin file (dtype <f4).
    val_file : str
        Path to values .bin file (dtype <f4).
    out_file : str
        Path where the output GeoTIFF will be saved.
    res_deg : float, optional
        Resolution of the output grid in degrees (default: 1/64).
    """

    # Load data
    lon = np.fromfile(lon_file, dtype="<f4")
    lat = np.fromfile(lat_file, dtype="<f4")
    val = np.fromfile(val_file, dtype="<f4")

    # Mask invalid data
    nodata = -1.0e31
    mask = (lon > -180) & (lon < 180) & (lat > -90) & (lat < 90) & (val != nodata)
    lon, lat, val = lon[mask], lat[mask], val[mask]

    # Grid dimensions
    min_lon, max_lon = lon.min(), lon.max()
    min_lat, max_lat = lat.min(), lat.max()

    ncols = int(np.ceil((max_lon - min_lon) / res_deg))
    nrows = int(np.ceil((max_lat - min_lat) / res_deg))

    transform = from_origin(min_lon, max_lat, res_deg, res_deg)

    # Assign values to grid
    col = ((lon - min_lon) / res_deg).astype(int)
    row = ((max_lat - lat) / res_deg).astype(int)

    grid = np.full((nrows, ncols), np.nan, dtype=np.float32)
    grid[row, col] = val

    # Write GeoTIFF
    with rasterio.open(
        out_file,
        "w",
        driver="GTiff",
        height=nrows,
        width=ncols,
        count=1,
        dtype=grid.dtype,
        crs="EPSG:4326",
        transform=transform,
        nodata=-9999,
    ) as dst:
        dst.write(np.nan_to_num(grid, nan=-9999), 1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert BIN files to GeoTIFF grid")
    parser.add_argument("--lon", help="Path to longitude .bin")
    parser.add_argument("--lat", help="Path to latitude .bin")
    parser.add_argument("--val", help="Path to values .bin")
    parser.add_argument("--out", help="Output GeoTIFF path")
    parser.add_argument("--res", type=float, default=1/64, help="Grid resolution in degrees")

    args = parser.parse_args()

    if args.lon and args.lat and args.val and args.out:
        # Mode ligne de commande
        bin_to_geotiff(args.lon, args.lat, args.val, args.out, res_deg=args.res)
    else:
        # Mode debug dans Spyder (mettre tes chemins ici)
        bin_to_geotiff(
            lon_file="=longitude.bin",
            lat_file="latitude.bin",
            val_file="values.bin",
            out_file="output.tif",
            res_deg=1/64
        )
