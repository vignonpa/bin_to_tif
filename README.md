# BIN to TIFF Conversion Tools

This repository contains two Jupyter notebooks for converting **binary data files (.bin)** into **TIF** raster images.  

---

## 📂 Notebooks

### 1. `bin_to_tif_shape.ipynb`
- Converts three `.bin` files (latitude, longitude, value) into a **3-channel TIFF**.  
- Each channel stores one variable.
- Uses a user-defined shape (`image_shape`) in px x px.  
- Includes validation checks and visualization.  

### 2. `bin_to_tif_res.ipynb`
- Converts three `.bin` files (latitude, longitude, value) into a **georeferenced GeoTIFF**.  
- Uses a user-defined resolution (`res_deg`) in degrees.  
- Interpolates values into a raster grid.  
- Exports as `EPSG:4326` by default.  

---

## ⚙️ Requirements
Install dependencies:
```bash
pip install numpy matplotlib pandas rasterio tifffile
