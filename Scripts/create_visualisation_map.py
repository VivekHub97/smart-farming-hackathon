
import geopandas as gpd
import plotly.express as px

import find_json_files as  find

# Predefined color scales in Plotly
COLOR_SCALES = [
    "Viridis",
    "Cividis",
    "Plasma",
    "Inferno",
    "Magma",
    "Turbo",
    "Blues",
    "Greens",
    "Purples",
    "Oranges",
]

def gen_dash_plot(gdf, columnName, title, call_count=0):
    # Step 2: Convert the GeoDataFrame geometry to latitude and longitude for scatter plots
    # gdf["lon"] = gdf.geometry.centroid.x
    # gdf["lat"] = gdf.geometry.centroid.y

    # # Reproject to a suitable projected CRS (e.g., UTM)
    # if gdf.crs.is_geographic:
    #     gdf = gdf.to_crs(gdf.estimate_utm_crs())
    
    # Calculate centroids in the projected CRS
    gdf["lon"] = gdf.geometry.centroid.x
    gdf["lat"] = gdf.geometry.centroid.y

    # # Reproject back to the original CRS for visualization if needed
    # gdf = gdf.to_crs("EPSG:4326")

    # Get the minimum and maximum values of the column
    # min_val = gdf[columnName].min()
    # max_val = gdf[columnName].max()

    # Select a color scale based on the call count
    color_scale = COLOR_SCALES[call_count % len(COLOR_SCALES)]

    scatter_fig = px.scatter_mapbox(
    gdf,
    lat="lat",
    lon="lon",
    color=columnName,  # Replace with a column from your shapefile
    # size=columnName,  # Optional: Scale points based on a column
    hover_name=columnName,  # Replace with a relevant column
    title=title,
    mapbox_style="open-street-map",
    zoom=15,
    height=600,
    # range_color=[min_val, max_val],
    # color_continuous_scale=color_scale,  # Dynamic color scale
)

    return scatter_fig

# Function to create a Mapbox scatter plot from shapefiles
def create_visualisation_map(columnName, shapefile_path, title, count):
    
    # Read the shapefile
    gdf = gpd.read_file(shapefile_path)
    
    # Ensure coordinate system is WGS84 (EPSG:4326)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")  # Set CRS to WGS84 (latitude/longitude) 
    else:
        gdf = gdf.to_crs("EPSG:4326")  # Convert to WGS84 if not already
        
    gdf = gdf.to_crs("EPSG:4326")  # Convert to WGS84 if not already
    
    gdf = find.remove_outliers_from_gdf(gdf,columnName)

    fig = gen_dash_plot(gdf,columnName,title, count)
    
    # Update layout
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0}  # Minimal margins for full-width maps
    )
    return fig