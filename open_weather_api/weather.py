# import urllib library
from urllib.request import urlopen
  
# import json
import json

def weatherAPIPull(lat,long):
  base_url = 'https://api.weatherapi.com/v1/current.json?key='
  api_key = '8664fdd71ee74cc5b6d220917222107'
  spacer_1 = '&q='
  lat = str(lat)
  long = str(long)
  spacer2 = ','
  spacer3 ='&aqi=no'
  weather_api_url = base_url + api_key + spacer_1 + lat + spacer2 + long + spacer3
  response = urlopen(weather_api_url)
  #read the json file into a new variable
  response_json = json.loads(response.read())
  feels_like = response_json['current']['feelslike_f']
  return feels_like

