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
        newly unlocked.

        Returns a tuple of:
            (unlocks, newness) where
                    -unlocks is newly completed cheeves
                    -newness is new added cheeves
        """

        unlocks = []
        newness = []
        for cheeve in new_cheeves:
            if cheeve['id'] not in old_cheeves:
                newness.append(cheeve)
            elif cheeve['done'] != old_cheeves[cheeve['id']]['done']:
                unlocks.append(cheeve)
        return (unlocks, newness)

    def _get_new_progress_cheeves(self, old_cheeves, new_cheeves):
        """Given a dict of old and new Achievements, find those that have
        new progress on them."""

        new_prog = []
        for cheeve in new_cheeves:
            if cheeve.get('current', 0) != \
                    old_cheeves[cheeve['id']].get('current', 0):
                new_prog.append(cheeve)

    def update(self, cheeves=None):
        """Will update the datastore with the current cheeves. Intended to be
        called once per day, per week, per cycle (whatever).

        If 'cheeves' is ommitted, will get the current cheevese via API"""

        if cheeves is None:
            cheeves = self._get_current()

        self.ds.put(self.__achievements_id, cheeves)
