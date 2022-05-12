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
agol_password = ''
agol_org_url = r""



json = {
  "Locations": [
    [41.0, 41.1],    [42.2, 42.3],    [43.4, 43.5],    [44.6, 44.7],    [45.8, 45.9],
    [46.0, 46.1],    [47.2, 47.3],    [48.4, 48.5],    [49.6, 49.7],    [50.8, 50.9]
  ]
}
response = requests.post(multi_location_risk_url, auth=HTTPBasicAuth(ihs_username, ihs_password), json=json)

#Loop through a feature class and select a 1000 records and create a new DF of that query

{'Locations': [['-84.3403308429999', '33.8595021740001'], ['-118.542429965', '34.201197517'], ['-87.630833684', '41.881616546'], ['-77.410900935', '38.9508075210001'], ['-117.161062665', '32.714130675'], ['-122.170053709', '37.442789475'], ['-122.677668654', '45.5185718870001'], ['-122.229504775', '38.0953396740001'], ['-73.96993436', '40.7896069280001']]}

print("Status code: ", response.status_code)
print("Printing Entire Post Request")
risk_value= response.json()


