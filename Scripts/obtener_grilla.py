import geopandas as gpd
from shapely.geometry import box
import numpy as np

def create_grid(gdf, cell_size):
    # Asegurarnos de que el GeoDataFrame esté en un CRS proyectado para calcular distancias en metros
    if gdf.crs.to_string() != "EPSG:3857":
        gdf = gdf.to_crs("EPSG:3857")
    
    polygon = gdf.unary_union  # Combinar todas las geometrías en una sola
    minx, miny, maxx, maxy = polygon.bounds
    x_coords = np.arange(minx, maxx, cell_size)
    y_coords = np.arange(miny, maxy, cell_size)
    
    cells = []
    cell_id = 1
    
    for x in x_coords:
        for y in y_coords:
            cell = box(x, y, x + cell_size, y + cell_size)
            if polygon.intersects(cell):
                intersected_cell = polygon.intersection(cell)
                cells.append({'geometry': intersected_cell, 'id': cell_id})
                cell_id += 1
                
    return gpd.GeoDataFrame(cells, crs="EPSG:3857")

# Cargar el shapefile con el polígono
input_shapefile = r"C:\Users\Facu\Desktop\MalawiWoodfuelSite_1a.shp"
gdf = gpd.read_file(input_shapefile)

# Crear la grilla de 100x100 metros
cell_size = 100  # en metros, ajusta esto si necesitas una unidad diferente
grid = create_grid(gdf, cell_size)

# Convertir de nuevo al CRS original si es necesario
grid = grid.to_crs(gdf.crs)

# Guardar el resultado como un nuevo shapefile
output_shapefile = "Malawi-grid.shp"
grid.to_file(output_shapefile)

print("Grilla creada y guardada en:", output_shapefile)
