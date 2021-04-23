import glob
import os
from utils import *
import pandas as pd

processed_data_path = '/nfs/turbo/midas-applied-ds/Data/Processed'

def append_accel_info(path):
  trip = pd.read_csv(path)
  f = accel_functor()
  trip['Acceleration[mph/s]'] = trip.apply(lambda df : f(df['Vehicle Speed[km/h]'], df['Timestamp(ms)']), axis=1)
  f = open(path, 'w')
  trip.to_csv(path)

def append_dist_info(path):
  trip = pd.read_csv(path)
  f = distance_functor()
  trip['Distance[km]'] = trip.apply(lambda df : f(df['Latitude[deg]'], df['Longitude[deg]']), axis=1)
  f = open(path, 'w')
  trip.to_csv(path)

def append_fuel_info(path):
  trip = pd.read_csv(path)
  VehID = trip['VehId'].iloc[0]
  static_ICE_data = pd.read_csv('VED_Static_Data_PHEV_EV.csv')
  displacement = static_ICE_data.loc[static_ICE_data['VehId']==VehID, 'Engine Configuration & Displacement']
  
  displacement = displacement.unique()[0]
  displacement = re.findall(r"\d.\d", displacement)
  trip['Fuel Rate [L/km'] = fuel_algo(trip, displacement)
  f = open(path, 'w')
  trip.to_csv(path)

paths = glob.glob(os.path.join(processed_data_path, 'HEV_trips', '*.csv'))

for i, path in enumerate(paths):
  if i % 1000 == 0:
    print(f'{i} of {len(paths)}')
  try: 
    append_dist_info(path)
  except Exception as e:
    print(f'error opening {path}')
    print(e)
    raise Exception

paths = glob.glob(os.path.join(processed_data_path, 'PHEV_trips', '*.csv'))

for i, path in enumerate(paths):
  if i % 1000 == 0:
    print(f'{i} of {len(paths)}')
  try: 
    append_dist_info(path)
  except Exception as e:
    print(f'error opening {path}')
    print(e)
    raise Exception

