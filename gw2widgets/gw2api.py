# Simple wrapper for the GW2 rest APIs

import requests

class GW2_API:
    __borg_state = {}
    __api_base = "https://api.guildwars2.com/v2"

    def __init__(self, config):
        self.__dict__ = self.__borg_state
        self.config = config
        self.__header = { "Authorization" :
                "Bearer {0}".format(self.config.get('api-key', "")) }

    def construct_params(self, params):
        """Construct a params line from a params dict"""
        pline = ""
        if len(params) > 0:
            pline = pline + "?"
            for k in params.keys():
                pline = pline + "{0}={1}&".format(k, params[k])

        return pline

    def get(self, endpoint, params={}):
        """GW2 Rest API get method.

        Params:
            endpoint = The API endpoint
            params   = A dict containing the parameters to use
        """
        p = self.construct_params(params)
        r = requests.get("{0}/{1}{2}".format(self.__api_base, endpoint, p),
                headers=self.__header)
        return r.json()

    def get_one(self, endpoint, params={}):
        """GW2 Rest API get method for obtaining only one result.

        Params:
            endpoint = The API endpoint
            params   = A dict containing the parameters to use
        """
        r = self.get(endpoint, params)
        if type(r) is list:
            r = r[0]
        return r

    def get_with_limit(self, endpoint, params={}, key=None, limit=200):
        """GW2 Rest API get method, with limit.

        Will wrap the normal get(..) method, but limitting the items in
        params to whatever 'limit' is set to.

        Params:
            endpoint = The API endpoint
            params   = A dict containing the parameters to use
            key      = The key to limit on. If key is None, will just run get()
            limit    = The upper limit on the key
        """
        if key is None:
            return self.get(endpoint, params)

        if len(params[key]) <= limit:
            return self.get(endpoint, params)

        last = 0
        results = []
        for i in range(limit, len(params[key]), limit):
            new_params = params.copy()
            new_params[key] = ",".join(map(str, params[key][last:i-1]))
            results.extend(self.get(endpoint, new_params))
            last = i

        if last < len(params[key]):
            new_params = params.copy()
            new_params[key] = ",".join(map(str, params[key][last:]))
            results.extend(self.get(endpoint, new_params))

        return results
