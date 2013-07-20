#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import sys
import time
import simplejson as json
from BeautifulSoup import BeautifulSoup
import pynag.Plugins
reload(sys)
sys.setdefaultencoding('utf-8')

now = int( time.time() )
default_url =  'http://www.loft.rvk.is/station.jsp?station=02'

p = pynag.Plugins.PluginHelper()
p.parser.add_option('--url', dest='url', default=default_url)
p.parse_arguments()


start_time=time.time()
html = requests.get(p.options.url).content
end_time=time.time()
duration = end_time-start_time
size=len(html)


soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
title = soup.find('h2').text
table = soup.find('table')
if not title or not table:
  p.status(3)
  p.add_summary('Invalid output from remote server')
  p.add_long_output(html)
  p.exit()

title_without_spaces = title.replace(' ','_')

p.add_summary(title)

rows = table.findAll('tr')
for row in rows:
  columns = row.findAll('td')
  if len(columns) != 6:
    continue  # skip headers, etc,
  description = columns[0].text
  metric = columns[1].text
  value = columns[2].text
  value = value.replace(',','.')
  uom = columns[3].text
  # Work around utf-8 issues with pnp4nagios
  #uom = uom.replace('W/m²', 'W_per_square_meter')
  uom = uom.replace('Gráður', 'degrees')
  uom = uom.replace('/', '_per_')
  uom = uom.replace('m³', 'm3')
  uom = uom.replace('m²', 'm2')
  uom = uom.replace('°', '')
  uom = uom.replace('µg', 'mcg')
  
  p.add_long_output('* %s (%s) %s %s' % (description,metric,value,uom)) 
  try:
    float(value)
    p.add_metric(label=metric,value=value,uom=uom)
  except ValueError:
    pass

p.add_metric('time',value=duration,uom='s')
p.add_metric('size',value=size,uom='b')
p.add_summary("%s metrics collected" % (len(p._perfdata.metrics)))
p.status(0)
p.check_all_metrics()
p.exit()
