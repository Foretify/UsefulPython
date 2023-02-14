import os
import arcpy
from arcpy import env
from pathlib import Path


folder_path = str(Path(__file__).parent)
geo_database_name = "Titan_IM_.gdb"
geo_database = folder_path + '/' + geo_database_name


if arcpy.Exists(geo_database):
    print("The geodatabase already exists moving on to the next step")
else: 
    print('Creating the geo database')
    arcpy.CreateFileGDB_management(folder_path, geo_database_name)

im_dict = { 'hpt_targets1'   : ['targets',"POINT","HPT"],
            'hvt_targets'   : ['targets',"POINT","HVT"],
            'known_entity'   : ['entity',"POINT","Known"],
            'unknown_entity'   : ['entity',"POINT","Unknown"],
            'units_template'   : ['template',"POINT","Templated Units"],
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
            'sensor_track'   : ['fmv',"POINT","Sensor Track"],
            'sensor_footprint'   : ['fmv',"POLYLINE","Sensor Footprint"],
            

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
        print(f"The feature data set {out_name} already exists moving on to the next step")
    else: 
        print(f'Creating the feature set:  {out_name}')
        
        # Execute Create Feature dataset 
        arcpy.CreateFeatureDataset_management(geo_database, out_name, sr)
    if arcpy.Exists(folder_path + "/" + geo_database_name +"/" + out_name + "/" + feature_service_name):
        print(f"The feature class {feature_service_name} already exists moving on to the next step")
    else: 
        print(f'Creating the feature class: {feature_service_name}')

        arcpy.management.CreateFeatureclass(folder_path + "/" + geo_database_name +"/" + out_name, feature_service_name,geom_type,"","","","","","","","",feature_service_alias) 
print(f'Finished creating the geodata base information model')



