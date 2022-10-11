from cProfile import run
import sys
import time
import os
import pandas as pd
from datetime import date
from common import common

def main():
    runner_start_time = time.time()
    print("Starting the process of checking the health of the Esri System\n")
    print(runner_start_time)


    # Read Configuration File
    # This is the configuration file that has all connection info for the script to 
    # run ie layers from AGOL and connection parameters
    # Create the config parser object to store all the connection information for AGOL

    print("Reading details Configuration File")
    
    config_dir = common.get_config_path()
    
    config = common.load_configuration(config_dir)
    print(f"configuration file location:\n{config_dir}")
    
   


    
    print("Querying Content from ArcGIS")
    arcgis_org_url = config.get('ArcGIS Credentials', 'arcgis_org_url')
    username = config.get('ArcGIS Credentials', 'username')
    password = config.get('ArcGIS Credentials', 'password')

    gis = common.connect(org_url=arcgis_org_url, login_name=username, user_password=password)

    print("Completed all necessary steps")

# Processing Steps to check the health of the system
if __name__ == "__main__":
    main()