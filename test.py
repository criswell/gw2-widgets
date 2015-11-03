#! /usr/bin/env python

from __future__ import print_function
from gw2widgets import colors, config
import sys

if len(sys.argv) < 2:
    print("Must be called with a config json file!")
    sys.exit(1)

cfile = sys.argv[1]

header = ''
with open("sample/header.html", "r") as h:
    header = ''.join(h.readlines())
footer = ''
with open("sample/footer.html", "r") as f:
    footer = ''.join(f.readlines())

cfg = config.load_config(cfile)
outdir = cfg['output-dir']

# Start with colors
c = colors.Colors(cfg)
color_html = c.colorize()

with open("{0}/colors.html".format(outdir), "w") as cf:
    cf.write("{0}{1}{2}".format(header, color_html, footer))
