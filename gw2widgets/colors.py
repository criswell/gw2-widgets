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
        data = {}
        color_library = {}
        total_value = 0

        rarities = []
        for rarity in colors_by_set.keys():
            if rarity not in color_library:
                color_library[rarity] = []
            if rarity not in rarities:
                rarities.append(rarity)

            colors_by_set[rarity].sort()
            for c in colors_by_set[rarity]:
                cost = 0
                if c in listings_by_id:
                    cost = listings_by_id[c]['sells'][0]['unit_price']
                color_library[rarity].append({
                        "dye" : colors_by_id[c],
                        "price" : cost
                        })
                total_value += cost

        # Hackish way to ensure we sort rarities right
        rarities_sorted = []
        if "Starter" in rarities:
            rarities_sorted.append("Starter")
            rarities.remove("Starter")
        if "Common" in rarities:
            rarities_sorted.append("Common")
            rarities.remove("Common")
        if "Uncommon" in rarities:
            rarities_sorted.append("Uncommon")
            rarities.remove("Uncommon")
        if "Rare" in rarities:
            rarities_sorted.append("Rare")
            rarities.remove("Rare")
        if len(rarities) > 0:
            rarities.sort()
            rarities_sorted.extend(rarities)

        data = {
            'colors' : color_library,
            'value' : total_value,
            'rarities' : rarities_sorted
            }

        # Finally, render
        return self.render.render(self.__color_id, data)
