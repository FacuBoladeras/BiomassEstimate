import os
import numpy as np
import rasterio
from scipy.ndimage import generic_filter

def fill_nan_with_neighbors(input_tiff, output_tiff, radius=1, min_valid_neighbors=3):
    """
    Rellena los valores NaN en un TIFF utilizando un número definido de píxeles vecinos válidos.

    Parameters:
    - input_tiff: Ruta del archivo TIFF de entrada.
    - output_tiff: Ruta del archivo TIFF de salida.
    - radius: Radio de vecinos a considerar para la interpolación (por defecto 1).
    - min_valid_neighbors: Mínimo número de vecinos válidos requeridos para rellenar un píxel NaN (por defecto 3).
    """

    def interpolate(values):
        """Función interna para rellenar NaN si se cumplen los vecinos mínimos válidos."""
        center_value = values[len(values) // 2]
        
        if np.isnan(center_value):
            # Contar la cantidad de vecinos válidos (no NaN)
            valid_neighbors = values[~np.isnan(values)]
            
            # Si hay suficientes vecinos válidos, devolver el promedio, si no, devolver NaN
            if len(valid_neighbors) >= min_valid_neighbors:
                return np.mean(valid_neighbors)
            else:
                return np.nan
        else:
            return center_value

    with rasterio.open(input_tiff) as src:
        array = src.read(1)  # Leer la primera banda
        meta = src.meta

    # Crear un tamaño de filtro basado en el radio
    filter_size = (2 * radius + 1, 2 * radius + 1)

    # Aplicar el filtro para rellenar NaNs usando la función de interpolación definida
    filled_array = generic_filter(array, interpolate, size=filter_size)

    # Guardar el resultado en un nuevo archivo TIFF
    meta.update(dtype=rasterio.float32)

    with rasterio.open(output_tiff, "w", **meta) as dest:
        dest.write(filled_array, 1)

    print(f"Archivo guardado en: {output_tiff}")

# Ejemplo de uso
input_tiff = r"C:\Users\Facu\Downloads\Outputs\AGBD_2018.tif"
output_tiff = r"C:\Users\Facu\Downloads\Outputs\AGBD2_2018.tif"
fill_nan_with_neighbors(input_tiff, output_tiff, radius=2, min_valid_neighbors=5)
