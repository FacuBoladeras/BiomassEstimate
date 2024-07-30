import geopandas as gpd
from shapely.geometry import Point
import numpy as np

def generate_equidistant_points(input_shapefile, output_shapefile, distance_km=5):
    # Leer el archivo shapefile
    gdf = gpd.read_file(input_shapefile)

    # Asegurarse de que el CRS está en un sistema de coordenadas proyectadas (metros)
    if not gdf.crs or gdf.crs.is_geographic:
        gdf = gdf.to_crs(epsg=3857)  # Proyección Web Mercator

    # Obtener el polígono
    polygon = gdf.geometry.unary_union

    # Crear una cuadrícula de puntos
    minx, miny, maxx, maxy = polygon.bounds
    x = np.arange(minx, maxx, distance_km * 1000)
    points = [Point(xi, yi) for xi in x for yi in np.arange(miny, maxy, distance_km * 1000)]

    # Filtrar puntos dentro del polígono
    points_inside = [point for point in points if polygon.contains(point)]

    # Crear un nuevo GeoDataFrame con los puntos
    points_gdf = gpd.GeoDataFrame(geometry=points_inside, crs=gdf.crs)

    # Convertir de vuelta a WGS84 (EPSG:4326) para guardar
    points_gdf = points_gdf.to_crs(epsg=4326)

    # Guardar como nuevo shapefile
    points_gdf.to_file(output_shapefile)

    print(f"Se han generado {len(points_inside)} puntos equidistantes.")
    return points_gdf

generate_equidistant_points("C:/Users/Facu/Documents/Nepal.shp", "C:/Users/Facu/Desktop/puntos_nepal.shp", distance_km=5)