import os
import rasterio
from rasterio.merge import merge
from rasterio.enums import Resampling

def define_nodata(tiff_file, nodata_value=0):
    """
    Define un valor nodata en un archivo TIFF existente.

    Parameters:
    - tiff_file: Ruta del archivo TIFF que se va a modificar.
    - nodata_value: Valor nodata a establecer (por defecto 0).
    """
    with rasterio.open(tiff_file, "r+") as src:
        # Establecer el valor nodata
        src.nodata = nodata_value

def merge_tiffs_ignore_nodata(input_folder, output_path, nodata_value=0):
    """
    Lee todos los archivos TIFF de una carpeta y los une en un único archivo TIFF,
    ignorando los valores nodata definidos.

    Parameters:
    - input_folder: Ruta de la carpeta que contiene los archivos TIFF.
    - output_path: Ruta del archivo TIFF de salida que se generará.
    - nodata_value: Valor nodata a definir para cada TIFF (por defecto 0).
    """
    # Obtener una lista de archivos TIFF en la carpeta
    tiff_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.tif')]
    
    if not tiff_files:
        raise FileNotFoundError("No se encontraron archivos TIFF en la carpeta proporcionada.")
    
    # Lista para almacenar los datasets
    src_files_to_mosaic = []

    # Definir nodata en cada archivo TIFF y abrir los datasets
    for fp in tiff_files:
        define_nodata(fp, nodata_value=nodata_value)
        src = rasterio.open(fp)
        src_files_to_mosaic.append(src)

    # Unir los archivos TIFF ignorando el valor nodata
    mosaic, out_trans = merge(src_files_to_mosaic, nodata=nodata_value)
    
    # Copiar los metadatos del primer archivo
    out_meta = src_files_to_mosaic[0].meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans,
        "count": mosaic.shape[0],
        "nodata": nodata_value
    })

    # Guardar el archivo unido
    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(mosaic)

    print(f"Archivo combinado guardado en: {output_path}")

# Ejemplo de uso
input_folder = r"C:\Users\Facu\Downloads\ste_2023"
output_path = r"C:\Users\Facu\Downloads\ste_2023\tiff_unidio.tif"
merge_tiffs_ignore_nodata(input_folder, output_path)
