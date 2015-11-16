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

    def _get_current(self):
        """Get the current achievements for the character."""

        cheeves = self.api.get("account/achievements")
        cheeves_by_id = {}
        for cheeve in cheeves:
            cheeves_by_id[cheeve.id] = cheeve

        return cheeves_by_id

    def _get_new_cheeves(self, old_cheeves, new_cheeves):
        """Given a dict of old and new Achievements, find those that are
        newly completed."""

        unlocks = []
        for cheeve in new_cheeves:
            if cheeve.done != old_cheeves[cheeve.id].done:
                unlocks.append(cheeve)
        return unlocks
