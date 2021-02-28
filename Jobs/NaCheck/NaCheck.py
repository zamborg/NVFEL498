import sys
import os
import pandas

HOME_DIR = '/home/aysola/'

sys.path.append(os.path.join(HOME_DIR, 'NVFEL498'))

from Notebooks.utils import *

na_check_names = ['DayNum',
 'VehId',
 'Timestamp(ms)',
 'Latitude[deg]',
 'Longitude[deg]',
 'Vehicle Speed[km/h]',
 'MAF[g/sec]',
 'Engine RPM[RPM]',
 'Absolute Load[%]',
 'OAT[DegC]',
 'Fuel Rate[L/hr]',
 'Air Conditioning Power[kW]',
 'Air Conditioning Power[Watts]',
 'Heater Power[Watts]',
 'HV Battery Current[A]',
 'HV Battery SOC[%]',
 'HV Battery Voltage[V]',
 'Short Term Fuel Trim Bank 1[%]',
 'Short Term Fuel Trim Bank 2[%]',
 'Long Term Fuel Trim Bank 1[%]',
 'Long Term Fuel Trim Bank 2[%]']

na_check_funcs = [NaChecker(name) for name in na_check_names]

NA_DF = extract_trip_multifunc(RAW_PATHS, na_check_funcs, na_check_names)

NA_DF.to_csv(os.path.join('./NA_Percent.csv'))
