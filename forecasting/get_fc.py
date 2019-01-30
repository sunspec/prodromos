# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 14:17:18 2019

@author: cwhanse
"""

import requests
from requests.auth import HTTPBasicAuth

proxy = {'http': 'http://wwwproxy.sandia.gov:80'}
url = "https://sandia-dm.cnrg.com/api/pvanalysis/forecast/next"
usern = "fake"
passw = "fake"
payload = {'footprint': 'sunpower2201'}
headers = {}
auth = HTTPBasicAuth(usern, passw)
r = requests.get(url, params=payload, auth=auth, proxies=proxy, headers=headers, verify=False)

print(r.content)
