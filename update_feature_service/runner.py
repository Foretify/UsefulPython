import arcgis_helpers
from arcgis.gis import GIS
from optional import optional

arcgis_org_url="https://foretify.maps.arcgis.com"
username= "foretify_proton"
password='Zion2023!!'
item_id = '0ee6d6073b374d4d88756351d3aba465'
gis = GIS(arcgis_org_url, username, password, verify_cert=False)

arcgis_helpers.connect(arcgis_org_url,username,password)
arcgis_helpers.get_gis_item(item_id, gis)
