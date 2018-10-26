# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 13:34:29 2018

@author: cwhanse
"""

import inspect
import os
import datetime
from collections import OrderedDict

import numpy as np
from numpy import nan, array
import pandas as pd

import pytest
from pandas.util.testing import assert_series_equal, assert_frame_equal
from numpy.testing import assert_allclose

@pytest.fixture()
def pvdict():
    pvdict['sunpower'] = PVobj('sunpower',
                               dc_capacity=1900,
                               ac_capacity=3000,
                               lat=35.05,
                               lon=-106.54,
                               alt=1657,
                               tz=USMtn,
                               tilt=35,
                               azimuth=180,
                               forecast_method='persistence')
    return pvdict

