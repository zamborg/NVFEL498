import pandas as pd
from utils import *


trip = pd.read_csv("ICE_trip7636.csv")
f = distance_functor()
trip['Distance[km]'] = trip.apply(lambda df : f(df['Latitude[deg]'], df['Longitude[deg]']), axis=1)
