from common import common as cm
import time


def main():
    runner_start_time = time.time()
    print("##########################################################\n")
    hex_dictionary = cm.get_hex_grid_info(28.32,55.46,7)
    print(hex_dictionary)
    
    hex_grid = cm.create_hex_grids(25.32,55.46,7,3)
    #print(len(hex_grid))
    #print(hex_grid.head()
    
    
    
if __name__ == "__main__":
    main()