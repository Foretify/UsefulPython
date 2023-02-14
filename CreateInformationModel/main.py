import arcpy
import os
import os
import configparser
from pathlib import Path

folder_path = str(Path(__file__).parent)
geo_database_name = "fGDB.gdb"
geo_database = folder_path + '/' + geo_database_name


if arcpy.Exists(geo_database):
    print("The geodatabase already exists moving on to the next step")
else: 
    print('Creating the geo database')
    arcpy.CreateFileGDB_management(folder_path, geo_database_name)

im_dict = { 'hpt_targets'   : ['targets',"POINT","HPT"],
            'hvt_targets'   : ['targets',"POINT","HVT"],
            'known_entity'   : ['entity',"POINT","Known"],
            'unknown_entity'   : ['entity',"POINT","Unknown"],
            'point_gmti'   : ['gmti',"POINT","Point"],
            'track_gmti'   : ['gmti',"POINT","Track"],
            'to_gmti'   : ['gmti',"POLYGON","Tessellated Overlay"],
            'ellipse'   : ['elint',"POLYGON"," Ellipse"],
            'convolved_point_elint' : ['elint','POLYGON','Convolved Points'],
            'overlay_polygon_elint' : ['elint','POLYGON','Overlay Polygons'],
            'point_bda'   : ['bda',"POINT","BDA Point"],
            'line_bda'   : ['bda',"POLYLINE","BDA Line"],
            'polygon_bda'   : ['bda',"POLYGON","BDA Polygon"],
            'units_ops_graphics'   : ['ops_graphics',"POINT","Units"],
            'points_ops_graphics'   : ['ops_graphics',"POINT","Points"],
            'lines_ops_graphics'   : ['ops_graphics',"POLYLINE","Lines"],
            'polygons_ops_graphics'   : ['ops_graphics',"POLYGON","Polygons"],
            'units_intel_graphics'   : ['intel_graphics',"POINT","Units"],
            'points_intel_graphics'   : ['intel_graphics',"POINT","Points"],
            'lines_intel_graphics'   : ['intel_graphics',"POLYLINE","Lines"],
            'polygons_intel_graphics'   : ['intel_graphics',"POLYGON","Polygons"],
            'spot_reports'   : ['reports',"POINT","BDA Line"],

}
for key, value in im_dict.items():
    feature_service_name = key
    feature_set_name = value[0]
    geom_type = value[1]
    feature_service_alias = value[2]


    # Set local variables
    out_dataset_path = folder_path + "/" + geo_database_name
    out_name = feature_set_name

    # Create a spatial reference object
    sr = arcpy.SpatialReference(folder_path + "/" + "WGS1984WorldMercator.prj")


    if arcpy.Exists(geo_database + "/" + out_name):
        print("The featureset already exists moving on to the next step")
    else: 
        print('Creating the feature set')
        
        # Execute Create Feature dataset 
        arcpy.CreateFeatureDataset_management(geo_database, out_name, sr)

    arcpy.management.CreateFeatureclass(folder_path + "/" + geo_database_name +"/" + out_name, feature_service_name,geom_type,"","","","","","","","",feature_service_alias) 
