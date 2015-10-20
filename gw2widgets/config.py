# config loader

import json

def load_config(cfile):
    """load a config file, returns the json object"""
    j = {}
    with open(cfile, "r") as f:
        j = json.load(f)
    return j
