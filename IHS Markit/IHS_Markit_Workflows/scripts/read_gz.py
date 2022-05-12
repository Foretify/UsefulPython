import gzip
import pandas as pd
from io import BytesIO

## Enter in a file path of a raw.gz file
filepath = r'C:\Program Files\Splunk\var\run\splunk\dispatch\1613753334.104\dump\DESKTOP-ECJBIG8\Badge Swipe.csv\MyExport.csv_9_0.raw.gz'


df = pd.DataFrame()

# A list that takes the content from the source file and prepares it for a dataframe
lines= []

#Write the file to a list
with gzip.open(filepath, 'rb') as f:

   for line in f:
       #Move data from bytes to strings
       item = line.decode('UTF-8').strip().split(',')
    
       lines.append(item)
       
       

print(lines[0])
df = df.append(lines, ignore_index=True)
print(df)





