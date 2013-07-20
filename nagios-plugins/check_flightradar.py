#!/usr/bin/env python
# 
# Get a list of northatlantic airplanes via flightradar
# 
import requests

from BeautifulSoup import BeautifulSoup
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import simplejson as json


p = PluginHelper()

p.parser.add_option('--url', dest='url', default='http://db8.flightradar24.com/zones/northatlantic_all.js?callback=pd_callback&_=1373991753137')
p.parse_arguments()
html = requests.get(p.options.url).content
html = html.replace('pd_callback(','')
html = html.replace(");",'')

json_data = json.loads(html)
flights = json_data.values()

for i in flights:
  #print i
  #print "..."
  pass
p.add_metric('total_airplanes', len(flights), warn="0..1")
p.add_summary('%s airplanes are currently in the air above iceland' % (len(flights)))
  

p.check_all_metrics()
p.exit()

