import os
import glob
from tqdm import tqdm
import pandas as pd

HOME_DIR = '/home/aysola'
RAW_DATA_PATH = os.path.join(HOME_DIR, 'midas-applied-ds/Data/Raw/VED/')
RAW_PATHS = sorted(glob.glob(os.path.join(RAW_DATA_PATH, '*.csv')))

def extract_trip_info(paths, func, df=True, name='values'):
    """
    Paths is a list of paths that point to VED csv files
    func is a functor that grabs pertinent info from the slice of the csv. EG:
        func = lambda x: x['Vehicle Speed[km/h]'].sum()/len(x)
        
    func needs to take a dataframe as an input, the output of func is returned for each slice of the dataset in a dictionary with `Trip` as the keys and func output as the values.
    
    if df -> output is returned as a dataframe instead of a dict.
    name: name for column output of func in dataframe
    """
    
    return_dict = {}
    
    for path in tqdm(paths):
        data = pd.read_csv(path)
        for trip in data['Trip'].value_counts().index:
            return_dict[trip] = func(data[data['Trip']==trip])
                
    if df is True:
        return_dict = pd.DataFrame({'Trip':list(return_dict.keys()), name:list(return_dict.values())})
        
    return return_dict
    
    
def extract_trip_multifunc(paths, funcs:list, names:list, df=True):
    """
    This is the exact same function as extract_trip_info but with several functions concatted 
    
    names must be equally as long as funcs
    returns either dict or dataframe
    """
    
    results = {name:[] for name in names}
    results['Trip'] = []
    
    for path in tqdm(paths):
        data = pd.read_csv(path)
        for trip in data['Trip'].value_counts().index:
            results['Trip'].append(trip)
            for func, name in zip(funcs, names):
                results[name].append(func(data[data['Trip']==trip]))
    if df:
        return pd.DataFrame(results)
    return results

class NaChecker():
    def __init__(self, colname):
        self.colname = colname
        
    def __call__(self, x):
        return x[self.colname].isna().sum()/len(x)

ave_speed_func = lambda x:x['Vehicle Speed[km/h]'].mean()
max_speed_func = lambda x:x['Vehicle Speed[km/h]'].max()
