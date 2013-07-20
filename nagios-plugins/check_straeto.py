#!/usr/bin/env python

import requests

from BeautifulSoup import BeautifulSoup
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import simplejson as json


p = PluginHelper()

p.parser.add_option('--url', dest='url', default='http://apis.is/bus/realtime')
p.parse_arguments()
html = requests.get(p.options.url).content
json = json.loads(html)

buses_running = len(json['results'])
p.add_metric('buses running', buses_running)
soup = BeautifulSoup(html)
warnings = soup.findAll('div', {'class':'warning'})
p.add_summary('%s buses are currently running' % (buses_running))
for i in warnings:
  p.status(warning)
  p.add_long_output( i.text )
  
  

p.check_all_metrics()
p.exit()

