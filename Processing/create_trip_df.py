import glob
import os
from utils import aggressivity, aggressiveness, get_fuel, get_distances
import pandas as pd
import numpy as np

paths = os.listdir('/nfs/turbo/midas-applied-ds/Data/Processed/HEV_trips/')
alltrips_path = ('/nfs/turbo/midas-applied-ds/Project/NVFEL498/all_HEV_trips.csv')

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

nonEVs = pd.read_csv('/nfs/turbo/midas-applied-ds/Project/NVFEL498/VED_Static_Data_ICE_HEV.csv')

def nacheck(x):
  return pd.isna(x) or np.isinf(x) or x == 0

for i, path in enumerate(paths):
  if i % 1000 == 0:
    print(i)
  path = os.path.join('/nfs/turbo/midas-applied-ds/Data/Processed/HEV_trips/', path)
  try:
    trip = pd.read_csv(path)
    distance = get_distances(trip)
    
    pf = aggressivity(trip)
    pke = aggressiveness(trip)
    print(pke)
    total_d = np.sum(distance)
    total_fuel = get_fuel(trip, nonEVs)
    
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
    d['Fuel Rate[gpm]'].append(total_fuel / total_d / 2.352)
  except Exception as e:
    print(f'Error opening file {i}')
    print(e)
    l.append(np.nan)
  '''
  '''

df = pd.DataFrame(d)
f = open(alltrips_path, 'w')
df.to_csv(f)
