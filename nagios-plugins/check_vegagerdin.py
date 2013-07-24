#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import string
import random  
import sys
import re
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')


from BeautifulSoup import BeautifulSoup
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

p = PluginHelper()

chars = string.letters + string.digits
randomstring=  ''.join([random.choice(chars) for i in xrange(4)]) # avoid cache
default_url =  'http://www3.vegag.is/faerd/linurit/vedur.htm'
p.parser.add_option('--url', dest='url', default=default_url)
p.parser.add_option('--vedurstod', dest='vedurstod', default=None)
p.show_legacy = True
p.parse_arguments()
html = requests.get(p.options.url).content

# We are going to parse the html and look for lines like these:
#example = """
#<a href="st001.html">Hellisheiði</a>         16.07 22:20 SV   5 ( 7)     7     8 100%  45  6958
#<a href="st031.html">Þrengsli</a>            16.07 22:20 SSV  3 ( 4)     8    11 100%  12  1117
#"""
average_winds = []
max_winds = []
air_temperatures = []
road_temperatures = []
current_traffics = []
total_traffics = []
humidities = []

for i in html.split('\n'):
  soup = BeautifulSoup(i)
  # skip lines in the html that do not have a link in it
  a = soup.find('a')
  if not a:
    continue
  if len(i) != 96 and len(i) != 97:
    continue
  name = a.text
  date = i[45:51].strip()
  time = i[51:57].strip()
  direction = i[57:61].strip()
  average_wind = i[62:64].strip()
  max_wind = i[64:68].strip().strip('(').strip(')').strip()
  air_temperature =  i[69:78].strip()
  road_temperature =  i[78:81].strip()
  humidity =  i[81:85].strip().strip('%')
  current_traffic = i[86:90].strip()
  total_traffic = i[90:].strip()
  
  if max_wind:
    max_winds.append( int(max_wind) )
  if average_wind:
    average_winds.append( int(average_wind) )
  if road_temperature:
    road_temperatures.append( int(road_temperature))
  if air_temperature:
    air_temperatures.append( int(air_temperature))
  if humidity:
    humidities.append( int(humidity) )
  if current_traffic:
    current_traffics.append( int(current_traffic))
  if total_traffic:
    total_traffics.append( int(total_traffic) )



p.add_metric('Average Wind Speed', value=np.mean(average_winds),uom='m_per_s') 
p.add_metric('Max Gust measured', value=max(max_winds),uom='m_per_s') 
p.add_metric('Air temperature', value=np.mean(air_temperatures), uom='celcius')
p.add_metric('Road temperature', value=np.mean(road_temperatures), uom='celcius')
p.add_metric('traffic today', value=sum(total_traffics), uom='c')
p.add_metric('current traffic', value=sum(current_traffics), uom='cars')
p.add_summary('Got metrics from %s weather stations' % ( len(average_winds) ))
p.status(ok)
p.exit()

