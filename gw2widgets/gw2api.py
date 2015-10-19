# Simple wrapper for the GW2 rest APIs

import requests

class GW2_API:
    __borg_state = {}
    __api_base = "https://api.guildwars2.com/v2"

    def __init__(self, config):
        self.__dict__ = self.__borg_state
        self.config = config
        self.__header = { "Bearer" : self.config.get('api-key', "") }

    def construct_params(self, params):
        """Construct a params line from a params dict"""
        pline = ""
        if len(params) > 0:
            pline = pline + "?"
            for k in params.keys():
                pline = pline + "{0}={1}&".format(k, params[k])

        return pline

    def get(self, endpoint, params):
        """GW2 Rest API get method.

        Params:
            endpoint = The API endpoint
            params   = A dict containing the parameters to use
        """
        p = self.construct_params(params)
        r = requests.get("{0}/{1}{2}".format(self.__api_base, endpoint, p),
                headers=self.__header)
        return r.json()
