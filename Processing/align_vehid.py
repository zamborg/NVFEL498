import pandas as pd
import numpy as np

trip_data_path = '/nfs/turbo/midas-applied-ds/Data/Processed/ICE_trips/alltrips2.csv'
static_data_path = '/nfs/turbo/midas-applied-ds/Project/NVFEL498/VED_Static_Data_ICE_HEV.csv'
temp_data_path = '/nfs/turbo/midas-applied-ds/Data/Processed/ICE_trips/alltrips_with_weight_and_disp.csv'

static_df = pd.read_csv(static_data_path)
trips = pd.read_csv(trip_data_path)
ICEs = static_df[static_df['Vehicle Type'] == 'ICE']

weights = []
displacements = []
d = dict(trips)

for vid in trips['VehId']:
  row = static_df.loc[static_df['VehId'] == vid]
  try:
    weight = int(row['Generalized_Weight'])
    weights.append(weight)
  except Exception as e:
    print(e)
    weights.append(np.nan)
  disp_str = row['Engine Configuration & Displacement']
  try:
    disp = disp_str.str.extract(r'(\d\.\d)')
    displacements.append(disp)
  except Exception as e:
    print(e)
    displacements.append(np.nan)

d['Weight'] = weights
d['Displacement'] = displacements
df = pd.DataFrame(d)
f = open(temp_data_path, 'w')
df.to_csv(f)

