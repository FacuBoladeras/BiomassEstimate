import rasterio
import numpy as np

def fill_nan_with_value(tiff_path, output_path, fill_value=1):
    """
    Rellena los valores NaN de un archivo TIFF con un valor específico.

    Parámetros:
        tiff_path (str): Ruta al archivo TIFF original.
        output_path (str): Ruta donde se guardará el TIFF modificado.
        fill_value (int/float): Valor con el que se reemplazarán los NaN (default = 0).
    """
    # Abrir el archivo TIFF
    with rasterio.open(tiff_path) as src:
        # Leer los datos como una matriz numpy
        data = src.read(1)  # Leer solo la primera banda
        
        # Reemplazar los valores NaN con el valor especificado
        data_filled = np.nan_to_num(data, nan=fill_value)
        
        # Obtener la metadata del archivo original
        out_meta = src.meta.copy()
    
    # Guardar el archivo TIFF modificado
    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(data_filled, 1)  # Escribir en la primera banda
    
    print(f"El archivo TIFF con valores NaN reemplazados ha sido guardado en: {output_path}")



# Configuración de parámetros
tiff_path = r"C:\Users\Facu\Downloads\Rf_Bootstrap_mdg_south_20119\Bootstrap_mdg_south_2019_sde.tif"  # Ruta del raster original
shapefile_path = r"C:\Users\Facu\Documents\mgd_south.shp"  # Ruta del shapefile
output_path = r"C:\Users\Facu\Downloads\Output mdg_south\mdg_south_sde_2019.tif"  # Ruta del archivo TIFF de salida
fill_value = 1  # Valor con el que se rellenarán los píxeles sin datos

fill_nan_with_value(tiff_path, output_path, fill_value=1)
