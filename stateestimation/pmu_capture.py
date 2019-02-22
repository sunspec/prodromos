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
LOADS = {'Load142': {'Bus': 'B09', 'OpenDSSname': 'Load.Load142', 'Phasors':  ['795D00087-01'], 'phase': [0],
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load143': {'Bus': 'B09', 'OpenDSSname': 'Load.Load143', 'Phasors':  ['795D00088-01'], 'phase': [1],
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load144': {'Bus': 'B09', 'OpenDSSname': 'Load.Load144', 'Phasors': ['795D00089-01'], 'phase': [2],
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load133': {'Bus': 'B10', 'OpenDSSname': 'Load.Load133', 'Phasors':  ['795D00090-01'], 'phase': [0],
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load134': {'Bus': 'B10', 'OpenDSSname': 'Load.Load134', 'Phasors':  ['795D00091-01'], 'phase': [1],
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load135': {'Bus': 'B10', 'OpenDSSname': 'Load.Load135', 'Phasors': ['795D00092-01'], 'phase': [2],
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'Load20': {'Bus': 'B04', 'OpenDSSname': 'Load.Load20', 'Phasors': ['796D00097-03'], 'phase': [0, 1, 2],
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'PV1': {'Bus': 'B12', 'OpenDSSname': 'PVSystem.PVSy1', 'Phasors': ['794D00050-02'], 'phase': [0, 1, 2],
                 'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'PV2': {'Bus': 'B14', 'OpenDSSname': 'PVSystem.PVSy2', 'Phasors': ['794D00057-02'], 'phase': [0, 1, 2],
                 'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         'PV3': {'Bus': 'B15', 'OpenDSSname': 'PVSystem.PVSy3', 'Phasors': ['794D00084-02'], 'phase': [0, 1, 2],
                    'va_mag': [0., 0., 0.], 'va_deg': [0., 0., 0.], 'P': [0., 0., 0.], 'Q': [0., 0., 0.]},
         }

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
            # print('"%s"' % ph_name)
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

    RUNNING = True
    p = 0
    CSV_DIR = "./data"
    csv_handle = createCsvFile(confFrame)

    while RUNNING:
        try:
            d = tools.getDataSample(cli, debug=False)
            d2 = tools.getDataSample(cli2, debug=False)
            if d == '' or d2 == '':
                break
            dFrame = DataFrame(d, confFrame)  # Create dataFrame
            dFrame2 = DataFrame(d2, confFrame2)  # Create dataFrame

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
