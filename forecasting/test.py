# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 10:57:30 2018

@author: cwhanse
"""
import pvlib
import pytz
from pv_forecast_dev import PVobj
import pandas as pd
from datetime import timedelta

USMtn = pytz.timezone('US/Mountain')
if pvlib.__version__ < '0.4.1':
    print('pvlib out-of-date, found version ' + pvlib.__version__ +
          ', please upgrade to 0.4.1 or later')
else:
    # make a dict of PV system objects
    pvdict = {};

    pvdict['sunpower2018'] = PVobj('sunpower',
                                   dc_capacity=1900,
                                   ac_capacity=3000,
                                   lat=35.05,
                                   lon=-106.54,
                                   alt=1657,
                                   tz=USMtn,
                                   tilt=35,
                                   azimuth=180,
                                   forecast_method='persistence')

    from dateutil import parser

    timestamps = [parser.parse(ts).replace(tzinfo=pytz.UTC).astimezone(USMtn)
                  for ts in
                  ['2018-09-20T12:55:00','2018-09-20T13:00:00','2018-09-20T13:15:00','2018-09-20T13:30:00','2018-09-20T13:45:00','2018-09-20T14:00:00']]
    values = [9000, 9000, 9000, 9000, 9000, 9000]
    history = pd.Series(data=values, index=pd.DatetimeIndex(timestamps))
    start = parser.parse('2018-09-20T13:55:00').replace(tzinfo=pytz.UTC).astimezone(USMtn)
    end = parser.parse('2018-09-20T15:55:00').replace(tzinfo=pytz.UTC).astimezone(USMtn)


    fc_2018 = pvdict['sunpower2018'].forecast(start=start,
                                              end=end,
                                              history=history,
                                              deltat=timedelta(minutes=5),
                                              dataWindowLength=timedelta(hours=1))
    print(fc_2018)

