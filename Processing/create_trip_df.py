import glob
import os
from utils import *
import pandas as pd
import numpy as np

processed_data_path = '/nfs/turbo/midas-applied-ds/Data/Processed'
paths = glob.glob(os.path.join(processed_data_path, 'ICE_trips', 'ICE_trip*.csv'))
alltrips_path = os.path.join(processed_data_path, 'ICE_trips', 'alltrips.csv')

num_trips = 17737
l = []

d = {
  'TripId' : [],
  'Aggressivity' : [],
  'Aggressiveness' : [],
  'Fuel Consumed[L]' : [],
  'Distance[km]' : [],
}

for i, path in enumerate(paths):
  if i % 1000 == 0:
    print(i)
  #path = os.path.join(processed_data_path, 'ICE_trips', f'ICE_trip{i}.csv')
  try:
    trip = pd.read_csv(path)
    fuel_comp = trip['Fuel Consumption[km/L]']
    distance = trip['Distance[km]']
    
    pf = aggressivity(trip)
    pke = aggressiveness(trip)
    total_d = np.sum(distance)
    total_fuel = np.sum(distance / fuel_comp)
    
    d['TripId'].append(i)
    d['Aggressivity'].append(pf)
    d['Aggressiveness'].append(pke)
    d['Fuel Consumed[L]'].append(total_fuel)
    d['Distance[km]'].append(total_d)
  except Exception as e:
    print(f'Error opening file {i}')
    print(e)
    l.append(np.nan)
  '''
  '''

df = pd.DataFrame(d)
f = open(alltrips_path, 'w')
df.to_csv(f)
  
