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


    # 1. Can we connect to the ArcGIS Portal or AGOL @topowright

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


    # 2. Can we connect to ArcGIS Server
    # 3. Can we connect to the web adaptors for portal and server
    # 4. We need to understand the user type and permissions of the user
    # 5. We need to be able to create a folder and delete a folder in the users content

        # create folder:
    me = gis.users.me
    user_folders = (me.folders)    
    folder_name = config.get('ArcGIS Online Test Folder', 'folder')
    folder_list = [i['title'] for i in user_folders]
    if folder_name not in folder_list:
        print(f"There is no folder named:  {folder_name}; it will now be created. ")
        gis.content.create_folder(folder_name)
        print(f'{folder_name} was created.')
    elif folder_name in folder_list:
        print(f"The folder: {folder_name} already exists and was not created.")

        # delete folder:
    me = gis.users.me
    user_folders = (me.folders)    
    folder_name = config.get('ArcGIS Online Test Folder', 'folder')
    folder_list = [i['title'] for i in user_folders]
    if folder_name in folder_list:
        print(f"The test folder:  {folder_name} exists and will now be deleted")
        gis.content.delete_folder(folder_name)
        print(f'The folder:  {folder_name} was deleted.')
    elif folder_name not in folder_list:
        print(f'The folder:  {folder_name} does not exist.')


    # 6. We need to be able to publish a shapefile as a hosted feature service


    # 7. We need to be able to publish an excel as a hosted feature service
    # 8. We need to be able to pull down these files and edit the content and push back our edits
    # 9. We need to be able to run a geometry query on this data and produce a new layer in the enterprise based on this query
    # 10. We need to be able to create new users
    # let us create a built-in account with username: demo_user1 with org_user privilege
    demo_user1 = gis.users.create(username = 'demo_user1',
                                password = '0286eb9ac01f',
                                firstname = 'demo',
                                lastname = 'user',
                                email = 'python@esri.com',
                                description = 'Demonstrating how to create users using ArcGIS Python API',
                                role = 'org_user',
                                level = 2,
                                user_type = 'creatorUT',
                                provider = 'arcgis')
    demo_user1_role = demo_user1
    print(type(demo_user1_role))
    print(demo_user1_role)                                
    


    

    print("Completed all necessary steps")

# Processing Steps to check the health of the system
if __name__ == "__main__":
    main()