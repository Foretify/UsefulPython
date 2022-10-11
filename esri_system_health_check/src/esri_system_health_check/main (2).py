from cProfile import run
import sys
import time
import os
import pandas as pd
from datetime import date
from esri_system_health_check.common.common import *
#from traveladvisories.common.schema import *
#from esri_system_health_check.util.webscrape import scrape_page
#from esri_system_health_check.validation import GISAuthenticationException, QueryingLayerException


def main():
    # Set initial runtime.  This reference time will be used to measure runtime performance. 
    runner_start_time = time.time()
    print(runner_start_time)



    try:
        # Read Configuration File
        # This is the configuration file that has all connection info for the script to 
        # run ie layers from AGOL and connection parameters
        # Create the config parser object to store all the connection information for AGOL
        print("Reading Configuration File")
        print("Reading in details from configuration file")
        config_dir = common.get_config_path()
        config = common.load_configuration(config_dir)

        

        # 
        print("Querying Content from ArcGIS")
        arcgis_org_url = config.get('ArcGIS Credentials', 'arcgis_org_url')
        username = config.get('ArcGIS Credentials', 'username')
        password = config.get('ArcGIS Credentials', 'password')

        gis = common.connect(org_url=arcgis_org_url, login_name=username, user_password=password)
# Processing Steps to bring the state department data into our layer in Foretify
if __name__ == "__main__":
    main()