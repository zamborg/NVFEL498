import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

from pandas.core.reshape.concat import concat
from utils import group_into_trips, group_by_engine_type



raw_data_path = '/nfs/turbo/midas-applied-ds/Data/Raw/VED/'
processed_data_path = '/nfs/turbo/midas-applied-ds/Data/Processed'

def distance_functor():
    '''
    Return a function object that, when called with a vehicle's coordinates (Latitude, Longitude in degrees), computes the distance
    traveled based on the coordinates of the current timestamp and the parameters from the previous call to the function.
    
    Calulcates distance using Haversine Formula
    '''
    
    prev_lat = None
    prev_long = None
    
    def wrapped(lat, long):
        nonlocal prev_lat, prev_long
        dist = None
        if prev_lat is not None and prev_long is not None:
            dist = haversine_distance(prev_lat, prev_long, lat, long)
            
        prev_lat = lat
        prev_long = long
        return dist
    return wrapped