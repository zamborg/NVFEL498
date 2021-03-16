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
  trip['Distance[km]'] = get_distances(trip)
  f = open(path, 'w')
  trip.to_csv(path)

def append_fuel_info(path):
  trip = pd.read_csv(path)
  VehID = trip['VehId'].iloc[0]
  static_ICE_data = pd.read_csv('../VED_Static_Data_ICE_HEV.csv')
  trip['Fuel Consumption[km/L]'] = fuel_algo(trip, static_ICE_data)
  f = open(path, 'w')
  trip.to_csv(path)

paths = glob.glob(os.path.join(processed_data_path, 'ICE_trips', '*.csv'))
for i, path in enumerate(paths):
  if i % 1000 == 0:
    print(i)
  try:
    append_dist_info(path)
  except Exception as e:
    print(f'error opening {path}')
    print(e)
