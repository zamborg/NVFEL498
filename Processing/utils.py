import pandas as pd
import numpy as np
import re

def group_by_engine_type(static_df, timeseries_df, ignore_diesel=True, ignore_turbocharged=True):
    ICEs = static_df[static_df['Vehicle Type'] == 'ICE']
    HEVs = static_df[static_df['Vehicle Type'] == 'HEV']
    PHEVs = static_df[static_df['EngineType'] == 'PHEV']
    BEVs = static_df[static_df['EngineType'] == 'BEV']

    if ignore_diesel:
        ICEs = ICEs[~ICEs['Engine Configuration & Displacement'].str.contains('DSL')]
    if ignore_turbocharged:
        ICEs = ICEs[~ICEs['Engine Configuration & Displacement'].str.contains('T/C')]

    ICE_timeseries = pd.merge(ICEs, timeseries_df, on ='VehId')
    HEV_timeseries = pd.merge(HEVs, timeseries_df, on='VehId')
    PHEV_timeseries = pd.merge(PHEVs, timeseries_df, on='VehId')
    BEV_timeseries = pd.merge(BEVs, timeseries_df, on='VehId')

    return ICE_timeseries, HEV_timeseries, PHEV_timeseries, BEV_timeseries

def group_into_trips(timeseries):
    '''
    Given a Pandas df representing timeseries data, create an array of Pandas df for each unique trip.
    
    Input: a Pandas DataFrame
    Output: a list of Pandas DataFrame objects

    Note: Different trip IDs sometimes corresponded to more than one VehId, implying that they aren't unique.
    For this reason, we split on both the 'Trip' column AND the 'VehId' column
    '''
    trips = []
    for trip_id in timeseries['Trip'].unique():
        trip_timeseries = timeseries[timeseries['Trip'] == trip_id]

        for veh_id in trip_timeseries['VehId'].unique():
            trip_timeseries_split_by_vehicle = trip_timeseries[trip_timeseries['VehId'] == veh_id]
            trips.append(trip_timeseries_split_by_vehicle)

    return trips

def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   return np.round(res, 20)

def distance_functor():
    '''
    Return a function object that, when called with a vehicle's velocity in km/h and a current timestamp in ms, 
    computes the distance traveled in the time interval.
    '''
    
    prev_t = None

    def wrapped(v, t):
        nonlocal prev_t
        dist = None
        if prev_t is not None:
            delta_t = (t - prev_t) / 1000 / 3600
            dist = v * delta_t
        else:
          dist = 0
            
        prev_t = t
        return dist
    return wrapped

def get_distances2(trip):
    '''
    Given a trip in a Pandas DataFrame, return a Pandas Series that contains distance traveled for each datapoint in the trip.
    Distance is in km.
    '''
    f = distance_functor()
    return trip.apply(lambda df : f(df['Vehicle Speed[km/h]'], df['Timestamp(ms)']), axis=1)

def get_distances(trip):
    t = np.array(trip['Timestamp(ms)'])
   
    helpme = t[1:] - t[:-1]
    delta_t = np.append(np.array([0]), t[1:] - t[:-1]) / 1000 / 3600
    return delta_t * trip['Vehicle Speed[km/h]']


def accel_functor():
    '''
    Return a function object that, when called with a vehicle's velocity (in km/h) 
    and a timestamp (in ms), computes the acceleration of the vehicle (in mph/s)
    based on the velocity and time of the given parameters and the parameters from
    the previous call to the function.

    The reason for the units of mph/s is for compatibility with the power factor
    formula as presented in the following paper:
    https://silo.tips/download/a-comparison-of-real-world-and-modeled-emissions-under-conditions-of-variable-dr


    This is very convenient to use with Pandas Series objects.
    For example (where trip is a DataFrame representing a trip):
    f = accel_functor()
    a = trip.apply(lambda df : f(df['Vehicle Speed[km/h]'], df['Timestamp(ms)']), axis=1)
    '''
    unit_conversion = 621.371 # from kph / ms to mph / s

    prev_v = None
    prev_t = None
    def wrapped(v, t):
        nonlocal prev_v, prev_t
        a = None
        if prev_v is not None and prev_t is not None:
            delta_v = v - prev_v # in km/h
            delta_t = t - prev_t # in ms

            a = delta_v / delta_t * unit_conversion
        prev_v = v
        prev_t = t
        return a
    return wrapped

def get_accel2(trip):
    '''
    Given a trip as a Pandas DataFrame, return a Pandas Series that contains acceleration 
    data for the vehicle (in mph/s) on that trip.

    The reason for the units of mph/s is for compatibility with the power factor
    formula as presented in the following paper:
    https://silo.tips/download/a-comparison-of-real-world-and-modeled-emissions-under-conditions-of-variable-dr
    '''
    f = accel_functor()
    return trip.apply(lambda df : f(df['Vehicle Speed[km/h]'], df['Timestamp(ms)']), axis=1)

