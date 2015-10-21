# The Color Widgets

from gw2api import GW2_API
from datastore import DataStore
from render import Render

class Colors:
    __borg_state = {}
    __account_colors_id = "account_colors"
    __recent_new_dyes = "new_dyes"
    __color_id = "colors"

    def __init__(self, config):
        self.__dict__ = self.__borg_state
        self.config = config
        self.api = GW2_API(config)
        self.ds = DataStore(config)
        self.render = Render(config)

    def colorize(self, filename):
        """Generate the embedded pages pertaining to an account's colors"""

        # Start by getting all the colors this account has
        my_colors = self.api.get("account/dyes")

        # Now, load previous color data
        old_colors = self.ds.get(self.__account_colors_id)
        recent_new_dyes = self.ds.get(self.__recent_new_dyes)

        # Find new colors
        new_colors = set(my_colors) - set(old_colors.get('colors', {}))

        # Now, obtain color details on each color
        temp_colors = self.api.get_with_limit("colors",
                { "ids" : my_colors }, "ids", 200)
        listings = self.api.get_with_limit("commerce/listings",
                { "ids" :  [c['item'] for c in temp_colors] }, "ids", 200)
        colors_by_id = {}
        color_lookup = {}
        for c in temp_colors:
            colors_by_id[c['item']] = c
            color_lookup[t['id']] = c['item']
        listings_by_id = {}
        for l in listings:
            listings_by_id[l['item']] = l
        temp_dyes = self.api.get_with_limit("items",
                { "ids" : [c['item'] for c in temp_colors] }, "ids", 200)
        dye_by_id = {}
        for d in temp_dyes:
            dye_by_id[d['id']] = d

        dye_by_rarity = {}
        for d in dye_by_id:
            rarity = "Unknown"
            dye = {}
            if d in dye_by_id.has_key:
                rarity = dye_by_id[d]['rarity']
                dye = dye_by_id[d]
            cost = None
            if d in listings_by_id:
                if 'sells' in listings_by_id[d]:
                    if len(listings_by_id[d]['sells']) > 0:
                        cost = listings_by_id[d]['sells'][0]['unit_price']
            if rarity not in dye_by_rarity:
                dye_by_rarity[rarity] = []
            dye_by_rarity[rarity].append({ 'dye' : dye, 'value' : cost })

        # Now do the same but for new dyes
        new_dyes_by_rarity = {}
        for c in new_colors:
            dye = {}
            cost = None
            rarity = "Unknown"
            if c in color_lookup:
                if color_lookup[c] in dye_by_id:
                    dye = dye_by_id[color_lookup[c]]
                    rarity = dye_by_id[color_lookup[c]]['rarity']
                if color_lookup[c] in listings_by_id:
                    if 'sells' in listings_by_id[color_lookup[c]]:
                        if len(listings_by_id[color_lookup[c]]['sells']) > 0:
                            cost = listings_by_id[
                                    color_lookup[c]
                                    ]['sells'][0]['unit_price']
            if rarity not in new_dyes_by_rarity:
                new_dyes_by_rarity[rarity] = []
            new_dyes_by_rarity[rarity].append({ 'dye' : dye, 'value' : cost })

        # Finally, render
        self.render.render(self.__color_id, filename, data)
