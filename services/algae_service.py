import rasterio
import numpy as np

def calculate_algae(filepath):
    with rasterio.open(filepath) as src:
        red = src.read(3)
        nir = src.read(4)
        ndvi = (nir - red) / (nir + red + 1e-10)
        return ndvi.tolist()

