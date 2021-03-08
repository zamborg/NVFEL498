import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

from pandas.core.reshape.concat import concat
from utils import group_into_trips, group_by_engine_type

ICE_trips = group_into_trips(ICEs)
HEV_trips = group_into_trips(HEVs)
PHEV_trips = group_into_trips(PHEVs)
BEV_trips = group_into_trips(BEVs)

raw_data_path = '/nfs/turbo/midas-applied-ds/Data/Raw/VED/'
processed_data_path = '/nfs/turbo/midas-applied-ds/Data/Processed'
ICE_HEV = pd.read_csv(os.path.join(raw_data_path, 'VED_Static_Data_ICE_HEV.csv'))
PHEV_BEV = pd.read_csv(os.path.join(raw_data_path, 'VED_Static_Data_PHEV_EV.csv'))
static = pd.concat([ICE_HEV, PHEV_BEV])

paths = glob.glob(os.path.join(raw_data_path, '*.csv'))
df = pd.concat((pd.read_csv(f) for f in paths))

ICEs, HEVs, PHEVs, BEVs = group_by_engine_type(static, df)
ICE_trips = group_into_trips(ICEs)
HEV_trips = group_into_trips(HEVs)
PHEV_trips = group_into_trips(PHEVs)
BEV_trips = group_into_trips(BEVs)

for i, trip in enumerate(ICE_trips):
    path = os.path.join(processed_data_path, 'ICE_trips', f'ICE_trip{i}.csv')
    f = open(path, 'w')
    trip.to_csv(f)

for i, trip in enumerate(HEV_trips):
    path = os.path.join(processed_data_path, 'HEV_trips', f'HEV_trip{i}.csv')
    f = open(path, 'w')
    trip.to_csv(f)

for i, trip in enumerate(PHEV_trips):
    path = os.path.join(processed_data_path, 'PHEV_trips', f'PHEV_trip{i}.csv')
    f = open(path, 'w')
    trip.to_csv(f)

for i, trip in enumerate(BEV_trips):
    path = os.path.join(processed_data_path, 'BEV_trips', f'BEV_trip{i}.csv')
    f = open(path, 'w')
    trip.to_csv(f)