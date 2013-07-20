#!/usr/bin/env python

import requests

from BeautifulSoup import BeautifulSoup
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown
import simplejson as json


p = PluginHelper()

p.parser.add_option('--url', dest='url', default='http://api.gulur.is/buses/?geo=true&latitude=64.1251991&longitude=-21.8108419&accuracy=20&range=restOfDay&radius=750000')
p.parse_arguments()
html = requests.get(p.options.url).content
json_data = json.loads(html)

buses_running = len(json_data)
p.add_metric('buses running', buses_running)
p.add_summary('%s buses are currently running' % (buses_running))
  
print json.dumps(json_data[0], indent=4)

p.check_all_metrics()
p.exit()

