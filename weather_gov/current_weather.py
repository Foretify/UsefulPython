### Importing necessary libaries 
from arcgis.features import GeoAccessor, summarize_data, FeatureLayer, analysis, Feature, FeatureSet
from arcgis.mapping import WebMap
import sys
import csv
import os.path
import datetime
import pandas as pd
from arcgis.gis import GIS
from datetime import datetime, timedelta
import pandas as pd
import requests
import numpy as np
import uuid

#### Functions needed for the script
def get_gis_item(item_id, gis):

    item = gis.content.get(item_id)

    if not item:
        raise Exception(f'Input Item ID Not Found in GIS: {item_id}')
    else:
        return item
    
    
def process_edits(feature_layer, data_frame, operation, batch_count=500):
    """
    Push edits from SDF to hosted feature layer.
    """

    print(f"Running {operation.upper()} on Hosted Feature Layer")

    # Chunk edits into lists of 500 items. Python API can only push so many updates; item sized based on bytes.
    update_sets = list(batch_it(data_frame.spatial.to_featureset().features, batch_count))

    for edits in update_sets:
        if operation == 'update':
            res = feature_layer.edit_features(updates=edits, rollback_on_failure=False)['updateResults']
            print(f"Updated {len([i for i in res if i['success']])} rows of {len(edits)}")
        else:
            res = feature_layer.edit_features(adds=edits, rollback_on_failure=False)['addResults']
            print(f"Added {len([i for i in res if i['success']])} rows of {len(edits)}")
def batch_it(l, n):

    for i in range(0, len(l), n):
        yield l[i:i + n]
        
#### Connection to AGOL
#### This is the information needed to connect to the AGOL instance
username = "analyst2022" #AGOL username
password = "ForetifyTillIDie2022!!" #AGOL password
gis = GIS("https://foretifydev.maps.arcgis.com", username, password)
print("Successfully logged in as: " + gis.properties.user.username)


# import urllib library
from urllib.request import urlopen
  
# import json
import json

def weatherByCoordiante(lattitude , longitude, weather_type):
  '''
  This is a function that allows a user to input a set of coordinates and the type of forcast they desire to return
  infomation about inputted location. The options are: 
  1. Get current weather will return a list that is formatted this [lattitude , longitude,current_tempature] 
  2. Get a general forcast for the near future
  3. Get the current tempature and entire hourly forcast for the near future
  '''
  #Build the url "https://api.weather.gov/points/39.7456,-116.0892"
  spacer = ','
  latitude = str(lattitude)
  longitude = str(longitude)
  weather_gov_url = 'https://api.weather.gov/points/'+  latitude + spacer + longitude
  weather_gov_url

  # store the response of URL which is in json 
  response = urlopen(weather_gov_url)
  #read the json file into a new variable
  data_json = json.loads(response.read())



  if weather_type == 1:
    print("User slected current weather") 
    # We capture the url to allow us to pull the current tempature. This is a url that is given to us in the
    # first response
    hourly_forcast_url= data_json["properties"]['forecastHourly']
    
    # store the response for the hourly forecast 
    hourly_response = urlopen(hourly_forcast_url)
    #read the json data into a new variable for hourly forcast
    hourly_data_json = json.loads(hourly_response.read())
    # Using the hourly data json content we can pull out the first item in the array and get the tempature
    current_tempature = hourly_data_json['properties']['periods'][0]['temperature']


     
    print(current_tempature)
    
    hourly_forcast_list = [lattitude , longitude,current_tempature]
    print(hourly_forcast_list)
    return hourly_forcast_list


  if weather_type == 2:
    print("")  
  if weather_type == 3:
    print("")  

location_data_list = weatherByCoordiante(35,-116,1)
print(location_data_list)

#Create a DataFrame object
location_data_df = pd.DataFrame(columns = ['lattitude' , 'longitude', 'temperature' ])
# using loc methods to update the data in the newly created dataframe object
location_data_df.loc[len(location_data_df)] = location_data_list
### Create a pandas df out of the list above
#location_data_df = pd.DataFrame(location_data_list)

location_data_sdf = GeoAccessor.from_xy(location_data_df,'longitude','lattitude')


#location_data_sdf = location_data_df.set_geometry(['longitude', 'latitude'])
print(len(location_data_df))


#Adding a point location layer from AGOL
target_layer_id ='ae140cced1fe42dea8227acb8ed47c92'
# Get item content for Facilities layer
target_layer_item = get_gis_item(target_layer_id, gis)
target_layer_lyr = target_layer_item.layers[0]

# Push udpates into the facilities layer.
process_edits(target_layer_lyr, location_data_sdf, 'add')
