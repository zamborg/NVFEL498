import pandas as pd
import numpy as np
import utils


trips = pd.read_csv('../alltrips_final.csv')
norm1 = []
norm2 = []

for i, row in trips.iterrows():
  if i % 1000 == 0:
    print(i)
  try:
    tripId = str(int(row['TripId']))
    fname = f'/nfs/turbo/midas-applied-ds/Data/Processed/ICE_trips/ICE_trip{tripId}.csv'
    trip = pd.read_csv(fname)
    norm1.append(utils.normalized_aggressiveness1(trip))
    norm2.append(utils.normalized_aggressiveness2(trip))
  except Exception as e:
    print(f'failed reading file {i}')
    print(e)

trips['Normalized PKE 1'] = np.array(norm1)
trips['Normalized PKE 2'] = np.array(norm2)

with open('../alltrips_final2.csv', 'w') as f:
  trips.to_csv(f)
