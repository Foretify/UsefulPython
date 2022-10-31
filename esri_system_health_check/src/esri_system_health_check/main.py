
import sys
import time
import os
import pandas as pd
from datetime import date
from arcgis.gis import GIS
from cProfile import run
from common import common as cm
from arcgis.features import GeoAccessor

def main():
    runner_start_time = time.time()
    print("Starting the process of checking the status of the Esri System\n")
    print("Reading details Configuration File")
    
    # 1. Can we connect to the ArcGIS Portal or AGOL 

        # Read Configuration File
        # This is the configuration file that has all connection info for the script to run correctly
        # Create the config parser object to store all the connection information for AGOL

    config_dir = cm.get_config_path()
    
    config = cm.load_configuration(config_dir)
    print("##########################################################")
    print('1. Testing to connect to the ArcGIS Enterprise ')
    print("Pulling information from the configureation file")
    print("##########################################################")
    
    print(f"configuration file location:\n{config_dir}")
    print("Querying Content from ArcGIS")
    arcgis_org_url = config.get('ArcGIS Credentials', 'arcgis_org_url')
    username = config.get('ArcGIS Credentials', 'username')
    password = config.get('ArcGIS Credentials', 'password')
    folder_name = config.get('Test Folder', 'folder')
    csv_path = config.get('Test Folder', 'csv_path')
    layer_title = config.get('Test Folder', 'csv_layer')
    sample_item = config.get('ArcGIS Items', 'test_item')
    
    print("Creating the GIS Object to connect to the instance of ArcGIS")
    print("##########################################################")

    gis = cm.connect(org_url=arcgis_org_url, login_name=username, user_password=password)
    status = gis.properties.portalName
    print(f'The connected system is an: {status} ')

    if status == 'ArcGIS Online': 
        print(f'We are skipping steps 2 and 3 due to the instance being {status}.')


    # 2. Can we connect to ArcGIS Server
    # 3. Can we connect to the web adaptors for portal and server
    


    # 4. Pull a gis item into a dataframe and create a feature set from this item
   
    itm = sample_item
    sample_itm = cm.get_gis_item(itm, gis)
    sample_lyr = sample_itm.layers[0]
    sample_fs = sample_lyr.query()
    sample_df = sample_lyr.query(as_df=True)

    # 5. We need to be able to create a folder and delete a folder in the users content

    
    print("##########################################################")
    print("5. Creating a folder that will be deleted in step 6\n")
    cm.create_folder_in_ags(gis, folder_name)

    print("##########################################################")
    # 6. We need to be able to publish an excel as a hosted feature service
    print("##########################################################")
    print("6. Creating a layer in the hosted server from a csv that is stored locally\n")
    cm.create_layer_in_test_folder(gis, csv_path, folder_name, layer_title)


    # delete folder:
    cm.delete_folder_in_args(gis, folder_name)

    print("##########################################################")
    # 7. We need to be able to publish a shapefile as a hosted feature service

    


    # 8. We need to be able to pull down these files and edit the content and push back our edits
    print('Pulling a feature layer into a dataframe removing all the content and adding new content')


    # 9. We need to be able to run a geometry query on this data and produce a new layer in the enterprise based on this query
    
    
    # 10. We need to be able to create new users
    

    print("Completed all necessary steps")

# Processing Steps to check the health of the system
if __name__ == "__main__":
    main()