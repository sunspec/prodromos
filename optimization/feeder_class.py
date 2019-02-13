# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 09:43:05 2019

@author: cwhanse
"""

import numpy as np
from . import dss_util

class Feeder():

    def __init__(self, filename, pv):
        """
        filename is the DSS master file
        pv is a dict of the form {derid: pvobj}
        """
        self.DSS = dss_util.DSS(filename)
        self.pv_on_feeder = list(self.DSS.circuit.PVSystems.AllNames)
        self.pv = pv
        if not (set(self.pv_on_feeder) <= set(pv)):
            raise ValueError('pv keys {} do not match OpenDSS PV systems {}'
                             .format(pv, self.pv_on_feeder))
        self.pv_forecasts = {}
        self.pf = {pv: 1.0 for pv in self.pv_on_feeder}


    def get_pv_forecast(self, derid, api):
        """
        Gets forecast from server.
        
        Args:
            derid: str
            api: CE_API
        
        Returns: pandas Series
        """
        return api.get_forecasts([derid])[derid]

    def update_pv_forecasts(self, api):
        """
        Updates self.pv_forecasts, a dict of the form {derid, forecast}
        """
        for derid in self.pv_on_feeder:
            pvobj = self.pv[derid]
            if pvobj.surrogateid:
                # use surrogate system for forecast
                pvobj_fc = self.pv[pvobj.surrogateid]
                capacity_ratio = pvobj.ac_capacity / pvobj_fc.ac_capacity
            else:
                pvobj_fc = pvobj
                capacity_ratio = 1.0
            fc = self.get_pv_forecast(pvobj_fc.derid, api)
            self.pv_forecasts[derid] = fc * capacity_ratio

    def get_load_forecast(self, periods):
        """ Returns dict of the form {bus: load} where load is of type Load
        """
        curr_loads = self.DSS.get_loads()
        load_fc = {}
        for b in curr_loads.keys():
            Pmult = np.tile(curr_loads[b].Pmult[0], periods)
            load_fc[b] = dss_util.Load(curr_loads[b].kW, Pmult)
        return load_fc

    def update_loads(self, loads):
        """ Updates loads for each bus

        Args:
            loads: dict {load name: load} where load is of type Load
        """
        for b in loads.keys():
            self.DSS.set_load(b, loads[b].Pmult)

    def update_power_factors(self, pvlist, pv_forecast, load_forecast, 
                             stepsize, numsteps, options):
        """
        Determines new power factor settings.
        
        Args:
            pvlist: list
                derid (str) for each PV system with changeable power factor
            pv_forecast: dict
                {derid, forecast} for each PV system on the Feeder.
                derid: (str)
                forecast: numeric
            load_forecast: dict
                {loadid, forecast} for each bus on the Feeder.
                loadid: str
                forecast: numeric
            stepsize: str
                interval in pv_forecast and load_forecast, of the form 'XXm'
                where XX is number of minutes
            numsteps: int
                number of intervals to consider in power flow calculation
            options: VVar_opt

        Returns:
            pf: dict
                {pv, pf} where pv is in pvlist
        """
        pvlist = self.pv_on_feeder
        curr_pf = []
        pf_ub = []
        pf_lb = []
        for pv in pvlist:
            curr_pf.append(self.pf[pv])
            pf_ub.append(self.pv[pv].pf_max)
            pf_lb.append(self.pv[pv].pf_min)
        change, new_pf = dss_util.update_power_factors(curr_pf, pv_forecast,
                                                       load_forecast, self.DSS,
                                                       pvlist, hour, sec,
                                                       pf_lb, pf_ub, options)
        if change:
            pf = {pv: pf for (pv, pf) in zip(pvlist, new_pf)}
        else:
            pf = {pv: pf for (pv, pf) in zip(pvlist, curr_pf)}
        return pf

