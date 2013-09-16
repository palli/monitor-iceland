#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import requests

from BeautifulSoup import BeautifulSoup
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

p = PluginHelper()

p.parser.add_option('--url', dest='url', default='http://www.vedur.is')
p.parse_arguments()
html = requests.get(p.options.url).content
soup = BeautifulSoup(html)
warnings = soup.findAll('div', {'class':'warning'})
p.add_summary('%s warnings are being displayed on vedur.is' % len(warnings))
for i in warnings:
  p.status(warning)
  p.add_long_output( i.text )
  
  
p.status(ok)
p.check_all_metrics()
p.exit()

