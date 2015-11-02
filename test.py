#! /usr/bin/env python

from __future__ import print_function
from gw2widgets import colors, config
import sys

if len(sys.argv) < 2:
    print("Must be called with a config json file!")
    sys.exit(1)

cfile = sys.argv[1]

c = colors.Colors(config.load_config(cfile))
c.colorize("test.html")
