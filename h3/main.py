from common import common as cm
import warnings
warnings.filterwarnings('ignore')
import time


def main():
    runner_start_time = time.time()
    
    hex_dictionary = cm.get_hex_grid_info(34.82,-116.46,7)
    print(hex_dictionary)
    print("##########################################################\n")
    
    hex_grid = cm.create_hex_grid(35.02,-116.36,8,10)
    #print(len(hex_grid))
    #print(hex_grid.head()
    print("##########################################################\n")
    cm.create_shapefile(hex_grid,"C:\Working","Cali1.shp")
    print("##########################################################\n")
    
    cm.create_hex_csv(hex_grid,"C:\Working","Cali1.csv" )
    print("##########################################################\n")
    
    
if __name__ == "__main__":
    main()