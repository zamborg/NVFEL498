import glob
import os
from utils import *
import pandas as pd

processed_data_path = '/nfs/turbo/midas-applied-ds/Data/Processed'
paths = glob.glob(os.path.join(processed_data_path, 'ICE_trips', '*.csv'))
alltrips_path = os.path.join(processed_data_path, 'ICE_trips', 'alltrips.csv')

df = pd.read_csv(alltrips_path)

for i in range(17739):
  if i % 1000 == 0:
    print(i)
  path = os.path.join(processed_data_path, 'ICE_trips', f'ICE_trip{i}.csv')
  trip = pd.read_csv(path)
  '''
  pf = aggressivity(trip)
  pke = aggressiveness(trip)
  d['TripId'].append(i)
  d['Aggressivity'].append(pf)
  d['Aggressiveness'].append(pke)
  '''
  fuel_comp = trip['Fuel Consumption[km/L]']
  distance = trip['Distance[km]']
  temp_f = []
  final_f = []
  final_d = []
  for i in range(len(distance)):
    d = distance[i]
    f = fuel_comp[i]
    if d == 0 or pd.isna(d) and not pd.isna(f):
      temp_f.append(f)
    else:
      final_f.append(np.array(temp_f).mean())
      temp_f = []
      final_d.append(d)
  total_d = np.sum(np.array(final_d))
  total_fuel = 1/np.sum(np.array(final_f) / np.array(final_d))
  print(total_fuel, total_d, 1.6* total_d / .26* total_fuel)

df = pd.DataFrame(d)
f = open(alltrips_path)
df.to_csv(f)
  
  
  
