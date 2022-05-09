import os
import pandas as pd


#input file names to compare

#Input the list of cities
#filename = 'filename'
american_cities = 'cities.csv'
covered_cities = 'covered_cities.csv'


##Functions
##

#create the path for the csv file
def createCSVPath(filename):
    path = os.path.abspath('')
    csv_path = path + "/" + filename
    return csv_path

#mycsv = createCSVPath(american_cities)
american_cities_path = createCSVPath(american_cities)
covered_cities_path = createCSVPath(covered_cities)

# Read the csv file from local directory into a pandas dataframe:
#df = pd.read_csv(mycsv)
#print("The csv that is being read into AGOL is: " + mycsv)
#print(df)

american_cities_df = pd.read_csv(american_cities_path)
#print("The csv that is being read into AGOL is: " + american_cities_path)
#print(american_cities_df)
#
covered_cities_df = pd.read_csv(covered_cities_path)
#print("The csv that is being read into AGOL is: " + covered_cities_path)
#print(covered_cities_df)

cities = []
covered = []
for index, row in american_cities_df.iterrows():
    city = row["City"]
    print (row["City"])
    for index, row in covered_cities_df.iterrows():
        covered_city = row["City"]
        covered.append(covered_city)