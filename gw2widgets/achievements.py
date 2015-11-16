# The Achievements Widgets

from gw2api import GW2_API
from datastore import DataStore
from render import Render

class Achievements:
    __borg_state = {}
    __achievements_id = "account_achievements"

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

    def _get_new_unlock_cheeves(self, old_cheeves, new_cheeves):
        """Given a dict of old and new Achievements, find those that are
        newly unlocked."""

        unlocks = []
        for cheeve in new_cheeves:
            if cheeve.done != old_cheeves[cheeve.id].done:
                unlocks.append(cheeve)
        return unlocks

    def update(self, cheeves=None):
        """Will update the datastore with the current cheeves. Intended to be
        called once per day, per week, per cycle (whatever).

        If 'cheeves' is ommitted, will get the current cheevese via API"""

        if cheeves is None:
            cheeves = self._get_current()

        self.ds.put(self.__achievements_id, cheeves)
