# The Achievements Widgets

from gw2api import GW2_API
from datastore import DataStore
from render import Render

class Achievements:
    __borg_state = {}

    def __init__(self, config):
        self.__dict__ = self.__borg_state
        self.config = config
        self.api = GW2_API(config)
        self.ds = DataStore(config)
        self.render = Render(config)
