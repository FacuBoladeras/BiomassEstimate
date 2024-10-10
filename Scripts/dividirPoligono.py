import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, box
import numpy as np
import math

def dividir_shapefile(ruta_shapefile, n_partes, prefijo_salida):

    gdf = gpd.read_file(ruta_shapefile)
    # Unificar todas las geometrías en una sola
    geometria_unificada = gdf.unary_union

    # Obtener el cuadro delimitador (bounding box)
    minx, miny, maxx, maxy = geometria_unificada.bounds

    # Calcular el área total
    area_total = geometria_unificada.area

    # Área aproximada por parte
    area_por_parte = area_total / n_partes

    # Estimar el tamaño de la cuadrícula
    ancho = maxx - minx
    alto = maxy - miny
    area_bbox_total = ancho * alto

    # Número de celdas en la cuadrícula
    area_celda = area_bbox_total / n_partes
    tamano_celda = math.sqrt(area_celda)

    # Calcular el número de celdas en los ejes x e y
    n_celdas_x = max(1, int(round(ancho / tamano_celda)))
    n_celdas_y = max(1, int(round(alto / tamano_celda)))

    # Ajustar el tamaño de las celdas
    ancho_celda = ancho / n_celdas_x
    alto_celda = alto / n_celdas_y

    # Generar las celdas de la cuadrícula
    celdas_cuadricula = []
    for i in range(n_celdas_x):
        for j in range(n_celdas_y):
            x1 = minx + i * ancho_celda
            x2 = x1 + ancho_celda
            y1 = miny + j * alto_celda
            y2 = y1 + alto_celda
            celdas_cuadricula.append(box(x1, y1, x2, y2))

    # Crear un GeoDataFrame de la cuadrícula
    cuadricula_gdf = gpd.GeoDataFrame(geometry=celdas_cuadricula, crs=gdf.crs)

    # Intersectar la cuadrícula con la geometría unificada
    interseccion = gpd.overlay(cuadricula_gdf, gpd.GeoDataFrame(geometry=[geometria_unificada], crs=gdf.crs), how='intersection')

    # Calcular el área de cada polígono resultante
    interseccion['area'] = interseccion.geometry.area

    # Ordenar los polígonos por área (descendente)
    interseccion_ordenada = interseccion.sort_values(by='area', ascending=False)

    # Acumular áreas para agrupar en n partes
    interseccion_ordenada['area_acumulada'] = interseccion_ordenada['area'].cumsum()

    # Área total de la intersección
    area_total_interseccion = interseccion_ordenada['area'].sum()

    # Área objetivo por parte
    area_objetivo = area_total_interseccion / n_partes

    # Asignar identificadores de grupo a los polígonos
    ids_grupo = []
    area_actual = 0
    id_grupo = 1
    for idx, fila in interseccion_ordenada.iterrows():
        area_actual += fila['area']
        ids_grupo.append(id_grupo)
        if area_actual >= area_objetivo * id_grupo and id_grupo < n_partes:
            id_grupo += 1
    interseccion_ordenada['id_grupo'] = ids_grupo

    # Disolver polígonos por id_grupo
    poligonos_divididos = interseccion_ordenada.dissolve(by='id_grupo')

    # Guardar cada parte en un shapefile separado
    for idx, fila in poligonos_divididos.iterrows():
        parte_gdf = gpd.GeoDataFrame(geometry=[fila.geometry], crs=gdf.crs)
        ruta_salida = f"{prefijo_salida}_parte_{idx}.shp"
        parte_gdf.to_file(ruta_salida)
        print(f"Parte {idx} guardada en {ruta_salida}")


input = r"C:\Users\Facu\Desktop\Kisangani\Kisangani.shp"
prefijo = "kisangani"
dividir_shapefile(input,4, prefijo)