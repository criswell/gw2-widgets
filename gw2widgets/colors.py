# The Color Widgets

from gw2api import GW2_API
from datastore import DataStore

class Colors:
    __borg_state = {}
    __account_colors_id = "account_colors"

    def __init__(self, config):
        self.__dict__ = self.__borg_state
        self.config = config
        self.api = GW2_API(config)
        self.ds = DataStore(config)

    def colorize(self):
        """Generate the embedded pages pertaining to an account's colors"""

        # Start by getting all the colors this account has
        my_colors = self.api.get("account/dyes")

        # Now, load previous color data
        old_colors = self.ds.get(self.__account_colors_id)

        # Find new colors
        new_colors = set(my_colors) - set(old_colors.get('colors', {}))

        # Now, obtain color details on each color
        temp_colors = self.api.get_with_limit("colors",
                { "ids" : my_colors }, "ids", 200)
        listings = self.api.get_with_limit("commerce/listings",
                { "ids" :  [c['item'] for c in temp_colors] }, "ids", 200)
        colors_by_id = {}
        for c in temp_colors:
            colors_by_id[c['item']] = c
        listings_by_id = {}
        for l in listings:
            listings_by_id[l['item']] = l
        temp_dyes = self.api.get_with_limit("items",
                { "ids" : [c['item'] for c in temp_colors] }, "ids", 200)
        dye_by_id = {}
        for d in temp_dyes:
            dye_by_id[d['id']] = d

        # Finally, render
