# Name: CreateFeatureDataset_Example2.py
# Description: Create a feature dataset 

# Import system modules
import arcpy


""" # Set local variables
out_dataset_path = "C:/output/HabitatAnalysis.gdb" 
out_name = "analysisresults"

# Create a spatial reference object
sr = arcpy.SpatialReference("C:/data/studyarea.prj")

# Create a FileGDB for the fds
arcpy.CreateFileGDB_management("C:/output", "HabitatAnalysis.gdb")

# Execute CreateFeaturedataset 
arcpy.CreateFeatureDataset_management(out_dataset_path, out_name, sr) """