import pandas as pd
import numpy as np

features = [
    'Aggressiveness',
    'Weight',
    'Displacement',
    'Air Temperature[F]',
    'Precipitation Level[mm]',
    'SpeedAverage',
    'Aggressiveness*SpeedAverage',
    'Aggressiveness*Weight',
    'Aggressiveness*Displacement',
    'Displacement/Weight'
]

def transform_data(data, features, out = 'Fuel Rate[gpm]'):
    d = pd.DataFrame(columns = features)
    
    for f in features:
        if '*' in f:
            f1, f2 = f.split('*')
            d[f] = data[f1] * data[f2]
        elif '/' in f:
            f1, f2 = f.split('/')
            d[f] = data[f1] / data[f2]
        else:
            d[f] = data[f]
            
    return np.array(d), np.array(data[out]), {f:i for i,f in enumerate(features)}

def generate_trip_data(**kwargs):
    """
    kwargs:
        size = # of trips
        num_vehicles = # of vehicles
        prop_ICE = proportion of ICE vehicles
        prop_HEV = proportion of HEV
        prop_PHEV = prop of PHEV
        trips: DICT with trip characteristics as tuples
        cars: DICT with vehicle characteristics as tuples
    
    """
    size = kwargs['size']
    num_vehicles = kwargs['num_vehicles']
    
    #TODO: figure out how to deal with these
    # PRESENTLY Vehicle Type DEFAULTS TO ICE
#     prop_ICE = kwargs['prop_ICE']
#     prop_HEV = kwargs['prop_HEV']
#     prop_PHEV =kwargs['prop_PHEV']
    
    #DEFAULT TRIP AND CARS
    trips = {
        'Air Temp (units)':(0,0),
        'Precipitation (units)':(0,0),
        'Average Speed (units)':(0,0),
        'Speed Variance (units)':(0,0),
        'Distance (units)':(0,0)
            }
    
    cars = {
        'Weight (units)':(0,0),
        'Displacement (units)':(0,0),
            }
    #OVERWRITING DEAFAULTS
    
    for k,v in kwargs['trips'].items():
        trips[k] = v
    for k,v in kwargs['cars'].items():
        cars[k] = v
        
    
    car_keys = cars.keys()
    trip_keys = trips.keys()
    
    data = {k:[] for k in trips.keys()}
    for k in cars.keys():
        data[k] = []
    data['Vehicle Type'] = []
    
    
    vehicles = {k:np.random.normal(v[0], v[1], size=num_vehicles) for k,v in cars.items()}
    vehicles = [{k:v[i] for k,v in vehicles.items()} for i in range(num_vehicles)]
    vehicle_mask = np.random.randint(0, num_vehicles, size)
    
    trips = {k:np.random.normal(v[0], v[1], size) for k,v in trips.items()}
    trips = [{k:v[i] for k,v in trips.items()} for i in range(size)]
    
    # data has all the keys we just need to append for each value:
    for i, veh in enumerate(vehicle_mask):
        for k in trip_keys:
            data[k].append(trips[i][k])
        for k in car_keys:
            data[k].append(vehicles[veh][k])
            
        data['Vehicle Type'].append('ICE')
            
    return pd.DataFrame(data)

#fleet_cols = ['Hybridization', 'Weight (units)', 'Displacement (units)', 'Aggressiveness Percentile',
#                 'Average Speed (units)', 'Speed Variance (units)', 'Air Temperature (units)',
#                 'Precipitation Level (units)', 'Distance (units)']
class ManualFleet():
    def __init__(self, col_names:list = ['Vehicle ID', 'Hybridization', 'Weight (units)', 'Displacement (units)', 'Aggressiveness Percentile',
                 'Average Speed (units)', 'Speed Variance (units)', 'Air Temperature (units)',
                 'Precipitation Level (units)', 'Distance (units)']):
        # set default data to nothing
        self.data = pd.DataFrame({l:[] for l in col_names})
        
    def reset(self):
        self.data = pd.DataFrame({l:[] for l in self.data.columns}).reset_index(drop=True)
    
    def update(self, data:dict):
        """
        Data has:
        'Air Temp'
        'Precipitation'
        'Average Speed'
        'Speed Variance'
        'Distance'
        'Weight'
        'Displacement'
        'Vehicle Type'
        """
        self.data = pd.concat([self.data, pd.DataFrame(data)])
        return self.data
    def show(self):
        return self.data
    
