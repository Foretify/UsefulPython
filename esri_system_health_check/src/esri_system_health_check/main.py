from cProfile import run
import sys
import time
import os
import pandas as pd
from datetime import date
from common import common as cm
from arcgis.gis import GIS
from arcgis.features import GeoAccessor



def main():
    runner_start_time = time.time()
    print("Starting the process of checking the health of the Esri System\n")
    print(runner_start_time)


    # 1. Can we connect to the ArcGIS Portal or AGOL @topowright

        # Read Configuration File
        # This is the configuration file that has all connection info for the script to 
        # run ie layers from AGOL and connection parameters
        # Create the config parser object to store all the connection information for AGOL

    print("Reading details Configuration File")
    

    config_dir = cm.get_config_path()
    
    config = cm.load_configuration(config_dir)
    print(f"configuration file location:\n{config_dir}")
    print("Querying Content from ArcGIS")
    arcgis_org_url = config.get('ArcGIS Credentials', 'arcgis_org_url')
    username = config.get('ArcGIS Credentials', 'username')
    password = config.get('ArcGIS Credentials', 'password')
    folder_name = config.get('ArcGIS Online Test Folder', 'folder')
    csv_path = config.get('ArcGIS Online Test Folder', 'csv_path')
    layer_title = config.get('ArcGIS Online Test Folder', 'csv_layer')

    gis = cm.connect(org_url=arcgis_org_url, login_name=username, user_password=password)


    # 2. Can we connect to ArcGIS Server
    # 3. Can we connect to the web adaptors for portal and server
    # 4. We need to understand the user type and permissions of the user
    # 5. We need to be able to create a folder and delete a folder in the users content

        # create folder:
    print("5. Creating a folder that will be deleted in step 6\n")
    cm.create_folder_in_ags(gis, folder_name)

    # 7. We need to be able to publish an excel as a hosted feature service
    print("6. Creating a layer in the hosted server from a csv that is stored locally\n")
    cm.create_layer_in_test_folder(gis, csv_path, folder_name, layer_title)

        # delete folder:
    cm.delete_folder_in_args(gis, folder_name)


    # 6. We need to be able to publish a shapefile as a hosted feature service

    

    



    # 8. We need to be able to pull down these files and edit the content and push back our edits
    # 9. We need to be able to run a geometry query on this data and produce a new layer in the enterprise based on this query
    # 10. We need to be able to create new users
    


    

    print("Completed all necessary steps")

# Processing Steps to check the health of the system
if __name__ == "__main__":
    main()