import h3
from shapely.geometry import Polygon, Point
import shapely.wkt
import pandas as pd
import geopandas as gpd
import warnings
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
        
        #"parent" : h3.h3_to_parent(h3_id), 
        #"children" : h3.h3_to_children(h3_id)
    }
# start with a grid coordainte and a number of rings
def create_hex_grids(lat: int, long: int, resolution: int, number_of_rings:int):
    rings = {}
    count = 0
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