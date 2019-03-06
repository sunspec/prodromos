# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 13:58:12 2019

@author: cwhanse

2019-2-19 jjohns2@sandia.gov: Updated with communication interfaces
"""

import pytz
from optimization.ce_api import CE_API
from optimization.feeder_class import Feeder
from forecasting.pv_system_class import PVobj
from optimization.dss_util import PFOptim
import numpy as np
import time
import os
import math
import csv

USMtn = pytz.timezone('US/Mountain')

username = "fake"
password = "fake"

# Create the Connected Energy API interface to get PV forecasts and issue DER PV setpoints
api = CE_API(username=username, password=password)

# Create dictionary of all PV systems and associated forecast information
pvdict = {}
use_surrogates = True
if use_surrogates:
    pvdict['sunpower2201'] = PVobj('sunpower2201', dc_capacity=1900, ac_capacity=3000, lat=35.05, lon=-106.54, alt=1657,
                                   tz=USMtn, tilt=35, azimuth=180, pf_max=0.85, pf_min=-0.85,
                                   forecast_method='persistence')

    pvdict['pvsy1'] = PVobj('1 MW Plant', dc_capacity=1000, ac_capacity=1000, lat=35.05, lon=-106.54, alt=1657,
                            tz=USMtn, tilt=35, azimuth=180, pf_max=0.85, pf_min=-0.85,
                            surrogateid='sunpower2201', forecast_method='persistence')

    pvdict['pvsy2'] = PVobj('10 MW Plant', dc_capacity=10000, ac_capacity=10000, lat=35.05, lon=-106.54, alt=1657,
                            tz=USMtn, tilt=35, azimuth=180, pf_max=0.85, pf_min=-0.85,
                            surrogateid='sunpower2201', forecast_method='persistence')

    pvdict['pvsy3'] = PVobj('258 kW Plant', dc_capacity=258, ac_capacity=258, lat=35.05, lon=-106.54, alt=1657,
                            tz=USMtn, tilt=35, azimuth=180, pf_max=0.85, pf_min=-0.85,
                            surrogateid='sunpower2201', forecast_method='persistence')
else:
    pvdict['pvsy1'] = PVobj('1 MW Plant', dc_capacity=1000, ac_capacity=1000, lat=35.05, lon=-106.54, alt=1657,
                            tz=USMtn, tilt=35, azimuth=180, pf_max=0.85, pf_min=-0.85,
                            forecast_method='persistence')

    pvdict['pvsy2'] = PVobj('10 MW Plant', dc_capacity=10000, ac_capacity=10000, lat=35.05, lon=-106.54, alt=1657,
                            tz=USMtn, tilt=35, azimuth=180, pf_max=0.85, pf_min=-0.85,
                            forecast_method='persistence')

    pvdict['pvsy3'] = PVobj('258 kW Plant', dc_capacity=258, ac_capacity=258, lat=35.05, lon=-106.54, alt=1657,
                            tz=USMtn, tilt=35, azimuth=180, pf_max=0.85, pf_min=-0.85,
                            forecast_method='persistence')

dss_to_phil_map = {'pvsy1': 'epri3', 'pvsy2': 'epri2', 'pvsy3': 'epri1'}

pvlist = list(pvdict.keys())

# Setup feeder object which points to the local OpenDSS time series simulation
feeder = Feeder(filename=os.getcwd() + "\\PNM_reduced_timeseries\\Master.DSS",
                pv=pvdict)

derlist = feeder.pv_on_feeder
loadlist = feeder.DSS.circuit.Loads.AllNames

if not (set(derlist) <= set(pvlist)):
    raise ValueError('OpenDSS PV system list not included in pvlist')

# Assume DER devices start at unity PF
curr_pf = {pv: 1.0 for pv in pvlist}

# stepsize hardcoded at 5m for now because that's the resolution of the PV forecasts
stepsize = '5m'

# Number of stepsize time periods that the optimization will be working over
periods = 3

# Results dataset
results_filename = os.getcwd() + ' Optimization %s.csv' % time.time()
csvfile = open(results_filename, 'x')
csvfile.write('Time (s), Power Factor DER 1, Power Factor DER 2, Power Factor DER 3, '
              'Reactive Power DER 1 (var), Reactive Power DER 2 (var), Reactive Power DER 3 (var), '
              'Optimization Function, PV Forecast, Power Forecast, Reactive Power Forecast\n')
csvfile.close()

sim_duration = 5.*60.*60.  # 5 hours (in seconds)
sec_per_loop = 60.0  # number of seconds between optimizations
n_iter = math.ceil(sim_duration/sec_per_loop)  # number of 5-minute optimizations
starttime = time.time()
for opt_loop in range(n_iter):

    print('#### Running Optimization Loop %i. Total Time: %0.2f seconds ####' % (opt_loop + 1, time.time() - starttime))

    ''' Update PV forecast data in the OpenDSS simulations '''
    # Get the new forecast from the Connected Energy system for each of the PV systems in the feeder.pv_on_feeder
    feeder.update_pv_forecasts(api=api)
    # scale PV forecasts from W to p.u.
    pv_forecast = {pv: feeder.pv_forecasts[pv].values[:periods] * 1. / pvdict[pv].ac_capacity for pv in feeder.pv_on_feeder}
    # print('pv_forecast: %s' % pv_forecast)

    ''' Update Load information in the OpenDSS simulations '''
    # Get the new load data from the state estimator.  Assume persistence and forecast the same value into the future
    p_forecast, q_forecast = feeder.get_load_forecast(periods=periods)
    print('p_forecast: %s' % p_forecast)
    print('q_forecast: %s' % q_forecast)

    ''' control and options for optimization '''
    penalty = {'violation': 1.0, 'deviation': 1.0, 'power_factor': 0.05}

    # Voltage violation is at ANSI Range A
    # Optimization will not run if all voltages are within 0.2% of Vnom
    # PFs will not change if the new PF do not improve objective function my 0.5%
    threshold = {'violation': 0.05, 'accept': 0.002, 'object': 0.005}
    debug = True
    swarmsize = 10*len(pvlist)
    maxiter = 10
    minstep = 0.001
    minfunc = 1e-6

    options = PFOptim(penalty=penalty, threshold=threshold, debug=debug,
                         swarmsize=swarmsize, maxiter=maxiter, minstep=minstep,
                         minfunc=minfunc)

    new_pf, opt_obj = feeder.update_power_factors(pvlist, pv_forecast, p_forecast, q_forecast,
                                         hour=0, sec=0, stepsize=stepsize,
                                         numsteps=periods, options=options)

    print('The optimal power factors are %s' % new_pf)

    ''' Write the optimal PF values to the DER devices using the Connected Energy API '''
    # format of the DER write dict
    # der = {"epri1": {'excitation': "injectingQ", 'pf': -0.95, 'forecast': None},  # neg = Q4 (EPRI sign convention)
    #       "epri2": {'excitation': "injectingQ", 'pf': 0.93, 'forecast': None},
    #       "epri3": {'excitation': "injectingQ", 'pf': -0.88, 'forecast': None}}

    der = {}
    new_q_values = {}
    pv_names = []  # controller DER for the save file
    for pv_name in new_pf.keys():
        if new_pf[pv_name] >= 0:  # EPRI simulator convention
            excitation = "injectingQ"
            new_q_values[pv_name] = np.arccos(new_pf[pv_name])
        else:
            excitation = "absorbingQ"
            new_q_values[pv_name] = -1.0 * np.arccos(-new_pf[pv_name])
        der[dss_to_phil_map[pv_name]] = {'excitation': excitation, 'pf': new_pf[pv_name], 'forecast': None}
        pv_names.append(pv_name)
    print('The optimal reactive power values are %s' % new_q_values)

    print('DER dictionary to send to CE\'s API: %s' % der)
    api.set_pf(der=der)

    # Write data from this optimization loop
    results = '%s, %0.5f, %0.5f, %0.5f, %0.2f, %0.2f, %0.2f, %s, %s, %s, %s \n' % (time.time() - starttime,
                                                                                    new_pf[pv_names[0]],
                                                                                    new_pf[pv_names[1]],
                                                                                    new_pf[pv_names[2]],
                                                                                    new_q_values[pv_names[0]],
                                                                                    new_q_values[pv_names[1]],
                                                                                    new_q_values[pv_names[2]],
                                                                                    opt_obj, pv_forecast.values(),
                                                                                    p_forecast.values(),
                                                                                   q_forecast.values())

    # open/close results file each time so the latest data is stored even with a crash
    csvfile = open(results_filename, 'a')
    csvfile.write(results)
    csvfile.close()

    runtime = time.time() - starttime
    wait_time = sec_per_loop - (runtime % sec_per_loop)
    print('Total Run Time: %s. Waiting %0.1f seconds until recalculating optimal PFs.' % (runtime, wait_time))
    time.sleep(wait_time)  # Run code every sec_per_loop

