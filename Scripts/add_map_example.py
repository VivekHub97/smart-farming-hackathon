
import create_visualisation_map as cv
import geopandas as gpd
from globals import map_list, add_map
import find_json_files as find
def populate():
    # File paths
    fertilizer_path = "/home/abhinkop/ssd2/repos/SmartFarmingHackathon/Getreide/Farm1_Jennewein/Jennewein Anwendung24/doc/"
    harvest_path = "/home/abhinkop/ssd2/repos/SmartFarmingHackathon/Getreide/Farm1_Jennewein/Jennewein Ernte24/doc/"

# Create the maps   
    map1 = cv.create_visualisation_map(
    columnName="AppliedRate",
    shapefile_path= fertilizer_path + "Klostermühle_EJ_EJ 0080-0 Un_Application_2024-03-06_00.shp",
    title="AppliedRate"
)

    map2 = cv.create_visualisation_map(
    columnName="VRYIELDMAS",
    shapefile_path= harvest_path + "Klostermühle_EJ_EJ 0080-0 Un_Harvest_2024-07-20_00.shp",
    title="VRYIELDMAS"
)
    
    add_map(map1)
    add_map(map2)

def add_fertiliser_plots(fertilizer_path):

    json_files = find.find_json_files(fertilizer_path)

    for i, json_file in enumerate(json_files):
        print(find.get_product_name(json_file))

        map = cv.create_visualisation_map(
            columnName="AppliedRate",
            shapefile_path= find.generate_shape_filename(json_file),
            title=find.get_product_name(json_file), count=i
        )

        add_map(map)

def add_harvest_plots(harvest_path):

    json_files = find.find_json_files(harvest_path)

    for i, json_file in enumerate(json_files):

        map = cv.create_visualisation_map(
            columnName="VRYIELDMAS",
            shapefile_path= find.generate_shape_filename(json_file),
            title=find.get_crop_name(json_file), count=i
        )

        add_map(map)

def add_emission_plots(emission_path):
    shapefile_path = emission_path + "/combined_data.geojson"
    columns = ["Emissions", "FuelEmissions", "YieldEmissions"]
    for i, column in enumerate(columns):

        gdf = gpd.read_file(shapefile_path)
        if column in gdf.columns:
            print(column)
            map = cv.create_visualisation_map(
                columnName=column,
                shapefile_path= shapefile_path,
                title=column, count=i
            )

            add_map(map)


def populate_new():
    fertilizer_path = "/home/abhinkop/ssd2/repos/SmartFarmingHackathon/Getreide/Farm1_Jennewein/JenneweinAnwendung23/doc/"
    harvest_path = "/home/abhinkop/ssd2/repos/SmartFarmingHackathon/Getreide/Farm1_Jennewein/JenneweinErnte23/doc/"

    add_fertiliser_plots(fertilizer_path)
    add_harvest_plots(harvest_path)


def populate_new(year, Farm1 = True):
    if Farm1:
        fertilizer_path = "data/JenneweinAnwendung"+str(year)+"/doc/"
        harvest_path = "data/JenneweinErnte"+str(year)+"/doc/"
        emission_path = "data/JenneweinAnwendung"+str(year)
    else:
        print("here")
        fertilizer_path = "data/Gemmingen"+str(year)+"/doc/"
        harvest_path = "data/Gemmingen"+str(year)+"/doc/"
        emission_path = "data/Gemmingen"+str(year)

    add_fertiliser_plots(fertilizer_path)
    add_harvest_plots(harvest_path)
    add_emission_plots(emission_path)