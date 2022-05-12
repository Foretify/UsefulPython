import pandas as pd
from requests.auth import HTTPBasicAuth
import requests
import json
from pandas import ExcelWriter
import arcpy

username = 'lwright@esri.com'
password = 'C0nn3ct1!'
url = 'https://api.connect.ihsmarkit.com/risk/v2/country-risk/epop/location-risk?'
Latitude = '34.0442'
Longitude = '-117.24'


epop_url = 'https://api.connect.ihsmarkit.com/risk/v2/country-risk/epop/location-risk?' + 'lat=' + Latitude + '&' + 'lng=' + Longitude
response = requests.get(epop_url, auth=HTTPBasicAuth(username, password))
print(epop_url)
print(response)
text_response = json.loads(response.text)


print(text_response)





