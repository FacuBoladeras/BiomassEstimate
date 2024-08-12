import rasterio
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject
import numpy as np

def resample_raster(input_tiff, output_tiff, scale_factor):
    # Abrir el archivo raster de entrada
    with rasterio.open(input_tiff) as src:
        transform, width, height = calculate_default_transform(
            src.crs, src.crs, src.width, src.height, 
            src.bounds.left, src.bounds.bottom, 
            src.bounds.right, src.bounds.top, 
            dst_width=int(src.width / scale_factor), 
            dst_height=int(src.height / scale_factor)
        )

        # Actualizar los metadatos del nuevo raster
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': src.crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Leer los datos del raster de entrada
        data = src.read(
            out_shape=(src.count, int(src.height / scale_factor), int(src.width / scale_factor)),
            resampling=Resampling.average
        )

        # Escribir los datos remuestreados en el archivo de salida
        with rasterio.open(output_tiff, 'w', **kwargs) as dst:
            dst.write(data)

    print(f"Nuevo TIFF remuestreado guardado en: {output_tiff}")

# Rutas de los archivos de entrada y salida
input_tiff = r"C:\Users\Facu\Downloads\Malawi_2010-L-P (1).tif"
output_tiff = "malawi-resample-2010.tif"

# Factor de escala para remuestrear a 100x100 metros desde 30x30 metros
scale_factor = 100 / 30

# Ejecutar la función
resample_raster(input_tiff, output_tiff, scale_factor)
