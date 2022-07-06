### Importing necessary libaries 
import sys
import csv
import os.path
import datetime
import pandas as pd

# import urllib library
from urllib.request import urlopen
  
# import json
import json

def myfunction(lattitude , longitude, weather_type):
  '''
  This is a function that allows a user to input a set of coordinates and the type of forcast they desire to return
  infomation about inputted location. The options are: 
  1. Get current weather
  2. Get a general forcast for the near future
  3. Get the current tempature and entire hourly forcast for the near future
  '''

  if weather_type == 1:
    print("User slected current weather")  
    return current_tempature = 
  if weather_type == 2:
    print("")  
  if weather_type == 3:
    print("")  