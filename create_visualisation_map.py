
import geopandas as gpd
import plotly.express as px

import find_json_files as  find

def gen_dash_plot(gdf,columnName, title ):
    # Step 2: Convert the GeoDataFrame geometry to latitude and longitude for scatter plots
    gdf["lon"] = gdf.geometry.centroid.x
    gdf["lat"] = gdf.geometry.centroid.y

    scatter_fig = px.scatter_mapbox(
    gdf,
    lat="lat",
    lon="lon",
    color=columnName,  # Replace with a column from your shapefile
    size=columnName,  # Optional: Scale points based on a column
    hover_name=columnName,  # Replace with a relevant column
    title=title,
    mapbox_style="open-street-map",
    zoom=15,
    height=600,
)

    return scatter_fig

# Function to create a Mapbox scatter plot from shapefiles
def create_visualisation_map(columnName, shapefile_path, title):
    
    # Read the shapefile
    gdf = gpd.read_file(shapefile_path)
    
    # Ensure coordinate system is WGS84 (EPSG:4326)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")  # Set CRS to WGS84 (latitude/longitude) 
    else:
        gdf = gdf.to_crs("EPSG:4326")  # Convert to WGS84 if not already
        
    gdf = gdf.to_crs("EPSG:4326")  # Convert to WGS84 if not already
    
    # gdf = find.remove_outliers_from_gdf(gdf,columnName)

    fig = gen_dash_plot(gdf,columnName,title)
    
    # Update layout
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0}  # Minimal margins for full-width maps
    )
    return fig