
import create_visualisation_map as cv
import new_dash as my_dash
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
    
    # my_dash.add_map(map1)
    # my_dash.add_map(map2)

    my_dash.map_list.append(map1)
    my_dash.map_list.append(map2)