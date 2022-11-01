
import sys
import time
import os
import pandas as pd
import random
from datetime import date
from arcgis.gis import GIS
from cProfile import run
from common import common as cm
from arcgis.features import GeoAccessor

def main():
    runner_start_time = time.time()
    print(" \nStarting the process of checking the status of the Esri System")
    print(" - Reading details Configuration File")
    
    # 1. Can we connect to the ArcGIS Portal or AGOL 

        # Read Configuration File
        # This is the configuration file that has all connection info for the script to run correctly
        # Create the config parser object to store all the connection information for AGOL

    config_dir = cm.get_config_path()
    
    config = cm.load_configuration(config_dir)
    
    print(f" - Pulling information from the configuration file. Config file location:\n{config_dir} ")
    print("  - Querying Content from ArcGIS\n")
    arcgis_org_url = config.get('ArcGIS Credentials', 'arcgis_org_url')
    username = config.get('ArcGIS Credentials', 'username')
    password = config.get('ArcGIS Credentials', 'password')
    folder_name = config.get('Test Folder', 'folder')
    folder_name = folder_name + str(random.randint(1,10000))
    csv_path = config.get('Test Folder', 'csv_path')
    layer_title = config.get('Test Folder', 'csv_layer')
    
    layer_title = layer_title + str(random.randint(1,10000))
    sample_item = config.get('ArcGIS Items', 'test_item')
    print("##########################################################\n")

    # 1.Creating the GIS Object to connect to the instance of ArcGIS
    print('1. Testing the connection to ArcGIS Enterprise or AGOL ')
    
    print(" - Creating the GIS Object to connect to the instance of ArcGIS")

    gis = cm.connect(org_url=arcgis_org_url, login_name=username, user_password=password)
    status = gis.properties.portalName
    
    print(f" - Completed connecting to a {status}\n")
    print("##########################################################\n")

    if status == 'ArcGIS Online': 
        print(f'We are skipping steps 2 and 3 due to the instance being {status}.')
    
    # 2. Can we connect to ArcGIS Server
    print('2. Can we connect to ArcGIS Server')
    print(' - Here is the first thing we do. ')
    print(' - Here is the next thing we do. ')
    print(' - We completed doing the things for section 2. \n')
    print("##########################################################\n")


    # 3. Can we connect to the web adaptors for portal and server
    print('3. Can we connect to the web adaptors for portal and server')
    print(' - Here is the first thing we do. ')
    print(' - Here is the next thing we do. ')
    print(' - We completed doing the things for section 3. \n')
    print("##########################################################\n")
    

    # 4. Pull a gis item into a dataframe and create a feature set from this item
    
    print("4. Testing pulling a GIS item into a DataFrame and creating a feature set from this item")
    print(' - Pulling GIS item URL from Configuration file. ')
       
    itm = sample_item
    sample_itm = cm.get_gis_item(itm, gis)
    sample_lyr = sample_itm.layers[0]
    sample_fs = sample_lyr.query()
    sample_df = sample_lyr.query(as_df=True)
    print(' - Querying data from GIS item. ')
    print(f' - Successfully wrote data from GIS item: {itm} into a dataframe. \n')
    print("##########################################################\n")


    # 5. We need to be able to create a folder and delete a folder in the users content
    print("5. Testing the ability to create a folder\n")
    cm.create_folder_in_ags(gis, folder_name)
    print(f' - Successfully created a folder in {status}')
    print(f' - {folder_name} will be deleted in a subsequent test. \n')
    print("##########################################################\n")


    # 6. We need to be able to publish an excel as a hosted feature service
    print("6. Testing the ability to create a layer in the hosted server from a csv that is stored locally\n")
    cm.create_layer_in_test_folder(gis, csv_path, folder_name, layer_title)
    print(f' - Successfully created a hosted feature layer from a csv in {status}\n')
    print("##########################################################\n")

    # 7. Cleaning up the test data by deleting the folder created
    print('7. Cleaning up the test data by deleting the folder created in step 5')
    cm.delete_folder_in_args(gis, folder_name)
    print(f' - Successfully deleted the test folder: {folder_name} created in {status}\n')
    print("##########################################################\n")

    # 8. We need to be able to publish a shapefile as a hosted feature service
    print(f'8. Testing the ability to publish a shapefile as a hosted feature service')
    print(' - Here is the first thing we do. ')
    print(' - Here is the next thing we do. ')
    print(' - We completed doing the things for section 8. \n')
    print("##########################################################\n")


    # 9. We need to be able to pull down these files and edit the content and push back our edits
    print('9. Testing the ability to pull a feature layer into a DataFrame, remove all the content, and add new content.')
    print(' - Here is the first thing we do. ')
    print(' - Here is the next thing we do. ')
    print(' - We completed doing the things for section 9. \n')
    print("##########################################################\n")
    
    print("Completed all necessary steps. ")

# Processing Steps to check the health of the system
if __name__ == "__main__":
    main()