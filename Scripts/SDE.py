import numpy as np
import rasterio

def calculate_mean_and_std(tiff_1, tiff_2, tiff_3, output_mean_path, output_std_path):

    # Abrir los archivos TIFF
    with rasterio.open(tiff_1) as src1:
        data1 = src1.read(1)
        metadata = src1.meta.copy()

    with rasterio.open(tiff_2) as src2:
        data2 = src2.read(1)

    with rasterio.open(tiff_3) as src3:
        data3 = src3.read(1)

    # Calcular el promedio y el desvío estándar
    stack_data = np.stack([data1, data2, data3], axis=0)
    mean_data = np.mean(stack_data, axis=0)
    std_data = np.std(stack_data, axis=0)

    # Actualizar metadata
    metadata.update(dtype=rasterio.float32, count=1, nodata=np.nan)

    # Guardar el TIFF de salida con el promedio
    with rasterio.open(output_mean_path, 'w', **metadata) as dst_mean:
        dst_mean.write(mean_data.astype(rasterio.float32), 1)

    # Guardar el TIFF de salida con el desvío estándar
    with rasterio.open(output_std_path, 'w', **metadata) as dst_std:
        dst_std.write(std_data.astype(rasterio.float32), 1)

    print(f'Archivo TIFF con el promedio guardado en: {output_mean_path}')
    print(f'Archivo TIFF con el desvío estándar guardado en: {output_std_path}')

# Ejemplo de uso
tiff_1 = r'C:\Users\Facu\Downloads\Estimators_sde\malambique_completo.tif'
tiff_2 = r'C:\Users\Facu\Downloads\Estimators_sde\malambique_opt.tif'
tiff_3 = r'C:\Users\Facu\Downloads\Estimators_sde\malambique_rad.tif'
output_mean_path = 'path_to_output_mean.tif'
output_std_path = 'path_to_output_std.tif'


calculate_mean_and_std(tiff_1, tiff_2, tiff_3, output_mean_path, output_std_path)

