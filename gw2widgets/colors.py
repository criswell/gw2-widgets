# The Color Widgets

from gw2api import GW2_API
from datastore import DataStore
from render import Render
#import sys, pprint

class Colors:
    __borg_state = {}
    __account_colors_id = "account_colors"
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

        # Find new colors
        new_colors = set(my_colors) - set(old_colors.get('colors', {}))

        # Now, obtain color details on each color
        temp_colors = self.api.get_with_limit("colors",
                { "ids" : my_colors }, "ids", 200)
        listings = self.api.get_with_limit("commerce/listings",
                { "ids" :  [c['item'] for c in temp_colors] }, "ids", 200)
        colors_by_id = {}
        colors_by_set = {}
        for c in temp_colors:
            colors_by_id[c['item']] = c
            cat = c['categories'][-1]
            if cat not in colors_by_set:
                colors_by_set[cat] = []
            colors_by_set[cat].append(c['item'])
        listings_by_id = {}
        for l in listings:
            listings_by_id[l['id']] = l
        #temp_dyes = self.api.get_with_limit("items",
        #        { "ids" : [c['item'] for c in temp_colors] }, "ids", 200)
        data = {}
        color_library = {}
        total_value = 0
        #dye_by_id = {}
        #for d in temp_dyes:
        #    dye_by_id[d['id']] = d

        for rarity in colors_by_set.keys():
            if rarity not in color_library:
                color_library[rarity] = []

            colors_by_set[rarity].sort()
            #print rarity
            #print colors_by_set[rarity]
            for c in colors_by_set[rarity]:
                #print colors_by_id[c]
                cost = 0
                if c in listings_by_id:
                    cost = listings_by_id[c]['sells'][0]['unit_price']
                color_library[rarity].append({
                        "dye" : colors_by_id[c],
                        "price" : cost
                        })
                total_value += cost
                #print cost

        data = {
            'colors' : color_library,
            'value' : total_value
            }

        #print listings_by_id
        #print colors_by_id
        #print dye_by_id
        #pp = pprint.PrettyPrinter(indent=2)
        #pp.pprint(colors_by_set)
        #sys.exit()

        # Finally, render
        self.render.render(self.__color_id, filename, data)
