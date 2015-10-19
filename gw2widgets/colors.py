# The Color Widgets

from gw2api import GW2_API

class Colors:
    __borg_state = {}

    def __init__(self, config):
        self.__dict__ = self.__borg_state
        self.config = config
        self.api = GW2_API(config)

    def colorize(self):
        """Generate the embedded pages pertaining to an account's colors"""

        # Start by getting all the colors this account has
        my_colors = self.api.get("account/dyes")

        #
