import glob
import os
from utils import aggressivity, aggressiveness
import pandas as pd
import numpy as np

paths = ['sample_processed_trip.csv']

num_trips = 17737
l = []

d = {
  'TripId' : [],
  'TripId_raw' : [], 
  'VehId' : [],
  'Aggressivity' : [],
  'Aggressiveness' : [],
  'Distance[km]' : [],
  'Fuel Consumed[L]' : [],
  'Fuel Rate[gpm]' : [],
}

def nacheck(x):
  return pd.isna(x) or np.isinf(x) or x == 0

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
    print(pke)
    total_d = np.sum(distance)
    total_fuel = np.sum(distance / fuel_comp)
    
    raw_trip_ids = trip['Trip'].unique()
    assert(len(raw_trip_ids) == 1)
    raw_veh_ids = trip['VehId'].unique()
    assert(len(raw_trip_ids) == 1)

    if nacheck(total_fuel) or nacheck(total_d) or nacheck(pke):
      continue


    d['TripId'].append(i)
    d['TripId_raw'].append(raw_trip_ids[0])
    d['VehId'].append(raw_veh_ids[0])
    d['Aggressivity'].append(pf)
    d['Aggressiveness'].append(pke)
    d['Distance[km]'].append(total_d)
    d['Fuel Consumed[L]'].append(total_fuel)
    d['Fuel Rate[gpm]'].append(total_fuel / total_d)
  except Exception as e:
    print(f'Error opening file {i}')
    print(e)
    l.append(np.nan)
  '''
  '''

df = pd.DataFrame(d)
f = open(alltrips_path, 'w')
df.to_csv(f)
  
