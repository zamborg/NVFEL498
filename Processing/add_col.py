import glob
import os
from utils import *
import pandas as pd
import numpy as np

processed_data_path = '/nfs/turbo/midas-applied-ds/Data/Processed'
paths = glob.glob(os.path.join(processed_data_path, 'ICE_trips', 'ICE_trip*.csv'))
alltrips_path = os.path.join(processed_data_path, 'ICE_trips', 'alltrips.csv')
temp_alltrips_path = os.path.join(processed_data_path, 'ICE_trips', 'alltrips2.csv')

alltrips = pd.read_csv(alltrips_path)
d = dict(alltrips)
d['VehId'] = []

for i, path in enumerate(paths):
  if i % 1000 == 0:
    print(i)
  #path = os.path.join(processed_data_path, 'ICE_trips', f'ICE_trip{i}.csv')
  trip = pd.read_csv(path)
  vid = trip['VehId']
  tripid = trip['Trip'].iloc[0]
  print(d['TripId'].iloc[i])
  print(tripid)
  if tripid == d['TripId'].iloc[i]:
    print('found')  
    d['VehId'].append(vid)
  else:
      print('not found')
      continue

df = pd.DataFrame(d)
f = open(temp_alltrips_path, 'w')
df.to_csv(f)
  #except Exception as e:
  #  print(f'Error opening file {i}')
  #  print(e)

  
