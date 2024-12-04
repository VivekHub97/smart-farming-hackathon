import json
import os

def find_json_files(folder_path):
    """
    Find all JSON files in a folder and its subdirectories.

    Args:
        folder_path (str): The root folder path to search for JSON files.

    Returns:
        list: A list of absolute paths to all JSON files found.
    """
    json_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

def generate_shape_filename(json_filename):
    shape_file_name = json_filename.replace('-Deere-Metadata', '')
    shape_file_name = shape_file_name.replace('.json', '.shp')
    return shape_file_name

def fetch_json_data(json_file_name):
    f = open(json_file_name, "r")
    jsonfile = json.load(f)
    return jsonfile

def get_product_name(json_file_name):
    jsonfile = fetch_json_data(json_file_name)
    return str(jsonfile['Product']['ProductName'])

def get_crop_name(json_file_name):
    jsonfile = fetch_json_data(json_file_name)
    return str(jsonfile['CropName'])

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

