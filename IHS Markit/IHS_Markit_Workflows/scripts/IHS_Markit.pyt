# -*- coding: utf-8 -*-
import pandas as pd
from requests.auth import HTTPBasicAuth
import requests
import json
import arcpy
import os


arcpy.env.overwriteOutput = True
uname = ''
pword = ''
        
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "EPOP Area Score"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Enter a Lattitude",
            name="Lattitude",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=False
        )
        param1 = arcpy.Parameter(
            displayName="Enter a Longitutde",
            name="Longitutde",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=False
        )
        param2 = arcpy.Parameter(
            displayName="Enter a folder",
            name="Output_Folder",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
            multiValue=False
        )
        param3 = arcpy.Parameter(
            displayName="Table Name",
            name="Output_Table",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=False
        )
       
        params = [param0, param1,param2, param3]
        return params


    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
      

        def flatten_dict(dd, separator ='_', prefix =''): 
            """
                Returns a flat dictionary 
            """
            return { prefix + separator + k if prefix else k : v 
                    for kk, vv in dd.items() 
                    for k, v in flatten_dict(vv, separator, kk).items() 
                    } if isinstance(dd, dict) else { prefix : dd } 


        def get_eppop_score(x,y, username, password,filepath): 
            """
                The inputs are dd coordiantes and the username password for IHS Markit's API
                The output is a pandas dataframe that allows a user to understand the risk score at a location. Areas are captured every 500 meters

            """
            # retrive the epop score and cread dataframe with scores
            epop_url = 'https://api.connect.ihsmarkit.com/risk/v2/country-risk/epop/location-risk?' + 'lat=' + x + '&' + 'lng=' + y
            response = requests.get(epop_url, auth=HTTPBasicAuth(username, password))
            text_response = json.loads(response.text)
            flatten_dic = flatten_dict(text_response)
            epopp_df = pd.DataFrame([flatten_dic]) 

            # File path
            slash = '\\'
            #cp = os. getcwd()
            #current = os.path.realpath(__file__)

            csv = filepath + slash + 'epop.csv'
            geodatabase = filepath + slash + "results.gdb"

            epopp_df.to_csv(csv, index = False)
            arcpy.TableToTable_conversion(csv, geodatabase, "epop")
            return epopp_df
        
        
        eppop_one = get_eppop_score(parameters[0].valueAsText, parameters[1].valueAsText,uname,pword,parameters[2].valueAsText)
        arcpy.AddMessage("Starting epopp score")
        arcpy.AddMessage(eppop_one)

        arcpy.AddMessage('Lattitude entered: ' + parameters[0].valueAsText)
        arcpy.AddMessage('Longitutde entered: ' + parameters[1].valueAsText)
        arcpy.AddMessage("Finished  epopp score")
        
        arcpy.AddMessage("The results: ")
        arcpy.AddMessage("=================")
        arcpy.AddMessage("Latitude:  " + str(eppop_one.loc[0,"Location_Latitude"]))
        arcpy.AddMessage("Longitude: " + str(eppop_one.loc[0,"Location_Longitude"]))
        arcpy.AddMessage("Combined Risk:  " + str(eppop_one.loc[0,"Risk_Combined"]))
        arcpy.AddMessage("Civil Unrest: " + str(eppop_one.loc[0,"Risk_CivilUnrest"]))
        arcpy.AddMessage("War Risk: "  + str(eppop_one.loc[0,"Risk_War"]))
        arcpy.AddMessage("Terrorism Risk: "  + str(eppop_one.loc[0,"Risk_Terrorism"]))
        arcpy.AddMessage("Combined Risk: "  + str(eppop_one.loc[0,"Risk_Combined"]))
        arcpy.AddMessage("=================")
            
    


