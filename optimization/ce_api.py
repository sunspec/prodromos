"""
Simple code for gathering forecasts and adjusting the power factors for multiple DER devices

@author: cwhanse, jjohns2
"""

import requests
from requests.auth import HTTPBasicAuth


class CE_API(object):

    def __init__(self, username=None, password=None):

        self.proxy = {'http': 'http://wwwproxy.sandia.gov:80'}
        self.url = "https://sandia-dm.cnrg.com/api/sandia/pf"
        self.usern = username
        self.passw = password
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
        for der_id, pf_info in self.der.iteritems():
            self.n_der += 1
            # print(der, pf_info)
            setpoint = ({
                         "der_number": der_id,  # e.g., "sunpower2202"
                         "opendss_name": "some name 1",
                         "reactive_power_target": "5000",
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

        auth = HTTPBasicAuth(self.usern, self.passw)
        resp = requests.post(self.url, json=pf_cmd, auth=auth, proxies=self.proxy, headers=self.headers, verify=False)
        print('Data Posted! statusMessage: %s' % resp)

    def get_forecasts(self, der):
        """
        Get the forecasts of DER devices

        :param der: dict of DER devices where the keys are the Connected Energy DER IDs, e.g.,

        der = {"epri1": {'excitation': "injectingQ", 'pf': -0.95, 'forecast': None},
               "epri2": {'excitation': "injectingQ", 'pf': -0.93, 'forecast': None},
               "epri3": {'excitation': "injectingQ", 'pf': -0.88, 'forecast': None}}

        :return: der dict with updated forecasts
        """

        self.der = der

        proxy = {'http': 'http://wwwproxy.sandia.gov:80'}
        url = "https://sandia-dm.cnrg.com/api/pvanalysis/forecast/next"

        for der_id, pf_info in self.der.iteritems():
            payload = {'footprint': der_id}
            headers = {}
            auth = HTTPBasicAuth(self.usern, self.passw)
            resp = requests.get(url, params=payload, auth=auth, proxies=proxy, headers=headers, verify=False)
            self.der[der_id]['forecast'] = resp.content  # add the forecast to the der dict

        return self.der

if __name__ == "__main__":

    username = "fake"
    password = "fake"

    api = CE_API(username=username, password=password)

    der = {"epri1": {'excitation': "injectingQ", 'pf': -0.95, 'forecast': None},  # neg = Q4 (EPRI sign convention)
           "epri2": {'excitation': "injectingQ", 'pf': 0.93, 'forecast': None},
           "epri3": {'excitation': "injectingQ", 'pf': -0.88, 'forecast': None}}

    der = api.get_forecasts(der=der)
    print(der)

    api.set_pf(der=der)


