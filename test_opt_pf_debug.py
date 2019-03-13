# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 13:58:12 2019

@author: cwhanse
"""

import pytz
from optimization.feeder_class import Feeder
from forecasting.pv_system_class import PVobj
from optimization.dss_util import PFOptim
import os
import numpy as np
from optimization.dss_util import calc_obj, penalty2list


USMtn = pytz.timezone('US/Mountain')


# Create dictionary of all PV systems and associated forecast information
pvdict = {}
use_surrogates = False
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
    pvdict['pvsy1'] = PVobj('epri3', dc_capacity=1000e3, ac_capacity=1000e3, lat=35.05, lon=-106.54, alt=1657,
                            tz=USMtn, tilt=35, azimuth=180, pf_max=0.85, pf_min=-0.85,
                            forecast_method='persistence')

    pvdict['pvsy2'] = PVobj('epri2', dc_capacity=10000e3, ac_capacity=10000e3, lat=35.05, lon=-106.54, alt=1657,
                            tz=USMtn, tilt=35, azimuth=180, pf_max=0.85, pf_min=-0.85,
                            forecast_method='persistence')

    pvdict['pvsy3'] = PVobj('epri1', dc_capacity=258e3, ac_capacity=258e3, lat=35.05, lon=-106.54, alt=1657,
                            tz=USMtn, tilt=35, azimuth=180, pf_max=0.85, pf_min=-0.85,
                            forecast_method='persistence')

dss_to_phil_map = {'pvsy1': 'epri1', 'pvsy2': 'epri2', 'pvsy3': 'epri3'}

pvlist = list(pvdict.keys())

cwd = os.getcwd()

# Setup feeder object which points to the local OpenDSS time series simulation
feeder = Feeder(filename=cwd + "\\PNM_reduced_timeseries\\Master.DSS", pv=pvdict)

derlist = feeder.pv_on_feeder  # the controllable DER on the feeder
loadlist = feeder.DSS.circuit.Loads.AllNames

if not (set(derlist) <= set(pvlist)):
    raise ValueError('OpenDSS PV system list not included in pvlist')

# stepsize hardcoded at 5m for now because that's the resolution of the PV forecasts
stepsize = '5m'

# Number of stepsize time periods that the optimization will be working over
periods = 3

which = 12716

if which==2335:
    pv_forecast = {'pvsy1': np.array([0.50735348, 0.52203657, 0.5365032 ]),
                   'pvsy2': np.array([0.39371394, 0.40510824, 0.41633457]),
                   'pvsy3': np.array([0.50432767, 0.51892318, 0.53330354])}
    p_forecast = {'load142': np.array([0.98803568, 0.98803568, 0.98803568]),
                  'load143': np.array([0.98790436, 0.98790436, 0.98790436]),
                  'load144': np.array([0.98709768, 0.98709768, 0.98709768]),
                  'load133': np.array([0.98184213, 0.98184213, 0.98184213]),
                  'load134': np.array([0.98061394, 0.98061394, 0.98061394]),
                  'load135': np.array([0.97886882, 0.97886882, 0.97886882]),
                  'load20': np.array([0.48723141, 0.48723141, 0.48723141])}
    q_forecast = {'load142': np.array([0.97737663, 0.97737663, 0.97737663]),
                  'load143': np.array([0.9773692, 0.9773692, 0.9773692]),
                  'load144': np.array([0.97721731, 0.97721731, 0.97721731]),
                  'load133': np.array([0.33163815, 0.33163815, 0.33163815]),
                  'load134': np.array([0.3500364, 0.3500364, 0.3500364]),
                  'load135': np.array([0.38326755, 0.38326755, 0.38326755]),
                  'load20': np.array([0.98704586, 0.98704586, 0.98704586])}
    prior_pf = {'pvsy1': -0.9992755921799513, 'pvsy2': -0.9765051017408258,
                'pvsy3': 0.9958937925969981}
    ref_new_pf = {'pvsy1': -0.9992755921799513, 'pvsy2': -0.9765051017408258,
              'pvsy3': 0.9958937925969981}

elif which==2395:
    pv_forecast = {'pvsy1': np.array([0.5130373 , 0.52725455, 0.54125027]),
                   'pvsy2': np.array([0.41999446, 0.43163331, 0.44309081]),
                   'pvsy3': np.array([0.51363551, 0.52786933, 0.54188136])}
    p_forecast = {'load142': np.array([0.98744299, 0.98744299, 0.98744299]),
                  'load143': np.array([0.98732167, 0.98732167, 0.98732167]),
                  'load144': np.array([0.98654591, 0.98654591, 0.98654591]),
                  'load133': np.array([0.9813616, 0.9813616, 0.9813616]),
                  'load134': np.array([0.980138, 0.980138, 0.980138]),
                  'load135': np.array([0.97842982, 0.97842982, 0.97842982]),
                  'load20': np.array([0.48735571, 0.48735571, 0.48735571])}
    q_forecast = {'load142': np.array([0.97775353, 0.97775353, 0.97775353]),
                  'load143': np.array([0.97778793, 0.97778793, 0.97778793]),
                  'load144': np.array([0.97775304, 0.97775304, 0.97775304]),
                  'load133': np.array([0.33468284, 0.33468284, 0.33468284]),
                  'load134': np.array([0.35301471, 0.35301471, 0.35301471]),
                  'load135': np.array([0.38655799, 0.38655799, 0.38655799]),
                  'load20': np.array([0.98994339, 0.98994339, 0.98994339])}
    prior_pf = {'pvsy1': -0.9992755921799513, 'pvsy2': -0.9765051017408258,
                'pvsy3': 0.9958937925969981}
    ref_new_pf = {'pvsy1': 0.9983206462598185, 'pvsy2': 0.9849320175673264,
              'pvsy3': 0.9944201365744375}

elif which==2635:
    pv_forecast = {'pvsy1': np.array([0.5130373 , 0.52725455, 0.54125027]),
                   'pvsy2': np.array([0.41999446, 0.43163331, 0.44309081]),
                   'pvsy3': np.array([0.51363551, 0.52786933, 0.54188136])}
    p_forecast = {'load142': np.array([0.99549517, 0.99549517, 0.99549517]),
                  'load143': np.array([0.99539111, 0.99539111, 0.99539111]),
                  'load144': np.array([0.99459759, 0.99459759, 0.99459759]),
                  'load133': np.array([0.99161776, 0.99161776, 0.99161776]),
                  'load134': np.array([0.99039743, 0.99039743, 0.99039743]),
                  'load135': np.array([0.98865461, 0.98865461, 0.98865461]),
                  'load20': np.array([0.48770013, 0.48770013, 0.48770013])}
    q_forecast = {'load142': np.array([0.98671279, 0.98671279, 0.98671279]),
                  'load143': np.array([0.98677771, 0.98677771, 0.98677771]),
                  'load144': np.array([0.98673691, 0.98673691, 0.98673691]),
                  'load133': np.array([0.34186948, 0.34186948, 0.34186948]),
                  'load134': np.array([0.36030417, 0.36030417, 0.36030417]),
                  'load135': np.array([0.3942703, 0.3942703, 0.3942703]),
                  'load20': np.array([1.00121995, 1.00121995, 1.00121995])}
    prior_pf = {'pvsy1': -0.9998088302452541, 'pvsy2': -0.978758756686363,
                'pvsy3': 0.9943667532325103}
    ref_new_pf = {'pvsy1': -0.999629112121408, 'pvsy2': -0.9796364552516997,
              'pvsy3': 0.9941509696129766}

elif which==2695:
    pv_forecast = {'pvsy1': np.array([0.52833047, 0.54235474, 0.55614847]),
                   'pvsy2': np.array([0.42488386, 0.43616219, 0.44725512]),\
                   'pvsy3': np.array([0.54041048, 0.5547554 , 0.56886452])}
    
    p_forecast = {'load142': np.array([0.99644214, 0.99644214, 0.99644214]),
                  'load143': np.array([0.99633901, 0.99633901, 0.99633901]),
                  'load144': np.array([0.99554537, 0.99554537, 0.99554537]),
                  'load133': np.array([0.99327939, 0.99327939, 0.99327939]),
                  'load134': np.array([0.99205591, 0.99205591, 0.99205591]),
                  'load135': np.array([0.99031344, 0.99031344, 0.99031344]),
                  'load20': np.array([0.4896474, 0.4896474, 0.4896474])}
    
    q_forecast = {'load142': np.array([0.98762943, 0.98762943, 0.98762943]),
                  'load143': np.array([0.98771014, 0.98771014, 0.98771014]),
                  'load144': np.array([0.98766852, 0.98766852, 0.98766852]),
                  'load133': np.array([0.34247855, 0.34247855, 0.34247855]),
                  'load134': np.array([0.36099848, 0.36099848, 0.36099848]),
                  'load135': np.array([0.394991, 0.394991, 0.394991]),
                  'load20': np.array([1.00245823, 1.00245823, 1.00245823])}

    prior_pf = {'pvsy1': -0.999629112121408, 'pvsy2': -0.9796364552516997,
                'pvsy3': 0.9941509696129766}

    ref_new_pf = {'pvsy1': -0.9996218404344657, 'pvsy2': -0.9791126484100631,
                  'pvsy3': 0.9935960802968158}

elif which==12716:
    pv_forecast = {'pvsy1': np.array([0.64345614, 0.64538518, 0.64538518]),
                   'pvsy2': np.array([0.52141057, 0.52297373, 0.52297373]),
                   'pvsy3': np.array([0.61528297, 0.61712754, 0.61712754])}
    p_forecast = {'load142': np.array([0.98984651, 0.98984651, 0.98984651]),
                  'load143': np.array([0.98971563, 0.98971563, 0.98971563]),
                  'load144': np.array([0.98894367, 0.98894367, 0.98894367]),
                  'load133': np.array([0.98382005, 0.98382005, 0.98382005]),
                  'load134': np.array([0.98258515, 0.98258515, 0.98258515]),
                  'load135': np.array([0.98087875, 0.98087875, 0.98087875]),
                  'load20': np.array([0.59220664, 0.59220664, 0.59220664])}
    q_forecast = {'load142': np.array([0.98028833, 0.98028833, 0.98028833]),
                  'load143': np.array([0.98032463, 0.98032463, 0.98032463]),
                  'load144': np.array([0.98028568, 0.98028568, 0.98028568]),
                  'load133': np.array([0.33606385, 0.33606385, 0.33606385]),
                  'load134': np.array([0.35446236, 0.35446236, 0.35446236]),
                  'load135': np.array([0.38806192, 0.38806192, 0.38806192]),
                  'load20': np.array([1.03938613, 1.03938613, 1.03938613])}
    prior_pf = {'pvsy1': -0.999560425500708, 'pvsy2': -0.9847891284391119,
                'pvsy3': 0.998249598032435}
    ref_new_pf = {'pvsy1': -0.9980572871197689, 'pvsy2': 0.9856791970303866,
                  'pvsy3': 0.9956149347591993}

else:
    pass

#    feeder.update_pv_forecasts(api=api)
for derid in feeder.pv_on_feeder:
    pvobj = feeder.pv[derid]
    if pvobj.surrogateid:
        # use surrogate system for forecast
        pvobj_fc = feeder.pv[pvobj.surrogateid]
        capacity_ratio = pvobj.ac_capacity / pvobj_fc.ac_capacity
    else:
        pvobj_fc = pvobj
        capacity_ratio = 1.0
    fc = pv_forecast[derid]
    feeder.pv_forecasts[derid] = fc * capacity_ratio

    ''' control and options for optimization '''
    penalty = {'violation': 1.0, 'deviation': 2.0, 'power_factor': 0.05}

    # Voltage violation is at ANSI Range A
    # Optimization will not run if all voltages are within 0.2% of Vnom
    # PFs will not change if the new PF do not improve objective function my 0.5%
threshold = {'violation': 0.05, 'accept': 0.002, 'object': 0.001}
debug = True
swarmsize = 30
maxiter = 10
minstep = 0.001
minfunc = 1e-6

options = PFOptim(penalty=penalty, threshold=threshold, debug=debug,
                     swarmsize=swarmsize, maxiter=maxiter, minstep=minstep,
                     minfunc=minfunc)

#new_pf, prior_pf, opt_obj = feeder.update_power_factors(pvlist, pv_forecast,
#                                                        p_forecast, q_forecast,
#                                     hour=0, sec=0, stepsize=stepsize,
#                                     numsteps=periods, options=options,
#                                     prior_pf=ref_new_pf)

pf_prior = [prior_pf[pv] for pv in pvlist]
result_prior = feeder.DSS.run(pf_prior, pvlist, hour=0, sec=0,
                              pv_profile=pv_forecast, p_profile=p_forecast,
                              q_profile=q_forecast,
                              periods=periods, stepsize=stepsize)

obj_prior =calc_obj(result_prior, penalty2list(options.penalty), 
                    options.threshold['violation'],
                    base_voltage=1.0,
                    power_factors=pf_prior)
print(obj_prior)

unity_obj =calc_obj(result_prior, penalty2list(options.penalty),
                    options.threshold['violation'],
                    base_voltage=1.0,
                    power_factors=[1., 1., 1.])

print(unity_obj)

tot = 0.0
for v in result_prior:
    tot += penalty['deviation']*np.std(v - 1.0) + penalty['power_factor']*np.sum(1.0 - np.abs(pf_prior))
    print(penalty['deviation']*np.std(v - 1.0), penalty['power_factor']*np.sum(1.0 - np.abs(pf_prior)))

pf_next = [ref_new_pf[pv] for pv in pvlist]
result_next = feeder.DSS.run(pf_next, pvlist, hour=0, sec=0,
                             pv_profile=pv_forecast, p_profile=p_forecast,
                             q_profile=q_forecast,
                             periods=periods, stepsize=stepsize)
obj_next =calc_obj(result_next, penalty2list(options.penalty), 
                   options.threshold['violation'],
                   base_voltage=1.0,
                   power_factors=pf_next)
print(obj_next)

for v in result_next:
    print(penalty['deviation']*np.std(v - 1.0), penalty['power_factor']*np.sum(1.0 - np.abs(pf_next)))


