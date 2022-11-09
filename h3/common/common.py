import h3
from shapely.geometry import Polygon, Point
import shapely.wkt
import pandas as pd
import geopandas as gpd
import warnings
import os
warnings.filterwarnings('ignore')

def get_hex_grid_info(lat: int, long: int, resolution: int):
    '''
    Given a lat long and a hex grid resolution scale we are able to create a hex grid, which 
    outputs as a dictionary.
    '''
    h3_id = h3.geo_to_h3(lat=lat,lng=long,resolution=resolution)
    return {
       #"input coords": [lat, long, resolution]
       #"hash_simple": h3_id,
       "index": 0,
       "hash": h3.geo_to_h3(lat=lat,lng=long,resolution=resolution),
       "lat" : h3.h3_to_geo(h3_id)[0], 
       "long" : h3.h3_to_geo(h3_id)[1], 
       "center_coords" : h3.h3_to_geo(h3_id), 
       "geometry" : Polygon(h3.h3_to_geo_boundary(h3_id, geo_json=True)), 

    }
# start with a grid coordainte and a number of rings
def create_hex_grids(lat: int, long: int, resolution: int, number_of_rings:int):
    rings = {}
    count = 1
    ring_count = 0
    
    print(f'using the following coordinate {lat}, {long} with a resolution of: {resolution}')
    a = get_hex_grid_info(lat, long, resolution)
    #print(a)
    final_gpd = gpd.GeoDataFrame(a, geometry='geometry', crs ="EPSG:4326")
    final_gpd = final_gpd.drop(1)
    #print(final_gpd.head())
           
    h3_id = a['hash']
    print(h3_id)
    
    while count != number_of_rings:
        ring = h3.k_ring(h3_id,count)
        #print(ring)
        
        print(f' we are looking at the following nearest {count}')
        count = count + 1
        for i in ring:
            #print(i)
            ring_count = ring_count + 1
            coordinates = h3.h3_to_geo(i)
            
           
            hexs = get_hex_grid_info(coordinates[0], coordinates[1], resolution)
           
            hexs_gpd = gpd.GeoDataFrame(hexs, geometry='geometry', crs ="EPSG:4326")
            hexs_gpd = hexs_gpd.drop(1)
            final_gpd= hexs_gpd.append(hexs_gpd)
            
            
    print(ring_count)
    return final_gpd
def create_shapefile(dataframe: str ,filepath: str ,filename: str):

    completeName = os.path.join(filepath, filename)
    print(completeName)
    print("reading the dataframe into the model")
    dataframe = dataframe
    dataframe.to_file(filename= completeName, driver='ESRI Shapefile')
    print(f"shapefile has been created in the following directory: {completeName}")
    
def create_hex_csv(dataframe: str ,filepath: str ,filename: str):

    completeName = os.path.join(filepath, filename)
    print(completeName)
    print("reading the dataframe into the model")
    dataframe.to_csv(completeName) 
    print(f"CSV has been created in the following directory: {completeName}")


def create_hex_grid(lat:int,lng:int,resloution:int,rings:int):
    '''
    Creates a hex grids in a geodataframe from a given location the resloution of the grid 
    desired and the number of rings from the starting hex grid
    
    inputs: 
    lat = lattitude 
    lng = longitutde
    resloution = the scale fo the hex grid
    rings = number of rings desired from the center hex grid
    
    '''
    center_hex = get_hex_grid_info(lat,lng,resloution)
    ring = h3.k_ring(center_hex['hash'],rings)
    hex_output=gpd.GeoDataFrame(center_hex, geometry='geometry', crs ="EPSG:4326")
    hex_output = hex_output.drop(1)
    for i in ring:
        coordinates = h3.h3_to_geo(i)
        hex = get_hex_grid_info(coordinates[0],coordinates[1],resloution)
        hex_gdf = gpd.GeoDataFrame(hex, geometry='geometry', crs ="EPSG:4326")
        hex_gdf = hex_gdf.drop(1)
        hex_output = hex_output.append(hex_gdf)
    return hex_output