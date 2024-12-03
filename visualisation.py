import geopandas as gpd
import matplotlib.pyplot as plt
import os

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc

def generate_subplot(axes, title, xlabel, ylabel, gdf, columnName):
    axes.set_title(title)
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)

    gdf.plot(ax=axes, column=columnName, cmap="coolwarm", legend=True)

def open_file(file_path):
    gdf = gpd.read_file(file_path)
    return gdf

def create_subplot(axes, title, xlabel, ylabel, columnName, shape_file_path):
    gdf = open_file(shape_file_path)
    gdf = remove_outliers_from_gdf(gdf, columnName)
    generate_subplot(axes, title, xlabel, ylabel, gdf, columnName)


def gen_dash_plot(gdf,columnName, title ):
    # Step 2: Convert the GeoDataFrame geometry to latitude and longitude for scatter plots
    gdf["lon"] = gdf.geometry.centroid.x
    gdf["lat"] = gdf.geometry.centroid.y

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
)

    return scatter_fig

def create_scatterplot(title, columnName, shape_file_path):
    gdf = open_file(shape_file_path)
    gdf = remove_outliers_from_gdf(gdf, columnName)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")  # Set CRS to WGS84 (latitude/longitude) 
    else:
        gdf = gdf.to_crs("EPSG:4326")  # Convert to WGS84 if not already

    return gen_dash_plot(gdf, columnName,title)


def list_all_shape_files(root_dir):
    shapefiles = []

    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".shp"):  # Check for .shp files
                absolute_path = os.path.abspath(os.path.join(dirpath, file))
                shapefiles.append(absolute_path)

    return shapefiles

def remove_outliers_from_gdf(gdf, column, method="zscore", threshold=0.4):
    """
    Remove outliers from a GeoDataFrame based on a numeric column.

    Parameters:
        gdf (GeoDataFrame): Input GeoDataFrame.
        column (str): Column name to check for outliers.
        method (str): Outlier detection method ('iqr' or 'zscore').
        threshold (float): Threshold for detecting outliers.
                           - For IQR: Multiplier for the IQR (default is 1.5).
                           - For Z-score: Max Z-score value (e.g., 3).

    Returns:
        GeoDataFrame: GeoDataFrame with outliers removed.
    """
    if method == "iqr":
        # Calculate IQR
        Q1 = gdf[column].quantile(0.25)  # 25th percentile
        Q3 = gdf[column].quantile(0.75)  # 75th percentile
        IQR = Q3 - Q1
        
        # Define lower and upper bounds
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        # Filter rows that are within bounds
        filtered_gdf = gdf[(gdf[column] >= lower_bound) & (gdf[column] <= upper_bound)]

    elif method == "zscore":
        # Calculate Z-scores
        mean = gdf[column].mean()
        std = gdf[column].std()
        gdf["zscore"] = (gdf[column] - mean) / std
        
        # Filter rows with Z-scores within the threshold
        filtered_gdf = gdf[gdf["zscore"].abs() <= threshold].drop(columns=["zscore"])

    else:
        raise ValueError("Invalid method. Use 'iqr' or 'zscore'.")

    return filtered_gdf


def my_dash():
    # Use a Bootstrap theme
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Paths to shapefiles
    fertilizer_path = "/home/abhinkop/ssd2/repos/SmartFarmingHackathon/Getreide/Farm1_Jennewein/Jennewein Anwendung24/doc/"
    harvest_path = "/home/abhinkop/ssd2/repos/SmartFarmingHackathon/Getreide/Farm1_Jennewein/Jennewein Ernte24/doc/"

    # Generate scatter plots
    a = create_scatterplot("AppliedRate", "AppliedRate", "/home/vippin/dfki/smart-farming-hackathon/data/Erntejahr 2024 (Weizen, komplett)/Dritte Gabe KAS 14_05_2024/doc/Kaichgauer G_Kraichgauer _Hühnerberg_Application_2024-05-14_00.shp")
    b = create_scatterplot("VRYIELDMAS", "VRYIELDMAS", "/home/vippin/dfki/smart-farming-hackathon/data/Erntejahr 2024 (Weizen, komplett)/Ernte Weizen 25_07_2024/doc/Kaichgauer G_Kraichgauer _Hühnerberg_Harvest_2024-07-25_00.shp")

    # Define layout
    app.layout = dbc.Container([
        # Title
        dbc.Row([
            dbc.Col(html.H1("Fertilizer and Harvest Maps", className="text-center mt-4 mb-4"), width=12)
        ]),
        # Scatter plots
        dbc.Row([
            dbc.Col(dcc.Graph(figure=a), width=12, lg=6, className="mb-4"),  # Responsive: Full width on small screens
            dbc.Col(dcc.Graph(figure=b), width=12, lg=6, className="mb-4")   # Half width on larger screens
        ]),
    ], fluid=True)  # Fluid container for full-width responsiveness

    # Run the app
    app.run_server(debug=True)


