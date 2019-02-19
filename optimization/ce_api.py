"""
Simple code for gathering forecasts and adjusting the power factors for multiple DER devices

@author: cwhanse, jjohns2
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd


class CE_API(object):

    def __init__(self, username=None, password=None):

        self.proxy = {'http': 'http://wwwproxy.sandia.gov:80'}
        self.pf_url = "https://sandia-dm.cnrg.com/api/sandia/pf"
        self.forecast_url = "https://sandia-dm.cnrg.com/api/pvanalysis/forecast/next"
        self.usern = username
        self.passw = password
        self.auth = HTTPBasicAuth(self.usern, self.passw)
        self.headers = {'Content-type': 'application/json'}

        self.n_der = None
        self.der = None

    def set_pf(self, der):
        """
        Set the power factors of DER devices

        :param der: dict of DER devices where the keys are the Connected Energy DER IDs, e.g.,

        der = {"epri1": {'excitation': "injectingQ", 'pf': -0.95, 'forecast': None},
               "epri2": {'excitation': "injectingQ", 'pf': -0.93, 'forecast': None},
               "epri3": {'excitation': "injectingQ", 'pf': -0.88, 'forecast': None}}

        :return: None
        """

        self.der = der
        self.n_der = 0

        setpoints = []
        for der_id, pf_info in self.der.items():
            self.n_der += 1
            # print(der, pf_info)
            setpoint = ({
                         "der_number": der_id,  # e.g., "sunpower2202"
                         "opendss_name": "some name 1",
                         "reactive_power_target": "unknown",
                         "pf_setpoint_magnitude": pf_info["pf"],
                         "excitation": pf_info["excitation"]
                        })

            setpoints.append(setpoint)

        pf_cmd = {"solution_number": "1",
                  "time_stamp": "2018-12-25T15:00:00",
                  "number_of_der": self.n_der,
                  "setpoints": setpoints
                 }

        print(pf_cmd)

        resp = requests.post(self.pf_url, json=pf_cmd, auth=self.auth,
                             proxies=self.proxy, headers=self.headers,
                             verify=False)
        print('Data Posted! statusMessage: %s' % resp)

    def get_forecasts(self, der_ids):
        """
        Get the forecast for a DER device

        :param der_ids: list of str, names of the DER device

        :return forecasts: dict of pandas Series, keys are der_ids
        """

        forecasts = {}
        for der_id in der_ids:
            payload = {'footprint': der_id}
            headers = {}
            resp = requests.get(self.forecast_url, params=payload, 
                                auth=self.auth, proxies=self.proxy,
                                headers=headers, verify=False)
            if resp.status_code == 200:
                points = json.loads(resp.content.decode('utf-8'))
                idx = []
                fc = []
                for p in points:
                    idx.append(pd.to_datetime(p['timestamp'], utc=True))
                    fc.append(p['forecast'])
                forecast = pd.Series(data=fc, index=idx, dtype=float)
                forecasts[der_id] = forecast
        return forecasts


if __name__ == "__main__":

    username = "fake"
    password = "fake"

    api = CE_API(username=username, password=password)

    der = {"epri1": {'excitation': "injectingQ", 'pf': -0.95, 'forecast': None},  # neg = Q4 (EPRI sign convention)
           "epri2": {'excitation': "injectingQ", 'pf': 0.93, 'forecast': None},
           "epri3": {'excitation': "injectingQ", 'pf': -0.88, 'forecast': None},
           "sunpower2201": {'excitation': "injectingQ", 'pf': 1.0, 'forecast': None}}

    fc = api.get_forecasts(der_ids=['sunpower2201'])
    print(fc)

#    api.set_pf(der=der)


