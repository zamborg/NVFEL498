import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

from pandas.core.reshape.concat import concat
from utils import group_into_trips, group_by_engine_type



raw_data_path = '/nfs/turbo/midas-applied-ds/Data/Raw/VED/'
processed_data_path = '/nfs/turbo/midas-applied-ds/Data/Processed'
ICE_HEV = pd.read_csv('../VED_Static_Data_ICE_HEV.csv')
PHEV_BEV = pd.read_csv('../VED_Static_Data_PHEV_EV.csv')
static = pd.concat([ICE_HEV, PHEV_BEV])

paths = glob.glob(os.path.join(raw_data_path, '*.csv'))

entries = set()
w = 0
x = 0
y = 0
z = 0

def write_trip(trip, prefix, i):
  trip_id = trip['Trip'].unique()[0]
  veh_id = trip['VehId'].unique()[0]
  entry = (trip_id, veh_id)
  if entry in entries:
    print('error: duplicate trips across files')
    assert(False)
  path = os.path.join(processed_data_path, f'{prefix}_trips', f'{prefix}_trip{i}.csv')
  f = open(path, 'w')
  trip.to_csv(f)

def write_trips(path, w, x, y, z):
  df = pd.read_csv(path)
  ICEs, HEVs, PHEVs, BEVs = group_by_engine_type(static, df)
  print(len(PHEVs))
  ICE_trips = group_into_trips(ICEs)
  HEV_trips = group_into_trips(HEVs)
  PHEV_trips = group_into_trips(PHEVs)
  BEV_trips = group_into_trips(BEVs)
  '''
  for trip in ICE_trips:
    write_trip(trip, 'ICE', w)
    w += 1

  for trip in HEV_trips:
    write_trip(trip, 'HEV', x)
    x += 1
  '''
  for i, trip in enumerate(PHEV_trips):
    print(f'PHEV trip {i}')
    write_trip(trip, 'PHEV', y)
    y += 1

  for trip in BEV_trips:
    write_trip(trip, 'BEV', z)
    z += 1
  return w, x, y, z

for i, path in enumerate(paths):
  print(f'processing path {i} of {len(paths)}')
  w, x, y, z = write_trips(path, w, x, y, z)
