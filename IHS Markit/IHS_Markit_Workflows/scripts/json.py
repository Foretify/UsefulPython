from arcgis.gis import GIS
from requests.auth import HTTPBasicAuth
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from arcgis.features import GeoAccessor
from datetime import datetime, timedelta
import pandas as pd
import requests
import numpy as np
import getpass
import json
import requests


#Log in information for IHS Markit
ihs_username = ''
ihs_password = ''
multi_location_risk_url = 'https://api.connect.ihsmarkit.com/risk/v3/country-risk/epop/multi-location-risk'

#Log in information for AGOL
agol_username = ""
agol_password = ""
agol_org_url = r""

gis = GIS(agol_org_url, agol_username, agol_password)
print("Successfully logged in as: " + gis.properties.user.username)

input_risk_layer = "232b504be0914279ad8a143edd77360c"
item = gis.content.get(input_risk_layer)
table = item.layers[0]
lyr = item.layers[0]

# create a Spatially Enabled DataFrame of given locations of interest
sdf = pd.DataFrame.spatial.from_layer(lyr)
# Start a counter
count = 0
#Create an empty list to store locations
locations= []
# Create a payload to pass locations to 
payload={}

locations_df = sdf[['Site_ID','POINT_X', 'POINT_Y']]
print('Starting to retrieve risk')
for row in locations_df.itertuples():
    x = row[2]
    y = row[3]
    site_id = str(row[1])
    pos = count = count +1
    locations.append([y,x])
    


payload["Locations"] = locations
print("Here is the payload")
print(payload)

response = requests.post(multi_location_risk_url, auth=HTTPBasicAuth(ihs_username, ihs_password), json=payload)

print("Status code: ", response.status_code)
print("Printing Entire Post Request")
risk_value= response.json()
print("-----------------------------")
print(risk_value[0])