# The data storage class
# All data is JSON. JSON is God. JSON loves all.

import json

class DataStore:
    __borg_state = {}

    def __init__(self, config):
        self.__dict__ = self.__borg_state
        self.config = config
        self.__datastore = self.config["data-store"]

    def fname(self, store_id):
        """Return a full filename for a store_id"""
        return "{0}/{1}.json".format(self.__datastore, store_id)

    def get(self, store_id):
        """Given a store ID, get the data from data storage."""
        data = {}
        with open(self.fname(store_id), 'r' as f):
            data = json.load(f)

        return data

    def put(self, store_id, data):
        """Given a store ID, put data into data storage"""
        with open(self.fname(store_id), 'w' as f):
            json.dump(data, f)
