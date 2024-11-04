import h3
import geopandas as gpd
from shapely.geometry import Polygon

def generate_hexagons_from_gdf(gdf, resolution, output_filename):
    """
    Converts a GeoDataFrame into a hexagon grid and saves it as a new shapefile.

    Parameters:
    - gdf (GeoDataFrame): Input GeoDataFrame with geometries to cover with hexagons.
    - resolution (int): Resolution level for H3 hexagons (0-15, higher is finer).
    - output_filename (str): Path for saving the output shapefile.

    Returns:
    - hex_gdf (GeoDataFrame): GeoDataFrame of hexagons covering the input geometries.
    """
    
    hexagons = set()
    
    # Iterate through each geometry in the GeoDataFrame
    for geom in gdf.geometry:
        # Convert each polygon to hexagons at the specified resolution, using geo_json_conformant=True
        hex_ids = h3.polyfill(geom.__geo_interface__, resolution, geo_json_conformant=True)
        hexagons.update(hex_ids)
    
    # Convert hexagon IDs to shapely Polygon objects
    hexagon_polygons = [Polygon(h3.h3_to_geo_boundary(hex_id, geo_json=True)) for hex_id in hexagons]
    
    # Create a new GeoDataFrame with the hexagon polygons
    hex_gdf = gpd.GeoDataFrame(geometry=hexagon_polygons, crs=gdf.crs)
    
    # Save to a new shapefile
    hex_gdf.to_file(output_filename, driver='ESRI Shapefile')
    
    return hex_gdf

# Load your input shapefile
input_gdf = gpd.read_file(r"C:\Users\Facu\Documents\AreaDeEstudio_Nueva.shp")

# Define the H3 resolution (e.g., resolution 7)
resolution = 7

# Define the output file name
output_filename = "hexagon_grid_output.shp"

# Generate hexagons and save to a shapefile
hex_gdf = generate_hexagons_from_gdf(input_gdf, resolution, output_filename)
