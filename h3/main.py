from common import common as cm
import warnings
warnings.filterwarnings('ignore')
import time


def main():
    runner_start_time = time.time()
    
    hex_dictionary = cm.get_hex_grid_info(28.32,55.46,7)
    print(hex_dictionary)
    print("##########################################################\n")
    
    hex_grid = cm.create_hex_grid(25.32,55.46,7,3)
    #print(len(hex_grid))
    #print(hex_grid.head()
    print("##########################################################\n")
    cm.create_shapefile(hex_grid,"C:\Working","final.shp")
    print("##########################################################\n")
    
    cm.create_hex_csv(hex_grid,"C:\Working","final.csv" )
    print("##########################################################\n")
    
    
if __name__ == "__main__":
    main()