def get_accel(trip):
    unit_conversion = 621.371 # from kph / ms to mph / s
    t = np.array(trip['Timestamp(ms)'])
    v = np.array(trip['Vehicle Speed[km/h]'])
    delta_t = np.append(np.array([0]), t[1:] - t[:-1])
    delta_v = np.append(np.array([0]), v[1:] - v[:-1])
    out = np.append(np.array([0]), delta_v[1:] / delta_t[1:]) * unit_conversion
    return out

def get_power_factors(trip):
    '''
    Given a trip as a Pandas DataFrame and acceleration as a Pandas Series, return power
    factor data for the trip as a Pandas Series.
    '''
    return trip.apply(lambda df : 2 * df['Vehicle Speed[km/h]'] * get_accel(df), axis=1)

def aggressivity(trip):
    '''
    Given a trip as a Pandas DataFrame, return the aggressivity of the trip.
    '''
    power_factors = get_power_factors(trip)
    return np.sqrt(np.sum(power_factors ** 2) / len(power_factors))

def pke(d, v, a):
    begin_accel = None
    end_accel = None
    total = 0
    for i in range(len(a)):
        if a[i] > 0:
            if begin_accel is None:
                begin_accel = i - 1
        else:
            end_accel = i - 1
            if begin_accel is not None:
                
                pke_segment = v[end_accel] ** 2 - v[begin_accel] ** 2
                assert(pke_segment > 0)

                total += pke_segment
                begin_accel = None

    if begin_accel is not None and begin_accel < len(a) - 1:
        pke_segment = v[len(a) - 1] ** 2 - v[begin_accel] ** 2
        total += pke_segment
    
    return total / np.sum(d)

def normalized_pke1(d, v, a):
    begin_accel = None
    end_accel = None
    total = 0
    count = 0
    for i in range(len(a)):
        if a[i] > 0:
            if begin_accel is None:
                begin_accel = i - 1
        else:
            end_accel = i - 1
            if begin_accel is not None:
                
                pke_segment = v[end_accel] ** 2 - v[begin_accel] ** 2
                assert(pke_segment > 0)

                total += pke_segment
                count += 1
                begin_accel = None

    if begin_accel is not None and begin_accel < len(a) - 1:
        pke_segment = v[len(a) - 1] ** 2 - v[begin_accel] ** 2
        total += pke_segment
        count += 1
    
    return total / np.sum(d) / count

def normalized_pke2(d, v, a):
    begin_accel = None
    end_accel = None
    total = 0
    for i in range(len(a)):
        if a[i] > 0:
            if begin_accel is None:
                begin_accel = i - 1
        else:
            end_accel = i - 1
            if begin_accel is not None:
                
                pke_segment = v[end_accel] ** 2 - v[begin_accel] ** 2
                assert(pke_segment > 0)

                total += pke_segment
                begin_accel = None

    if begin_accel is not None and begin_accel < len(a) - 1:
        pke_segment = v[len(a) - 1] ** 2 - v[begin_accel] ** 2
        total += pke_segment
    
    return total / np.sum(d) / len(a)

def aggressiveness(trip):
    d = get_distances(trip)
    v = trip['Vehicle Speed[km/h]']
    a = get_accel(trip)
    a[0] = 0
    return pke(d, v, a)

def normalized_aggressiveness1(trip):
    d = get_distances(trip)
    v = trip['Vehicle Speed[km/h]']
    a = get_accel(trip)
    return normalized_pke1(d, v, a)

def normalized_aggressiveness2(trip):
    d = get_distances(trip)
    v = trip['Vehicle Speed[km/h]']
    a = get_accel(trip)
    return normalized_pke2(d, v, a)


def fuel_algo(x, displacement):
    # first do everything for MAF non NA
    # then for all MAF NA values, do absLoad calculation
    # Because NA denom or numer => NAN => NA in both => NAN
    sec_hour = 3600
    air_to_fuel = 14.7
    fuel_density = 820
    
    out = pd.DataFrame(np.zeros(shape=(len(x))))
    
    maf_screen = np.array(x['MAF[g/sec]'].isna()).reshape(-1,1)
    maf = x[maf_screen]['MAF[g/sec]']
    fuel_flow = (maf*sec_hour)/(air_to_fuel*fuel_density)
    out[maf_screen] = list(1/(fuel_flow/x[maf_screen]['Vehicle Speed[km/h]']))
    
    absLoad = x[~maf_screen]['Absolute Load[%]']
    RPM = x[~maf_screen]['Engine RPM[RPM]']
    fuel_flow = x[~maf_screen]['MAF[g/sec]']
    displacement = float(displacement[0].strip("L"))
    maf = 1.84 * displacement * absLoad/100 * RPM/2/60
    fuel_flow[~maf_screen] = list((maf*sec_hour)/(air_to_fuel*fuel_density)) #update out where MAF is NAN
    print(out.shape)
    tmp = ~maf_screen
    print(tmp.shape)
    out[~maf_screen] = list(1/(fuel_flow/x[~maf_screen]['Vehicle Speed[km/h]']))

    out.replace(float('inf'), 0, inplace=True)
    
    return pd.Series(out.iloc[:,0])


def get_fuel(trip, disp):
    f = fuel_algo(trip, disp)
    d = get_distances(trip)
    return np.sum(f * d)
