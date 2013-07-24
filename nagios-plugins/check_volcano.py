#!/usr/bin/env python
# 
# This script check volcano eruption status in iceland 
#
#

from PIL import Image
from collections import defaultdict
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import requests
import cStringIO


url = 'http://hraun.vedur.is/ja/eldgos/volcano_status.png'

p = PluginHelper()
p.parse_arguments()
p.show_legacy = True

tmp = requests.get(url)
image_file = cStringIO.StringIO(tmp.content)

image = Image.open(image_file)

p.add_summary("Volcano data last updated: %s." % (tmp.headers['last-modified']))

width = image.size[0]
height = image.size[1]


colormap = defaultdict(int)

for y in range(0, width):
  for x in range(0, height):
    xy = (x,y)
    rgb = image.getpixel(xy)
    colormap[rgb] += 1


pixels_per_triangle = 251 # How many pixels are in an triangle
grey = (110,110,110)
green = (0,255,0)
yellow = (255,255,0)
orange = (255,140,0)
red = (255,0,0)

grey = colormap.get(grey)
green = colormap.get(green)
yellow = colormap.get(yellow)
orange = colormap.get(orange)
red = colormap.get(red)

p.status(ok)

# Typical metrics: 'grey'=1553;;;; 'green'=16732;;;; 'yellow'=237;;;; 'orange'=232;;;; 'red'=251;;;;

p.add_metric('grey', grey)
p.add_metric('green', green)
p.add_metric('yellow', yellow, warn="240..inf")
p.add_metric('orange', orange,crit="240..inf")
p.add_metric('red', red,crit="260..inf")

p.check_all_metrics()
p.exit()
