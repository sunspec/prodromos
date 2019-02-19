#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright (c) 2013 Miguel Moreto <http://sites.google.com/site/miguelmoreto/>

#This file is part of pyComtrade.
#
#    pyComtrade is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    pyComtrade is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyComtrade.  If not, see <http://www.gnu.org/licenses/>.
# ====================================================================
#
# This is an example of using the pyComtrade module to read a comtrade record.

#
__version__ = "$Revision: 7 $" # SVN revision.
__date__ = "$Date: 2013-10-01 18:26:38 -0300 (ter, 01 out 2013) $" # Date of the last SVN revision.

# Matplotlib module is needed for this example.
# pyComtrade needs numpy.
import pyComtrade
# import pylab
import matplotlib.pyplot as pylab

 # Create an instance of the ComtradeRecord class and read the CFG file:
comtradeObj = pyComtrade.ComtradeRecord('LOHO13_REDUCED_LOHOS2.cfg')
print('%s' % comtradeObj.getSamplingRate())

#print comtradeObj.Ach_id # print the ids of the analog channels.

print('Record has %d samples' % (N))
print('Sampling rate is %f samples/sec.' % comtradeObj.getSamplingRate())

# Reading data file:
comtradeObj.ReadDataFile()

# Reading data:
AnalogChannelData1 = comtradeObj.getAnalogChannelData(1)
AnalogChannelData2 = comtradeObj.getAnalogChannelData(3)


with open("RawData.txt", 'w') as f:
    for i in range(len(AnalogChannelData1)):
        f.write(str(AnalogChannelData1[i])+"\n")
    f.close

# Reading time vector:
time = comtradeObj.getTime()

# Ploting with matplotlib
#pylab.plot(time,channelData)
f, axarr = pylab.subplots(2, sharex=True)
f.canvas.set_window_title('Comtrade Data')
axarr[0].plot(time, AnalogChannelData1)
axarr[0].set_title('pyComtrade Demo')
axarr[0].grid()
axarr[1].plot(time, AnalogChannelData2)
#axarr[1].set_ylim(top=1.05) # bottom unchanged
axarr[1].grid()
axarr[1].set_xlabel('Time [s]')
pylab.show()