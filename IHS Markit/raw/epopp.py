import pandas as pd
from requests.auth import HTTPBasicAuth
import requests
import json
from pandas import ExcelWriter

import os


arcpy.env.overwriteOutput = True
uname = 'lwright@esri.com'
pword = 'C0nn3ct1!'
url = 'https://api.connect.ihsmarkit.com/risk/v2/country-risk/epop/location-risk?'
Latitude = '35'
Longitude = '-117'

def flatten_dict(dd, separator ='_', prefix =''): 
    return { prefix + separator + k if prefix else k : v 
             for kk, vv in dd.items() 
             for k, v in flatten_dict(vv, separator, kk).items() 
             } if isinstance(dd, dict) else { prefix : dd } 


def get_eppop_score(x,y, username, password): 
    epop_url = 'https://api.connect.ihsmarkit.com/risk/v2/country-risk/epop/location-risk?' + 'lat=' + Latitude + '&' + 'lng=' + Longitude
    response = requests.get(epop_url, auth=HTTPBasicAuth(username, password))
    text_response = json.loads(response.text)
    flatten_dic = flatten_dict(text_response)
    print(flatten_dic)
    epopp_df = pd.DataFrame([flatten_dic]) 
    slash = '\\'
    cp = os. getcwd()
    current = os.path.realpath(__file__)
    filepath = cp+ slash + 'epop.csv'
    print(current)
    print(filepath)

    epopp_df.to_csv(filepath, index = False)
    #epopp_df.to_csv(r'C:\Users\topow\OneDrive\Desktop\Esri\IHS Markit\scripts\New folder\epop.csv', index = False)
    #arcpy.TableToTable_conversion(r"C:\Users\topow\OneDrive\Desktop\Esri\IHS Markit\scripts\New folder\epop.csv", "C:\Esri\LocationData\GeneralData.gdb", "epop")
    return epopp_df

inputs = ('a','y','username','password')
eppop_one = get_eppop_score(Latitude, Longitude, uname,pword)
print("Latitude:  " + eppop_one.loc[0,"Location_Latitude"])
print("Longitude: " + eppop_one.loc[0,"Location_Longitude"])
print("Combined Risk:  " + str(eppop_one.loc[0,"Risk_Combined"]))
print("Civil Unrest: " + str(eppop_one.loc[0,"Risk_CivilUnrest"]))
print("War Risk: "  + str(eppop_one.loc[0,"Risk_War"]))
print("Terrorism Risk: "  + str(eppop_one.loc[0,"Risk_Terrorism"]))
print("Combined Risk: "  + str(eppop_one.loc[0,"Risk_Combined"]))


