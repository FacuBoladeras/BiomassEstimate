import os
import numpy as np
import rasterio

def calculate_mean_and_std_from_folder(folder_path):
    """
    Lee todos los archivos TIFF en una carpeta y calcula la media y la desviación estándar pixel a pixel.

    Args:
        folder_path (str): Ruta a la carpeta que contiene los archivos TIFF.

    Returns:
        mean_data (numpy array): Array con la media pixel a pixel.
        std_data (numpy array): Array con la desviación estándar pixel a pixel.
        metadata (dict): Metadatos para guardar los archivos TIFF resultantes.
    """
    # Obtener todos los archivos TIFF en la carpeta
    tiff_files = [os.path.join(folder_path, f)
                  for f in os.listdir(folder_path)
                  if f.endswith('.tif') or f.endswith('.tiff')]

    if len(tiff_files) == 0:
        print(f"No se encontraron archivos TIFF en la carpeta {folder_path}")
        return None, None, None

    # Lista para almacenar los datos de los TIFFs
    data_stack = []

    # Leer y apilar los datos de cada archivo TIFF
    for idx, tiff_file in enumerate(tiff_files):
        with rasterio.open(tiff_file) as src:
            data = src.read(1)  # Leer la primera banda
            data_stack.append(data)
            if idx == 0:
                metadata = src.meta.copy()
                # Verificar dimensiones
                height, width = data.shape
            else:
                if data.shape != (height, width):
                    print(f"Dimensiones incompatibles en el archivo {tiff_file}")
                    return None, None, None

    # Convertir a array de numpy y calcular la media y desviación estándar
    stack_data = np.stack(data_stack, axis=0)
    mean_data = np.mean(stack_data, axis=0)
    std_data = np.std(stack_data, axis=0)

    return mean_data, std_data, metadata

# Ejemplo de uso
folder_path = r'C:\Users\Facu\Downloads\2010'  # Reemplaza con tu ruta

mean_data, std_data, metadata = calculate_mean_and_std_from_folder(folder_path)

# Si deseas guardar los resultados como archivos TIFF
if mean_data is not None and std_data is not None:
    # Actualizar metadatos para los archivos de salida
    metadata.update(dtype=rasterio.float32, count=1, nodata=None)

    output_mean_path = os.path.join(folder_path, 'mean.tif')
    output_std_path = os.path.join(folder_path, 'std.tif')

    # Guardar el TIFF con la media
    with rasterio.open(output_mean_path, 'w', **metadata) as dst_mean:
        dst_mean.write(mean_data.astype(rasterio.float32), 1)

    # Guardar el TIFF con la desviación estándar
    with rasterio.open(output_std_path, 'w', **metadata) as dst_std:
        dst_std.write(std_data.astype(rasterio.float32), 1)

    print(f'Archivo TIFF con la media guardado en: {output_mean_path}')
    print(f'Archivo TIFF con la desviación estándar guardado en: {output_std_path}')
else:
    print('No se pudo calcular la media y la desviación estándar.')
