import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ems.ems_mod import ems as ems_loc
from ems.ems_mod import ems_write
from ems.ems_mod import update_time_data
from ems.devices.devices import devices

from forecast.fcst import load_data
from forecast.price_fcst import get_elect_price_fcst

from ems.optim.opt_test import run_opt as opt
from ems.optim.optimize_EV_charging import create_ev_model

from pyomo.opt import SolverFactory
# import flex devices modules
from ems.flex.flex_ev import calc_flex_ev
from ems.plot.flex_draw import plot_flex as plot

# Read home availabilities from file
veh_availability = pd.read_csv('data/chts_veh_availability.csv')
rtp_price_forecast = pd.read_hdf('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV/Input-Data/RTP/rtp_15min_201802010000-201903010000.h5', key='df')

# Total number of home availabilities with trips conducted before and afterwards
n_avail = len(veh_availability)
n_veh = len(veh_availability['vehID'].unique())

mil2km_conversion = 1.61            # Miles to kilometer conversion rate
electr_consumption_per_km = 0.2     # electricity consumption per km (e.g. 0.2 equals 20kWh/100km

# load the predefined ems data, initialization by user input is also possible:
my_ems = ems_loc(initialize=True, path='data/test_Nr_01.txt')
my_ems = ems_loc(initialize=True, path='data/ev_ems_sa_constant_price_incl_error.txt')

# Counter for keeping track of insufficient time differences
t_insufficient_count = 0

# Create a list of result ems
results = list()

# Go through all vehicle availabilities
# for i in range(0, 10):
for i in range(len(veh_availability)):
    # Ceil arrival time to next quarter hour
    t_arrival_ceiled = pd.Timestamp(veh_availability['t_arrival'][i]).ceil(freq='15Min')
    # Floor departure time to previous quarter hour
    t_departure_floored = pd.Timestamp(veh_availability['t_departure'][i]).floor(freq='15Min')
    # Check whether time between ceiled arrival and floored departure time are at least two time steps
    if t_arrival_ceiled >= t_departure_floored:
        print('### Time is not sufficient for timestep:', i, '###')
        t_insufficient_count += 1
        continue

    # change the time interval
    my_ems['time_data']['t_inval'] = 15
    my_ems['time_data']['d_inval'] = 15
    my_ems['time_data']['start_time'] = t_arrival_ceiled.strftime('%Y-%m-%d %H:%M')
    my_ems['time_data']['end_time'] = t_departure_floored.strftime('%Y-%m-%d %H:%M')
    my_ems['time_data']['days'] = 1
    my_ems.update(update_time_data(my_ems))

    # Get price forecast for given time period
    price_fcst = get_elect_price_fcst(t_start=t_arrival_ceiled, t_end=t_departure_floored, pr_constant=0.19)
    price_fcst.insert(value=rtp_price_forecast['price'].loc[t_arrival_ceiled:t_departure_floored], loc=0, column='RTP')

    # Update forecast data
    my_ems['fcst']['ele_price_in'] = price_fcst['RTP'].to_list()
    my_ems['fcst']['ele_price_out'] = len(price_fcst) * [0]
    my_ems['fcst']['gas'] = len(price_fcst) * [0]
    my_ems['fcst']['last_elec'] = len(price_fcst) * [0]
    my_ems['fcst']['last_heat'] = len(price_fcst) * [0]
    my_ems['fcst']['temp'] = len(price_fcst) * [0]
    my_ems['fcst']['solar'] = len(price_fcst) * [0]

    # Update EV parameters
    my_ems['devices'].update(devices(device_name='ev', minpow=0, maxpow=11,
                                     stocap=round(veh_availability['d_travelled'][i]*mil2km_conversion*electr_consumption_per_km),
                                     init_soc=[0], end_soc=[100], eta=0.98,
                                     ev_aval=[my_ems['time_data']['start_time'], my_ems['time_data']['end_time']],
                                     timesetting=my_ems['time_data']))

    # calculate the timetable for all the devices
    my_ems['optplan'] = opt(my_ems, plot_fig=False, result_folder='data/')

    # Calculate ev flexibility
    my_ems['flexopts']['ev'] = calc_flex_ev(my_ems)

    # Plot flex result
    # plot(my_ems, 'ev')

    # Save results to files
    #results.append(my_ems)
    ems_write(my_ems, path='C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV/Results/RTP/ev_avail_' + str(i) + '.txt')
