# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 10:44:21 2018

@author: cwhanse
"""

import pandas as pd
from datetime import datetime, timedelta
import pv_forecast_dev
import numpy as np
import pytz
from matplotlib import pyplot as plt

USMtn = pytz.timezone('US/Mountain')

# read in historical data, clear sky and old forecast

filen = 'C:\\python\\prodromos-dev\\forecasting\\pvanalysis_sunpower2201_avg5_2018-10-24T17_21_51.853Z.csv'

with open(filen, 'r') as infile:
    df = pd.read_csv(infile, index_col='timestamp (UTC)', parse_dates=['timestamp (UTC)'])

df.rename(columns={'history (kW)': 'ac_power', 'forecast(kW)': 'forecast', 
                'clear sky(kW)': 'clearsky'}, inplace=True)
df = df.tz_localize('UTC')

df = df.tz_convert(USMtn)

#plt.plot(df['history'])

fcn = pd.DataFrame(df[['ac_power', 'forecast']])
fcn.rename(columns={'forecast': 'old'}, inplace=True)
fcn['new'] = np.nan

st = df.index[0] + timedelta(days=2)

pv = pv_forecast_dev.PVobj('sunpower',
                                dc_capacity=1900,
                                ac_capacity=3000,
                                lat=35.05,
                                lon=-106.54,
                                alt=1657,
                                tz=USMtn,
                                tilt=35,
                                azimuth=180,
                                forecast_method='persistence')

while st<df.index[-1] - timedelta(days=1):
    fc = pv.forecast(start=st, end=st+timedelta(hours=1), history=df['ac_power'],
                 deltat=timedelta(minutes=5),
                 dataWindowLength=timedelta(hours=1),
                 sunrise='yesterday')
    fc.name = 'new'
    fcn.update(fc.to_frame())
    st += timedelta(minutes=15)

plt.plot(fcn, '-')

plt.scatter(fcn['old'].values, fcn['new'].values)

plt.scatter(fcn['ac_power'].values, fcn['old'].values)
print(((fcn['ac_power'] - fcn['old'])**2).mean()*0.5)

plt.scatter(fcn['ac_power'].values, fcn['new'].values)
print(((fcn['ac_power'] - fcn['new'])**2).mean()*0.5)

err_old = fcn['old'].values - fcn['ac_power'].values
err_new = fcn['new'].values - fcn['ac_power'].values
plt.hist(err_old[~np.isnan(err_old)])
plt.hist(err_new[~np.isnan(err_new)])

dates = np.unique(df.index.date)

for dd in dates:
    dn = pd.to_datetime(dd).tz_localize(USMtn)
    plt.plot(fcn.loc[(fcn.index>dn) & (fcn.index<dn+timedelta(days=1))])
    plt.show()




