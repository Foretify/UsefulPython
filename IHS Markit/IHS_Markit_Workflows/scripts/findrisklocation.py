from arcgis.gis import GIS
from requests.auth import HTTPBasicAuth
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from arcgis.features import GeoAccessor
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import getpass, requests, json



#AGOL Account Information
agol_username = 'enter username'
agol_password = 'enter password'
agol_org_url = r'enter ArcGIS enterprise or AGOL'

#IHS Markit Account Information
ihs_username = 'enter username'
ihs_password = 'enter password'


#Assets Layer being read into for risk analysis
input_asset_layer = "enter asset layer"

#Risk Table for IHS Data
risk_table = "enter risk table"

gis = GIS(agol_org_url, agol_username, agol_password)
print("Successfully logged in to ArcGIS as: " + gis.properties.user.username)


#Pull out the information from the feature layer
asset_item = gis.content.get(input_asset_layer)
asset_lyr = item.layers[0]



#Pull out the information from the feature table
risk_table_item = gis.content.get(risk_table)
risk_gis_table = risk_table_item.tables[0]

# Functions
def get_gis_item(item_id, gis):

    item = gis.content.get(item_id)

    if not item:
        raise Exception(f'Input Item ID Not Found in GIS: {item_id}')
    else:
        return item
    
    
def add(lyr, sdf, id_field):

        incoming_ids = sdf[id_field].tolist()
        existing_ids = [f.attributes[id_field] for f in lyr.query().features]
        new_item_ids = list(set(incoming_ids).difference(set(existing_ids)))

        add_features = sdf[sdf[id_field].isin(new_item_ids)]

        if len(add_features) > 0:
            res = lyr.edit_features(adds=add_features.spatial.to_featureset())['addResults']
            return len([i for i in res if i['success']])
        else:
            return 0
        
        
def batch_it(l, n):

    for i in range(0, len(l), n):
        yield l[i:i + n]

def flatten_dict(dd, separator ='_', prefix =''): 
    """
        Returns a flat dictionary 
    """
    return { prefix + separator + k if prefix else k : v 
            for kk, vv in dd.items() 
            for k, v in flatten_dict(vv, separator, kk).items() 
            } if isinstance(dd, dict) else { prefix : dd } 



# create a Spatially Enabled DataFrame object for assets
sdf = pd.DataFrame.spatial.from_layer(asset_lyr)
output = pd.DataFrame()
log_df = pd.DataFrame( 
        columns = ['Location_Latitude',
                    'Risk_War',
                    'Asset_ID',
                   ])
for col in log_df.columns: 
    print(col)
locations_df = sdf[['Asset_ID','Longitude','Latitude']]    


risk_list = []
print('--------------------------------------------------------------')
print('Starting to retrieve risk')
print('--------------------------------------------------------------')
for row in locations_df.itertuples():
    x = str(row[2])
    y = str(row[3])
    site_id = str(row[1])
    #print(x)
    #print(y)
    #print(site_id)
    
   

    epop_url = 'https://api.connect.ihsmarkit.com/risk/v2/country-risk/epop/location-risk?' + 'lat=' + y + '&' + 'lng=' + x
    response = requests.get(epop_url, auth=HTTPBasicAuth(ihs_username, ihs_password))
    text_response = json.loads(response.text)

   
    flatten_dic = flatten_dict(text_response)
    flatten_dic['Asset_ID']=site_id
    output = output.append(flatten_dic, ignore_index=True)

#Update risk table in ArcGIS
print('--------------------------------------------------------------')
print('Updating feature table')
res = risk_gis_table.edit_features(adds = output, rollback_on_failure=False )['addResults']

print('Table update is complete')
print('--------------------------------------------------------------')



