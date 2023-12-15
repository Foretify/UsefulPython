import arcgis_helpers
from arcgis.gis import GIS
from optional import optional

arcgis_org_url="https://foretify.maps.arcgis.com"
username= "foretify_proton"
password='Zion2023!!'
item_id = '3ea418d655e74ec6a147f1bbcc588d52'
gis = GIS(arcgis_org_url, username, password, verify_cert=False)

arcgis_helpers.connect(arcgis_org_url,username,password)
arcgis_helpers.get_gis_item(item_id, gis)