def mymain():
    shape_files = list_all_shape_files('/home/abhinkop/ssd2/repos/SmartFarmingHackathon/Getreide/Farm1_Jennewein/Jennewein Anwendung24/doc')
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))

    fertilizer_patf = "/home/abhinkop/ssd2/repos/SmartFarmingHackathon/Getreide/Farm1_Jennewein/Jennewein Anwendung24/doc/"
    harvest_path = "/home/abhinkop/ssd2/repos/SmartFarmingHackathon/Getreide/Farm1_Jennewein/Jennewein Ernte24/doc/"
    create_subplot(axes[0],"AppliedRate","Longitude","Latitude", "AppliedRate",fertilizer_patf + "Klostermühle_EJ_EJ 0080-0 Un_Application_2024-03-06_00.shp")
    create_subplot(axes[1],"VRYIELDMAS","Longitude","Latitude", "VRYIELDMAS",harvest_path + "Klostermühle_EJ_EJ 0080-0 Un_Harvest_2024-07-20_00.shp")
    # create_subplot(axes[1],"Yeild","Longitude","Latitude")

    plt.tight_layout()

    # Save the figure to a file
    output_file = "shapefile_visualization.png"
    plt.savefig(output_file, dpi=300)
    print(f"Visualization saved to {output_file}")

def visualize_shapefile_multiple(file_path):
    """
    Loads and visualizes a shapefile with multiple plots using GeoPandas and Matplotlib.

    Args:
        file_path (str): Path to the shapefile (.shp) file.
    """
    try:
        # Load the shapefile
        gdf = gpd.read_file(file_path)

        # Print basic information about the shapefile
        print("Shapefile loaded successfully!")
        print(f"Number of features: {len(gdf)}")
        print("Coordinate Reference System (CRS):", gdf.crs)
        print("First 5 rows of attribute data:\n", gdf.head())

        # Create a figure with multiple subplots
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))  # 2x2 grid of plots

        # Plot 1: Default visualization
        gdf.plot(ax=axes[0], cmap="viridis", edgecolor="black")
        axes[0].set_title("Default Visualization")
        axes[0].set_xlabel("Longitude")
        axes[0].set_ylabel("Latitude")

        # Plot 2: Attribute-based coloring (if attributes exist)
        if not gdf.empty and len(gdf.columns) > 1:
            column_name = "AppliedRate"
            gdf.plot(ax=axes[1], column=column_name, cmap="coolwarm", legend=True)
            axes[1].set_title(f"Color by {column_name}")

        # # Plot 3: Geometry boundary visualization
        # gdf.boundary.plot(ax=axes[1, 0], color="blue", linewidth=0.8)
        # axes[1, 0].set_title("Boundary Plot")
        # axes[1, 0].set_xlabel("Longitude")
        # axes[1, 0].set_ylabel("Latitude")

        # # Plot 4: Centroid visualization (if geometry has centroids)
        # gdf["centroid"] = gdf.geometry.centroid
        # gdf.plot(ax=axes[1, 1], color="lightgray", edgecolor="black", alpha=0.6)
        # gdf.centroid.plot(ax=axes[1, 1], color="red", markersize=10, label="Centroids")
        # axes[1, 1].set_title("Centroid Plot")
        # axes[1, 1].legend()

        # Adjust layout to avoid overlap
        plt.tight_layout()

        # Save the figure to a file
        output_file = "shapefile_visualization.png"
        plt.savefig(output_file, dpi=300)
        print(f"Visualization saved to {output_file}")

        # Show the plots
        # plt.show()

    except Exception as e:
        print("Error loading or visualizing the shapefile:", str(e))


# Example usage
if __name__ == "__main__":
    # # Replace with the path to your .shp file
    # shapefile_path = "/home/abhinkop/ssd2/repos/SmartFarmingHackathon/Getreide/Farm1_Jennewein/doc/Klostermühle_EJ_EJ 0080-0 Un_Application_2021-04-21_00.shp"  # Replace with the path to your shapefile
    # # shapefile_path = "path/to/your/shapefile.shp"
    # visualize_shapefile_multiple(shapefile_path)
    # mymain()
    my_dash()
