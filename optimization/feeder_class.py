# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 09:43:05 2019

@author: cwhanse
"""

import numpy as np
from . import dss_util
from stateestimation.pmu_capture import *
import pymu.tools as tools
import time
import socket
import os
import sys
import math
import pprint
pp = pprint.PrettyPrinter(indent=4)

# model = 'PNM'
model = 'NG'

''' OpenDSS Load data for reduced-order PNM model.  Note: the smaller loads are ignored
New "Load.Load136" phases=1 kW=0 kvar=0.003438665 kV=7.199557857 
New "Load.Load137" phases=1 kW=3.860344758 kvar=0.489471522 kV=7.199557857 
New "Load.Load138" phases=1 kW=2.670415479 kvar=0.302451287 kV=7.199557857 

New "Load.Load139" phases=1 kW=0.028182185 kvar=-0.00895 kV=7.199557857 
New "Load.Load140" phases=1 kW=2.288289329 kvar=0.41371859 kV=7.199557857 
New "Load.Load141" phases=1 kW=0.393998726 kvar=0.154409997 kV=7.199557857 

New "Load.Load142" phases=1 kW=97.118471073 kvar=22.060387399 kV=7.199557857 
New "Load.Load143" phases=1 kW=100.579630241 kvar=22.407056152 kV=7.199557857
New "Load.Load144" phases=1 kW=116.317688067 kvar=25.61554001 kV=7.199557857

New "Load.Load133" phases=1 kW=107.384198104 kvar=11.558831106 kV=7.199557857 
New "Load.Load134" phases=1 kW=108.561893753 kvar=11.911280386 kV=7.199557857
New "Load.Load135" phases=1 kW=118.930157052 kvar=12.605383418 kV=7.199557857

New "Load.Load19" phases=3 kV=0.48 kW=25.5 kvar=19.2 
New "Load.Load20" phases=3 kV=12.47 kW=1885 kvar=1292
'''

if model == 'PNM':
    # Create large dictionary of data to collect from PMU stream from state estimator - PNM Loads.
    LOADS = {'load142': {'Bus': 'B09', 'OpenDSSname': 'Load.Load142', 'Phasors':  ['795D00087-01'], 'phase': [0],
                        'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.],
                         'init_load': 0, 'init_q_load': 0},
             'load143': {'Bus': 'B09', 'OpenDSSname': 'Load.Load143', 'Phasors':  ['795D00088-01'], 'phase': [1],
                        'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.],
                         'init_load': 0, 'init_q_load': 0},
             'load144': {'Bus': 'B09', 'OpenDSSname': 'Load.Load144', 'Phasors': ['795D00089-01'], 'phase': [2],
                        'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.],
                         'init_load': 0, 'init_q_load': 0},
             'load133': {'Bus': 'B10', 'OpenDSSname': 'Load.Load133', 'Phasors':  ['795D00090-01'], 'phase': [0],
                        'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.],
                         'init_load': 0, 'init_q_load': 0},
             'load134': {'Bus': 'B10', 'OpenDSSname': 'Load.Load134', 'Phasors':  ['795D00091-01'], 'phase': [1],
                        'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.],
                         'init_load': 0, 'init_q_load': 0},
             'load135': {'Bus': 'B10', 'OpenDSSname': 'Load.Load135', 'Phasors': ['795D00092-01'], 'phase': [2],
                        'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.],
                         'init_load': 0, 'init_q_load': 0},
             'load20': {'Bus': 'B04', 'OpenDSSname': 'Load.Load20', 'Phasors': ['796D00097-03'], 'phase': [0, 1, 2],
                        'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.],
                        'init_load': 0, 'init_q_load': 0},
             'PV1': {'Bus': 'B12', 'OpenDSSname': 'PVSystem.PVSy1', 'Phasors': ['794D00050-02'], 'phase': [0, 1, 2],
                     'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV2': {'Bus': 'B14', 'OpenDSSname': 'PVSystem.PVSy2', 'Phasors': ['794D00057-02'], 'phase': [0, 1, 2],
                     'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV3': {'Bus': 'B15', 'OpenDSSname': 'PVSystem.PVSy3', 'Phasors': ['794D00084-02'], 'phase': [0, 1, 2],
                        'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             }

if model == 'NG':
    # Create large dictionary of data to collect from PMU stream

    LOADS = {'load1633': {'Bus': 'B09', 'OpenDSSname': 'Load.Load1633', 'Phasors': ['795D00021-01'], 'phase': [0],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.],
                          'init_load': 0, 'init_q_load': 0},
             'PV1': {'Bus': 'B11', 'OpenDSSname': 'PVSystem.PVSy1', 'Phasors': ['794D00105-02'], 'phase': [0, 1, 2],
                     'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             }
    '''
    LOADS = {'load1633': {'Bus': 'B09', 'OpenDSSname': 'Load.Load1633', 'Phasors':  ['795D00021-01'], 'phase': [0],  # Section 1
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1615': {'Bus': 'B07', 'OpenDSSname': 'Load.Load1615', 'Phasors':  ['795D00014-01'], 'phase': [0],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1616': {'Bus': 'B07', 'OpenDSSname': 'Load.Load1615', 'Phasors': ['795D00015-01'], 'phase': [1],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1617': {'Bus': 'B07', 'OpenDSSname': 'Load.Load1615', 'Phasors': ['795D00016-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1612': {'Bus': 'B04', 'OpenDSSname': 'Load.Load1612', 'Phasors': ['795D00045-01'], 'phase': [0],  # Section 2
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1613': {'Bus': 'B04', 'OpenDSSname': 'Load.Load1613', 'Phasors': ['795D00046-01'], 'phase': [1],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1614': {'Bus': 'B04', 'OpenDSSname': 'Load.Load1614', 'Phasors': ['795D00047-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1627': {'Bus': 'B05', 'OpenDSSname': 'Load.Load1627', 'Phasors': ['795D00048-01'], 'phase': [0],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1628': {'Bus': 'B05', 'OpenDSSname': 'Load.Load1628', 'Phasors': ['795D00049-01'], 'phase': [1],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1629': {'Bus': 'B05', 'OpenDSSname': 'Load.Load1629', 'Phasors': ['795D00050-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1630': {'Bus': 'B13', 'OpenDSSname': 'Load.Load1630', 'Phasors': ['795D00051-01'], 'phase': [0],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1631': {'Bus': 'B13', 'OpenDSSname': 'Load.Load1631', 'Phasors': ['795D00052-01'], 'phase': [1],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1632': {'Bus': 'B13', 'OpenDSSname': 'Load.Load1632', 'Phasors': ['795D00053-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1609': {'Bus': 'B06', 'OpenDSSname': 'Load.Load1609', 'Phasors': ['795D00069-01'], 'phase': [0],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1610': {'Bus': 'B06', 'OpenDSSname': 'Load.Load1610', 'Phasors': ['795D00070-01'], 'phase': [1],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1611': {'Bus': 'B06', 'OpenDSSname': 'Load.Load1611', 'Phasors': ['795D00071-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1624': {'Bus': 'B12', 'OpenDSSname': 'Load.Load1624', 'Phasors': ['795D00072-01'], 'phase': [0],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1625': {'Bus': 'B12', 'OpenDSSname': 'Load.Load1625', 'Phasors': ['795D00073-01'], 'phase': [1],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1626': {'Bus': 'B12', 'OpenDSSname': 'Load.Load1626', 'Phasors': ['795D00074-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1618': {'Bus': 'B08', 'OpenDSSname': 'Load.Load1618', 'Phasors': ['795D00092-01'], 'phase': [0],  # Section 3
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1619': {'Bus': 'B08', 'OpenDSSname': 'Load.Load1619', 'Phasors': ['795D00093-01'], 'phase': [1],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1620': {'Bus': 'B08', 'OpenDSSname': 'Load.Load1620', 'Phasors': ['795D00094-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1606': {'Bus': 'B09', 'OpenDSSname': 'Load.Load1606', 'Phasors': ['795D00086-01'], 'phase': [0],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1607': {'Bus': 'B09', 'OpenDSSname': 'Load.Load1607', 'Phasors': ['795D00087-01'], 'phase': [1],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1608': {'Bus': 'B09', 'OpenDSSname': 'Load.Load1608', 'Phasors': ['795D00088-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1602': {'Bus': 'B10', 'OpenDSSname': 'Load.Load1602', 'Phasors': ['795D00089-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1603': {'Bus': 'B11', 'OpenDSSname': 'Load.Load1603', 'Phasors': ['795D00102-01'], 'phase': [0],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1604': {'Bus': 'B11', 'OpenDSSname': 'Load.Load1604', 'Phasors': ['795D00103-01'], 'phase': [1],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1605': {'Bus': 'B11', 'OpenDSSname': 'Load.Load1605', 'Phasors': ['795D00104-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1621': {'Bus': 'B02', 'OpenDSSname': 'Load.Load1621', 'Phasors': ['795D00119-01'], 'phase': [0],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1622': {'Bus': 'B02', 'OpenDSSname': 'Load.Load1622', 'Phasors': ['795D00120-01'], 'phase': [1],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1623': {'Bus': 'B02', 'OpenDSSname': 'Load.Load1623', 'Phasors': ['795D00121-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1636': {'Bus': 'B03', 'OpenDSSname': 'Load.Load1636', 'Phasors': ['795D00122-01'], 'phase': [0],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1637': {'Bus': 'B03', 'OpenDSSname': 'Load.Load1637', 'Phasors': ['795D00123-01'], 'phase': [1],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'load1638': {'Bus': 'B03', 'OpenDSSname': 'Load.Load1638', 'Phasors': ['795D00124-01'], 'phase': [2],
                          'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.], 'init_load': 0, 'init_q_load': 0},
             'PV869': {'Bus': 'B14', 'OpenDSSname': 'PVSystem.PVSy869', 'Phasors': ['792D00018-02'], 'phase': [0],  # Section 1
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV851': {'Bus': 'B07', 'OpenDSSname': 'PVSystem.PVSy851', 'Phasors': ['792D00011-02'], 'phase': [0],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV848': {'Bus': 'B04', 'OpenDSSname': 'PVSystem.PVSy848', 'Phasors': ['792D00025-02'], 'phase': [0],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV849': {'Bus': 'B04', 'OpenDSSname': 'PVSystem.PVSy849', 'Phasors': ['792D00026-02'], 'phase': [1],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV850': {'Bus': 'B04', 'OpenDSSname': 'PVSystem.PVSy850', 'Phasors': ['792D00027-02'], 'phase': [2],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV863': {'Bus': 'B05', 'OpenDSSname': 'PVSystem.PVSy863', 'Phasors': ['792D00031-02'], 'phase': [0],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV864': {'Bus': 'B05', 'OpenDSSname': 'PVSystem.PVSy864', 'Phasors': ['792D00032-02'], 'phase': [1],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV865': {'Bus': 'B05', 'OpenDSSname': 'PVSystem.PVSy865', 'Phasors': ['792D00033-02'], 'phase': [2],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV866': {'Bus': 'B13', 'OpenDSSname': 'PVSystem.PVSy866', 'Phasors': ['792D00037-02'], 'phase': [0],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV867': {'Bus': 'B13', 'OpenDSSname': 'PVSystem.PVSy867', 'Phasors': ['792D00038-02'], 'phase': [1],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV868': {'Bus': 'B13', 'OpenDSSname': 'PVSystem.PVSy868', 'Phasors': ['792D00039-02'], 'phase': [2],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV845': {'Bus': 'B06', 'OpenDSSname': 'PVSystem.PVSy845', 'Phasors': ['792D00058-02'], 'phase': [0],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV846': {'Bus': 'B06', 'OpenDSSname': 'PVSystem.PVSy846', 'Phasors': ['792D00059-02'], 'phase': [1],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV847': {'Bus': 'B06', 'OpenDSSname': 'PVSystem.PVSy847', 'Phasors': ['792D00060-02'], 'phase': [2],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV860': {'Bus': 'B12', 'OpenDSSname': 'PVSystem.PVSy860', 'Phasors': ['792D00061-02'], 'phase': [0],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV861': {'Bus': 'B12', 'OpenDSSname': 'PVSystem.PVSy861', 'Phasors': ['792D00062-02'], 'phase': [1],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV862': {'Bus': 'B12', 'OpenDSSname': 'PVSystem.PVSy862', 'Phasors': ['792D00063-02'], 'phase': [2],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV854': {'Bus': 'B08', 'OpenDSSname': 'PVSystem.PVSy854', 'Phasors': ['792D00098-02'], 'phase': [0],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV855': {'Bus': 'B08', 'OpenDSSname': 'PVSystem.PVSy855', 'Phasors': ['792D00097-02'], 'phase': [1],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV856': {'Bus': 'B08', 'OpenDSSname': 'PVSystem.PVSy856', 'Phasors': ['792D00096-02'], 'phase': [2],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV842': {'Bus': 'B09', 'OpenDSSname': 'PVSystem.PVSy842', 'Phasors': ['792D00079-02'], 'phase': [0],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV843': {'Bus': 'B09', 'OpenDSSname': 'PVSystem.PVSy843', 'Phasors': ['792D00080-02'], 'phase': [1],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV844': {'Bus': 'B09', 'OpenDSSname': 'PVSystem.PVSy844', 'Phasors': ['792D00081-02'], 'phase': [2],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV838': {'Bus': 'B10', 'OpenDSSname': 'PVSystem.PVSy838', 'Phasors': ['792D00078-02'], 'phase': [2],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV857': {'Bus': 'B02', 'OpenDSSname': 'PVSystem.PVSy857', 'Phasors': ['792D00109-02'], 'phase': [0],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV858': {'Bus': 'B02', 'OpenDSSname': 'PVSystem.PVSy858', 'Phasors': ['792D00110-02'], 'phase': [1],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV859': {'Bus': 'B02', 'OpenDSSname': 'PVSystem.PVSy859', 'Phasors': ['792D00111-02'], 'phase': [2],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV872': {'Bus': 'B03', 'OpenDSSname': 'PVSystem.PVSy872', 'Phasors': ['792D00112-02'], 'phase': [0],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV873': {'Bus': 'B03', 'OpenDSSname': 'PVSystem.PVSy873', 'Phasors': ['792D00113-02'], 'phase': [1],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV874': {'Bus': 'B03', 'OpenDSSname': 'PVSystem.PVSy874', 'Phasors': ['792D00114-02'], 'phase': [2],
                       'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             'PV1': {'Bus': 'B11', 'OpenDSSname': 'PVSystem.PVSy1', 'Phasors': ['794D00105-02'], 'phase': [0, 1, 2],
                     'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
             }
    '''


class Feeder(object):

    def __init__(self, filename, pv):
        """
        filename is the DSS master file
        pv is a dict of the form {derid: pvobj}
        """
        self.DSS = dss_util.DSS(filename)
        self.pv_on_feeder = list(self.DSS.circuit.PVSystems.AllNames)
        self.pv = pv
        if not (set(self.pv_on_feeder) <= set(pv)):
            raise ValueError('pv keys {} do not match OpenDSS PV systems {}'.format(pv, self.pv_on_feeder))
        self.pv_forecasts = {}
        self.pf = {pv: 1.0 for pv in self.pv_on_feeder}

        # get the original loads from OpenDSS
        self.loads = self.DSS.get_loads()
        # print('curr_loads: %s' % curr_loads)
        for bus in self.loads.keys():
            # print('bus: %s' % bus)
            # print('curr_loads[bus].kW: %s' % curr_loads[bus].kW)
            if bus in LOADS.keys():
                LOADS[bus]['init_load'] = self.loads[bus].kW
                LOADS[bus]['init_q_load'] = self.loads[bus].kvar

    @staticmethod
    def get_pv_forecast(derid, api):
        """
        Gets forecast from server.
        
        Args:
            derid: str
            api: CE_API
        
        Returns: pandas Series
        """
        print('Getting Forecast for derid: %s' % derid)
        return api.get_forecasts([derid])[derid]

    def update_pv_forecasts(self, api, debug=False):
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
            if debug:
                print('PV forecast: %s' % fc)
            self.pv_forecasts[derid] = fc * capacity_ratio

    def get_load_forecast(self, periods):
        """ Returns dict of the form {bus: load} where load is of type Load
        """
        cli3 = None
        d3 = None
        confFrame3 = None
        dFrame3 = None

        # Get Config Frame and Establish Client
        confFrame, cli = tools.startDataCapture(idcode=7007, ip="10.50.2.161", port=4125, tcpUdp='TCP', debug=True)
        print('Config Frame for Client 1 Captured!: %s' % confFrame)

        confFrame2, cli2 = tools.startDataCapture(idcode=7008, ip="10.50.2.161", port=4126, tcpUdp='TCP', debug=True)
        print('Config Frame for Client 2 Captured!: %s' % confFrame)

        if model == 'NG':
            confFrame3, cli3 = tools.startDataCapture(idcode=7009, ip="10.50.2.161", port=4127, tcpUdp='TCP',
                                                      debug=True)
            print('Config Frame for Client 3 Captured!: %s' % confFrame)

        save_pmu_data = False
        if save_pmu_data:
            csv_handle = createCsvFile(confFrame)
        else:
            csv_handle = None

        try:
            d = tools.getDataSample(cli, debug=False)
            d2 = tools.getDataSample(cli2, debug=False)
            if model == 'NG':
                d3 = tools.getDataSample(cli3, debug=False)
                if d == '' or d2 == '' or d3 == '':
                    print('No data samples from clients.  d1 = %s, d2 = %s, d3 = %s' % (d, d2, d3))
            else:
                if d == '' or d2 == '':
                    print('No data samples from clients.  d1 = %s, d2 = %s' % (d, d2))
            dFrame = DataFrame(d, confFrame)  # Create dataFrame
            dFrame2 = DataFrame(d2, confFrame2)  # Create dataFrame
            if model == 'NG':
                dFrame3 = DataFrame(d3, confFrame3)  # Create dataFrame

            if save_pmu_data:
                csvPrint(dFrame, csv_handle)  # Save 1 set of the State Estimation data

            print("Data Collection Started...")
            dFrame.dbg = False

            fill_dict_from_dataframes(dFrame=dFrame, LOADS=LOADS)
            fill_dict_from_dataframes(dFrame=dFrame2, LOADS=LOADS)
            if model == 'NG':
                fill_dict_from_dataframes(dFrame=dFrame3, LOADS=LOADS)

            pp.pprint(LOADS)

        except socket.timeout:
            print("#{}# Data not available right now...Exiting".format(p))
        except Exception as e:
            print("Exception: {}".format(e))

        # update the parameters of the loads based on the OpenDSS simulation
        load_p_fc = {}
        load_q_fc = {}
        # print('self.loads: %s' % self.loads)
        for load_name in self.loads.keys():
            load = self.loads[load_name]
            # print('load: %s' % load)
            load.update_load()
            # print('load.kW: %s' % load.kW)
            if load_name in LOADS.keys():  # if load name matches the state estimation load name

                init_load = LOADS[load_name]['init_load'] * 1000.  # in watts
                init_q_load = LOADS[load_name]['init_q_load'] * 1000.  # in vars

                # Get the multiplier for the first phase
                ph = load.phase[0]
                state_est_powers = LOADS[load_name]['P']
                state_est_q = LOADS[load_name]['Q']
                # print('state_est_powers: %s' % state_est_powers)
                # print('state_est_powers[ph]: %s' % state_est_powers[ph])

                if init_load != 0:
                    power_multiplier = state_est_powers[ph] / init_load
                else:
                    power_multiplier = 0

                if init_q_load != 0:
                    q_multiplier = state_est_q[ph] / init_q_load
                else:
                    q_multiplier = 0

                Pmult = np.tile(power_multiplier, periods)
                Qmult = np.tile(q_multiplier, periods)
                # print('Pmult: %s' % Pmult)

                print('For %s, the original power was %0.1f W, the state estimated power is %0.1f W, so the multiplier '
                      'is %0.6f' % (load_name, init_load, state_est_powers[ph], power_multiplier))
                print('For %s, the original q was %0.1f vars, the state estimated reactive power is %0.1f vars, '
                      'so the multiplier is %0.6f' % (load_name, init_q_load, state_est_q[ph], q_multiplier))

                self.loads[load_name].Pmult = Pmult
                self.loads[load_name].Qmult = Qmult

                # These loads are updated during optimization now
                # self.update_loads()  # set load in OpenDSS

                load_p_fc[load_name] = Pmult
                load_q_fc[load_name] = Qmult

        return load_p_fc, load_q_fc

    def update_loads(self):
        """ Updates load in DSS for each bus
        """
        for bus in self.loads.keys():
            self.DSS.set_load(bus, pmult=self.loads[bus].Pmult, qmult=self.loads[bus].Qmult)

    def update_power_factors(self, pvlist, pv_forecast, p_forecast, q_forecast, hour, sec, stepsize, numsteps, options,
                             controllable_pv=None, prior_pf=None, base=1.0):
        """
        Determines new power factor settings.

        Args:
            pvlist: list
                derid (str) for each PV system with changeable power factor
            pv_forecast: dict
                {derid, forecast} for each PV system on the Feeder.
                derid: (str)
                forecast: numeric
            p_forecast: dict
                {loadid, forecast} for each bus on the Feeder.
                loadid: str
                forecast: numeric np array
            q_forecast: dict
                {loadid, forecast} for each bus on the Feeder.
                loadid: str
                forecast: numeric np array
            hour: int
            sec: int
            stepsize: str
                interval in pv_forecast and load_forecast, of the form 'XXm'
                where XX is number of minutes
            numsteps: int
                number of intervals to consider in power flow calculation
            options: VVar_opt
            controllable_pv: list, default None
                optional parameter representing a subset of the pvlist that has
                controllable PF setpoints. If None, then controllable_pv is set
                equal to pvlist
            prior_pf: dict
                optional parameter that can instantiate the PSO with a
                different starting prior PF solution
            base: float
                target base voltage (p.u.)
        Returns:
            pf: dict
                {pv, pf} where pv is in pvlist
        """

        if controllable_pv is None:
            controllable_pv = pvlist
        # print('feeder_class.update_power_factors() controllable_pv: %s' % controllable_pv)

        curr_pf = {}
        pf_ub = {}
        pf_lb = {}
        if prior_pf is None:
            for pv in controllable_pv:
                curr_pf[pv] = self.pf[pv]
                pf_ub[pv] = self.pv[pv].pf_max
                pf_lb[pv] = self.pv[pv].pf_min
        else:
            for pv in controllable_pv:
                curr_pf[pv] = prior_pf[pv]
                pf_ub[pv] = self.pv[pv].pf_max
                pf_lb[pv] = self.pv[pv].pf_min

        change, new_pf, opt_obj, prior_obj = self.DSS.update_power_factors(curr_pf, pv_forecast, p_forecast, q_forecast,
                                                                           pvlist, hour, sec, pf_lb, pf_ub, stepsize,
                                                                           numsteps, options, controllable_pv, base=base)
        if change:
            print('Changing DER PFs!')
            pf = new_pf
            self.pf = pf  # store the PF values in the Feeder object as dict
        else:
            pf = curr_pf

        print('pvlist: %s' % pvlist)
        print('controllable_pv: %s' % controllable_pv)
        print('curr_pf: %s' % curr_pf)
        print('new_pf: %s' % new_pf)
        print('self.pf: %s' % self.pf)
        print('PSO solution, pf: %s' % pf)

        return pf, curr_pf, opt_obj, prior_obj, change
