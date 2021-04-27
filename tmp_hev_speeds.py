import glob
import os
import sys
import pandas as pd
import numpy as np
from tqdm import tqdm
import re

HOME_DIR = '/home/aysola/'

os.chdir(HOME_DIR)

sys.path.append('./NVFEL498/')

DATA_DIR = os.path.join(HOME_DIR, 'midas-applied-ds', 'Data', 'Processed', 'HEV_trips')

files = glob.glob(os.path.join(DATA_DIR, 'HEV*'))


# all_trips = pd.read_csv(os.path.join(HOME_DIR, 'NVFEL498', 'all_HEV_trips.csv'))
#alltrips for 500 HEVS
all_trips = pd.read_csv(os.path.join(HOME_DIR, 'NVFEL498', '500_HEV_trips.csv'))

def ave_velocity(trip):
    return trip['Vehicle Speed[km/h]'].mean()

def var_velocity(trip):
    return trip['Vehicle Speed[km/h]'].var()

def get_num(x):
    return int(re.search("\d+", os.path.basename(x)).group())

trip_numbers = [get_num(f) for f in files]

if len(trip_numbers) != len(files):
    raise Exception("tripnumbers should be the same length")
    
all_trips['SpeedAverage'] = np.NaN
all_trips['SpeedVariance'] = np.NaN

for i, file in tqdm(enumerate(files)):
    
    num = get_num(file)
    if num is None:
        raise Exception(f"File: {file} does not have a number in it")
    
    trip = pd.read_csv(file)
        
    all_trips.loc[all_trips['TripId_raw'] == num, 'SpeedAverage'] = ave_velocity(trip)
    all_trips.loc[all_trips['TripId_raw'] == num, 'SpeedVariance'] = var_velocity(trip)
    

all_trips.to_csv(os.path.join(HOME_DIR, 'NVFEL498', '500_HEV_trips_vel.csv'), index=False)