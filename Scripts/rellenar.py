import numpy as np
import rasterio
from scipy.ndimage import generic_filter

def fill_nodata(input_tiff, output_tiff, size=3, iterations=1):
    """
    Rellena los valores NaN en un archivo TIFF basado en el promedio de los vecinos.
    
    :param input_tiff: Ruta al archivo TIFF de entrada.
    :param output_tiff: Ruta al archivo TIFF de salida.
    :param size: Número de píxeles vecinos (ventana cuadrada) a tomar en cuenta para el relleno.
    :param iterations: Número de iteraciones para el relleno.
    """
    # Abrir el archivo TIFF
    with rasterio.open(input_tiff) as src:
        data = src.read(1)  # Leer la primera banda del TIFF
        profile = src.profile  # Obtener los metadatos del raster

    # Inicializar la máscara de valores nodata (NaN)
    nodata_mask = np.isnan(data)
    
    # Función para rellenar los nodata utilizando vecinos
    def fill_with_neighbors(values):
        center_value = values[len(values) // 2]  # Valor central
        if np.isnan(center_value):  # Si es nodata, llenar con la media de los vecinos
            neighbor_values = values[~np.isnan(values)]  # Excluir nodata en los vecinos
            if len(neighbor_values) > 0:
                return np.mean(neighbor_values)  # Promedio de vecinos
            else:
                return np.nan  # Mantener como NaN si no hay vecinos válidos
        return center_value  # Dejar el valor intacto si no es nodata

    # Realizar el relleno en múltiples iteraciones
    for _ in range(iterations):
        # Aplicar el relleno usando una ventana de vecinos (size x size)
        data = generic_filter(data, fill_with_neighbors, size=(size, size), mode='constant', cval=np.nan)

    # Reemplazar los NaN restantes por 0, si se requiere
    data = np.nan_to_num(data, nan=0)

    # Guardar el nuevo TIFF con los valores rellenados
    profile.update(dtype=rasterio.float32)  # Asegurarse de que el tipo de datos sea correcto
    with rasterio.open(output_tiff, 'w', **profile) as dst:
        dst.write(data, 1)
    
    print(f"Archivo TIFF rellenado guardado en: {output_tiff}")

# Ejemplo de uso
input_tiff = r"C:\Users\Facu\Downloads\Malambique_2010_30m.tif"
output_tiff = r"C:\Users\Facu\Downloads\Malambique_2010_relleno.tif"

# Rellenar los valores nodata utilizando una ventana de 3x3 vecinos y 2 iteraciones
fill_nodata(input_tiff, output_tiff, size=3, iterations=2)
