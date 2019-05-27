#!/bin/env python2.7

import pymu.tools as tools
from pymu.pmuDataFrame import DataFrame
import time
import socket
import os
import sys
import math
import pprint

# Create large dictionary of data to collect from PMU stream
LOADS = {'Load1633': {'Bus': 'B09', 'OpenDSSname': 'Load.Load1633', 'Phasors':  ['795D00021-01'], 'phase': [0],  # Section 1
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'PV1': {'Bus': 'B11', 'OpenDSSname': 'PVSystem.PVSy1', 'Phasors': ['794D00105-02'], 'phase': [0, 1, 2],
                   'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         }
'''
LOADS = {'Load1633': {'Bus': 'B09', 'OpenDSSname': 'Load.Load1633', 'Phasors':  ['795D00021-01'], 'phase': [0],  # Section 1
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1615': {'Bus': 'B07', 'OpenDSSname': 'Load.Load1615', 'Phasors':  ['795D00014-01'], 'phase': [0],
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1616': {'Bus': 'B07', 'OpenDSSname': 'Load.Load1615', 'Phasors': ['795D00015-01'], 'phase': [1],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1617': {'Bus': 'B07', 'OpenDSSname': 'Load.Load1615', 'Phasors': ['795D00016-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1612': {'Bus': 'B04', 'OpenDSSname': 'Load.Load1612', 'Phasors': ['795D00045-01'], 'phase': [0],  # Section 2
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1613': {'Bus': 'B04', 'OpenDSSname': 'Load.Load1613', 'Phasors': ['795D00046-01'], 'phase': [1],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1614': {'Bus': 'B04', 'OpenDSSname': 'Load.Load1614', 'Phasors': ['795D00047-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1627': {'Bus': 'B05', 'OpenDSSname': 'Load.Load1627', 'Phasors': ['795D00048-01'], 'phase': [0],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1628': {'Bus': 'B05', 'OpenDSSname': 'Load.Load1628', 'Phasors': ['795D00049-01'], 'phase': [1],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1629': {'Bus': 'B05', 'OpenDSSname': 'Load.Load1629', 'Phasors': ['795D00050-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1630': {'Bus': 'B13', 'OpenDSSname': 'Load.Load1630', 'Phasors': ['795D00051-01'], 'phase': [0],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1631': {'Bus': 'B13', 'OpenDSSname': 'Load.Load1631', 'Phasors': ['795D00052-01'], 'phase': [1],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1632': {'Bus': 'B13', 'OpenDSSname': 'Load.Load1632', 'Phasors': ['795D00053-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1609': {'Bus': 'B06', 'OpenDSSname': 'Load.Load1609', 'Phasors': ['795D00069-01'], 'phase': [0],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1610': {'Bus': 'B06', 'OpenDSSname': 'Load.Load1610', 'Phasors': ['795D00070-01'], 'phase': [1],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1611': {'Bus': 'B06', 'OpenDSSname': 'Load.Load1611', 'Phasors': ['795D00071-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1624': {'Bus': 'B12', 'OpenDSSname': 'Load.Load1624', 'Phasors': ['795D00072-01'], 'phase': [0],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1625': {'Bus': 'B12', 'OpenDSSname': 'Load.Load1625', 'Phasors': ['795D00073-01'], 'phase': [1],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1626': {'Bus': 'B12', 'OpenDSSname': 'Load.Load1626', 'Phasors': ['795D00074-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1618': {'Bus': 'B08', 'OpenDSSname': 'Load.Load1618', 'Phasors': ['795D00092-01'], 'phase': [0], # Section 3
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1619': {'Bus': 'B08', 'OpenDSSname': 'Load.Load1619', 'Phasors': ['795D00093-01'], 'phase': [1],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1620': {'Bus': 'B08', 'OpenDSSname': 'Load.Load1620', 'Phasors': ['795D00094-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1606': {'Bus': 'B09', 'OpenDSSname': 'Load.Load1606', 'Phasors': ['795D00086-01'], 'phase': [0],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1607': {'Bus': 'B09', 'OpenDSSname': 'Load.Load1607', 'Phasors': ['795D00087-01'], 'phase': [1],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1608': {'Bus': 'B09', 'OpenDSSname': 'Load.Load1608', 'Phasors': ['795D00088-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1602': {'Bus': 'B10', 'OpenDSSname': 'Load.Load1602', 'Phasors': ['795D00089-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1603': {'Bus': 'B11', 'OpenDSSname': 'Load.Load1603', 'Phasors': ['795D00102-01'], 'phase': [0],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1604': {'Bus': 'B11', 'OpenDSSname': 'Load.Load1604', 'Phasors': ['795D00103-01'], 'phase': [1],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1605': {'Bus': 'B11', 'OpenDSSname': 'Load.Load1605', 'Phasors': ['795D00104-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1621': {'Bus': 'B02', 'OpenDSSname': 'Load.Load1621', 'Phasors': ['795D00119-01'], 'phase': [0],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1622': {'Bus': 'B02', 'OpenDSSname': 'Load.Load1622', 'Phasors': ['795D00120-01'], 'phase': [1],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1623': {'Bus': 'B02', 'OpenDSSname': 'Load.Load1623', 'Phasors': ['795D00121-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1636': {'Bus': 'B03', 'OpenDSSname': 'Load.Load1636', 'Phasors': ['795D00122-01'], 'phase': [0],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1637': {'Bus': 'B03', 'OpenDSSname': 'Load.Load1637', 'Phasors': ['795D00123-01'], 'phase': [1],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load1638': {'Bus': 'B03', 'OpenDSSname': 'Load.Load1638', 'Phasors': ['795D00124-01'], 'phase': [2],
                      'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'PV869': {'Bus': 'B14', 'OpenDSSname': 'PVSystem.PVSy869', 'Phasors': ['792D00018-02'], 'phase': [0], # Section 1
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

pp = pprint.PrettyPrinter(indent=4)

def csvPrint(dFrame, csv_handle):

    strOut = ""
    for i in range(0, len(dFrame.pmus)):
        strOut += dFrame.soc.formatted + ","
        for j in range(0, len(dFrame.pmus[i].phasors)):
            strOut += str(dFrame.pmus[i].phasors[j].deg) + ","
            # print(str(dFrame.pmus[i].phasors[j].name))
        # for k in range(0, len(dFrame.pmus[i].analogs)):
        #     print(str(dFrame.pmus[i].analogs[k]))
        strOut += str(dFrame.pmus[i].freq) + ","
        strOut += str(dFrame.pmus[i].dfreq)
        if i != (len(dFrame.pmus) - 1):
            strOut += ","
    strOut += "\n"

    csv_handle.write(strOut)

def getNextIndex(originalPath):
    splitArr1 = originalPath.split('_')
    nextIndex = -1
    if len(splitArr1) == 2:
        nextIndex = 1
    elif len(splitArr1) > 2:
        splitArr2 = splitArr1[-1].split('.')
        nextIndex = int(splitArr2[0]) + 1

    if nextIndex <= 0:
        print("# Error creating next csv file from '{}'".format(originalPath))
        sys.exit()

    return nextIndex

def createCsvDir():
    global CSV_DIR
    CSV_DIR = "./data"

    if not os.path.isdir(CSV_DIR):
        os.mkdir(CSV_DIR)

def createCsvFile(confFrame):

    createCsvDir()

    stationName = confFrame.stations[0].stn
    prettyDate = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    csvFileName = "{}_{}.csv".format(prettyDate, stationName.rstrip(' \t\r\n\0'))
    csv_path = "{}/{}".format(CSV_DIR, csvFileName).replace(" ", "")

    print('Saving data in %s' % csv_path)
    if os.path.isfile(csv_path):
        nextIndex = getNextIndex(csv_path)
        csvFileName = "{}_{}.csv".format(prettyDate, nextIndex)
        csv_path = "{}/{}".format(CSV_DIR, csvFileName)

    csv_handle = open(csv_path, 'w')
    csv_handle.write("Timestamp")
    for ch in confFrame.stations[0].channels:
        csv_handle.write(",{}".format(ch.rstrip())) if ch.rstrip() != '' else None
    csv_handle.write(",Freq")
    csv_handle.write(",ROCOF")
    csv_handle.write("\n")

    return csv_handle


def fill_dict_from_dataframes(dFrame=None, LOADS=None):
    for i in range(0, len(dFrame.pmus)):
        pmu_current_count = 0  # hack because GT names are too long, e.g., 'C_B01_B02_2_B01_' i.e., no phase
        for j in range(0, len(dFrame.pmus[i].phasors)):
            ph_name = dFrame.pmus[i].phasors[j].name.rstrip(' \t\r\n\0')
            print('"%s"' % ph_name)
            for bus in LOADS.keys():
                # print(LOADS[bus]['Phasors'])
                if ph_name in LOADS[bus]['Phasors']:
                    print('Hunting for %s. Found %s.' % (bus, ph_name))
                    # Get PMU magnitudes, angles, and units
                    ph_val = dFrame.pmus[i].phasors[j].mag
                    ph_angle = dFrame.pmus[i].phasors[j].deg
                    ph_units = dFrame.pmus[i].phasors[j].voltORCurr[j].voltORcurr

                    phases = LOADS[bus]['phase']

                    for phase in phases:
                        if len(phases) == 3:
                            LOADS[bus]['va_mag'][phase] = ph_val
                            LOADS[bus]['va_deg'][phase] = ph_angle
                        else:
                            LOADS[bus]['va_mag'][phase] = ph_val
                            LOADS[bus]['va_deg'][phase] = ph_angle

                    '''
                    # Place the values of current and voltage in the dict of buses
                    if ph_name[0] == 'B' and ph_name[-1:] == 'A':
                        LOADS[bus]['I_mag'][0] = ph_val
                        LOADS[bus]['I_deg'][0] = ph_angle
                    elif ph_name[0] == 'B' and ph_name[-1:] == 'B':
                        LOADS[bus]['I_mag'][1] = ph_val
                        LOADS[bus]['I_deg'][1] = ph_angle
                    elif ph_name[0] == 'B' and ph_name[-1:] == 'C':
                        LOADS[bus]['I_mag'][2] = ph_val
                        LOADS[bus]['I_deg'][2] = ph_angle
                    elif ph_name[0] == 'V' and ph_name[-2:] == 'AN':
                        LOADS[bus]['V_mag'][0] = ph_val
                        LOADS[bus]['V_deg'][0] = ph_angle
                    elif ph_name[0] == 'V' and ph_name[-2:] == 'BN':
                        LOADS[bus]['V_mag'][1] = ph_val
                        LOADS[bus]['V_deg'][1] = ph_angle
                    elif ph_name[0] == 'V' and ph_name[-2:] == 'CN':
                        LOADS[bus]['V_mag'][2] = ph_val
                        LOADS[bus]['V_deg'][2] = ph_angle
                    else:
                        # print('Phasor: %s is %s %s at /_ %s deg ' % (ph_name, ph_val, ph_units, ph_angle))
                        pass
                    '''

    # Post-process the bus currents and voltages to determine P and Q values for each phase
    for bus in LOADS.keys():
        for phase in range(3):
            # print('Voltage angle: %s' % LOADS[bus]['V_deg'][phase])
            # print('Current angle: %s' % LOADS[bus]['I_deg'][phase])
            # vi_angle = (LOADS[bus]['V_deg'][phase] - LOADS[bus]['I_deg'][phase])*(math.pi/180.)
            vi_angle = LOADS[bus]['va_deg'][phase] * (math.pi / 180.)
            # print('V I Delta angle: %s' % (vi_angle*(180./math.pi)))
            LOADS[bus]['P'][phase] = LOADS[bus]['va_mag'][phase] * math.cos(vi_angle)
            LOADS[bus]['Q'][phase] = LOADS[bus]['va_mag'][phase] * math.sin(vi_angle)


if __name__ == "__main__":

    # Get Config Frame and Establish Client
    confFrame, cli = tools.startDataCapture(idcode=7007, ip="10.50.2.161", port=4125, tcpUdp='TCP', debug=True)
    print('Config Frame for Client 1 Captured!: %s' % confFrame)

    confFrame2, cli2 = tools.startDataCapture(idcode=7008, ip="10.50.2.161", port=4126, tcpUdp='TCP', debug=True)
    print('Config Frame for Client 2 Captured!: %s' % confFrame)

    confFrame3, cli3 = tools.startDataCapture(idcode=7009, ip="10.50.2.161", port=4127, tcpUdp='TCP', debug=True)
    print('Config Frame for Client 2 Captured!: %s' % confFrame)

    RUNNING = True
    p = 0
    CSV_DIR = "./data"
    csv_handle = createCsvFile(confFrame)

    while RUNNING:
        try:
            d = tools.getDataSample(cli, debug=False)
            d2 = tools.getDataSample(cli2, debug=False)
            d3 = tools.getDataSample(cli2, debug=False)
            if d == '' or d2 == '' or d3 == '':
                break
            dFrame = DataFrame(d, confFrame)  # Create dataFrame
            dFrame2 = DataFrame(d2, confFrame2)  # Create dataFrame
            dFrame3 = DataFrame(d3, confFrame3)  # Create dataFrame

            # Save 1 set of the State Estimation data
            csvPrint(dFrame, csv_handle)

            if p == 0:
                print("Data Collection Started...")
                dFrame.dbg = True
                dFrame.parsePmus()
            p += 1
            # print('Datapoint %d, dFrame: %s, ' % (p, dFrame))

            fill_dict_from_dataframes(dFrame=dFrame, LOADS=LOADS)
            fill_dict_from_dataframes(dFrame=dFrame2, LOADS=LOADS)
            fill_dict_from_dataframes(dFrame=dFrame3, LOADS=LOADS)

            # print(LOADS)
            pp.pprint(LOADS)

        except KeyboardInterrupt:
            RUNNING = False
            break
        except socket.timeout:
            print("#{}# Data not available right now...Exiting".format(p))
            break
        except Exception as e:
            print("Exception: {}".format(e))
            break
