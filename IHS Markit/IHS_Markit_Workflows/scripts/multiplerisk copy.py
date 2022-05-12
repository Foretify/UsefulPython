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
ihs_username = 'lwright@esri.com'
ihs_password = 'C0nn3ct1!'
multi_location_risk_url = 'https://api.connect.ihsmarkit.com/risk/v3/country-risk/epop/multi-location-risk'





json = {
  "Locations": [
    [41.0, 41.1],    [42.2, 42.3],    [43.4, 43.5],    [44.6, 44.7],    [45.8, 45.9],
    [46.0, 46.1],    [47.2, 47.3],    [48.4, 48.5],    [49.6, 49.7],    [50.8, 50.9]
  ]
}
response = requests.post(multi_location_risk_url, auth=HTTPBasicAuth(ihs_username, ihs_password), json=json)

#Loop through a feature class and select a 1000 records and create a new DF of that query



print("Status code: ", response.status_code)
print("Printing Entire Post Request")
print(risk_value= response.json())


