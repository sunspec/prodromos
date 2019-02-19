# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 15:15:16 2019

@author: cwhanse
"""
from datetime import timedelta
from . import pv_forecast_util

class PVobj():
    # create an instance of a PV class object
    def __init__(self, derid, lat, lon, alt, tz,
                 tilt, azimuth, dc_capacity, ac_capacity,
                 pf_max, pf_min,
                 forecast_method='persistence', surrogateid=None,
                 dssid=None):

        self.derid = derid
        # surrogateid will be used to forecast for derid, if provided
        self.surrogateid = surrogateid
        self.dssid = dssid
        if forecast_method.lower() in ['arma', 'persistence']:
            self.forecast_method = forecast_method.lower()
        else:
            # TODO: raise error
            warnstring = 'DER ID ' + str(derid) + \
               ' : no forecast method specified, default to persistence'
            raise RuntimeWarning(warnstring)
            self.forecast_method = None
        self.dc_capacity = dc_capacity
        self.ac_capacity = ac_capacity
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.timezone = tz
        self.tilt = tilt
        self.azimuth = azimuth
        self.pf_max = pf_max
        self.pf_min = pf_min

    # PVobj member functions
    def forecast(self,
                 start,
                 end,
                 history,
                 deltat=timedelta(minutes=15),
                 dataWindowLength=timedelta(hours=1),
                 order=(1, 1, 0),
                 sunrise=None):

        # wrapper for functions forecast_ARMA and forecast_persistence

        if self.forecast_method == 'arma':
            return pv_forecast_util.forecast_ARMA(self,
                                 start,
                                 end,
                                 history,
                                 deltat,
                                 dataWindowLength,
                                 order)

        elif self.forecast_method == 'persistence':
            return pv_forecast_util.forecast_persistence(self,
                                        start,
                                        end,
                                        history,
                                        deltat,
                                        dataWindowLength,
                                        sunrise)