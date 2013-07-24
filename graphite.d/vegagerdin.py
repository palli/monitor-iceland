#!/usr/bin/env python

import requests
import string
import random  
import sys
import numpy as np

import socket
import time
now = int( time.time() )
lines =[]


reload(sys)
sys.setdefaultencoding('utf-8')


from BeautifulSoup import BeautifulSoup
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

url =  'http://www3.vegag.is/faerd/linurit/vedur.htm'
html = requests.get(url).content

winds = []
max_winds = []
average_wind = []
avg_temp = []
avg_temp_at_road = []
for i in html.split('\n'):
  soup = BeautifulSoup(i)
  a = soup.find('a')
  if not a:
    continue
 
  name = a.text
  attributes = i.split()
  if len(attributes) == 13:
    attributes.pop(0)
    attributes.pop(0)
    
    date = attributes.pop(0)
    time = attributes.pop(0)
    direction = attributes.pop(0)
    wind = attributes.pop(0)
    max_wind = attributes.pop(0)
    if max_wind == '(':
      max_wind = attributes.pop(0)
    max_wind = max_wind.strip(')').strip('(')
    temperature = attributes.pop(0)
    temperature_at_road = attributes.pop(0)
    humidity = attributes.pop(0)
    traffic_last_10_minutes = attributes.pop(0)
    traffic_today = attributes.pop(0)
    max_winds.append( max_wind )
    winds.append( wind)
    avg_temp.append(wind)
    avg_temp_at_road.append(temperature_at_road)

    name = name.replace(' ','_')
    print 'vegagerdin.%s.wind %s %d' % (name, wind.strip('%'), now) 
    print 'vegagerdin.%s.max_wind %s %d' % (name, max_wind.strip('%'), now) 
    print 'vegagerdin.%s.traffic_last_10_minutes %s %d' % (name, traffic_last_10_minutes, now) 
    print 'vegagerdin.%s.traffic_today %s %d' % (name, traffic_today, now) 
    print 'vegagerdin.%s.temperature %s %d' % (name, temperature, now) 
    print 'vegagerdin.%s.temperature_at_road %s %d' % (name, temperature_at_road, now) 
    print 'vegagerdin.%s.humidity %s %d' % (name, humidity.strip('%'), now) 
    

#avg_temp = map(lambda x: float(x), avg_temp)
#traffic_today = map(lambda x: float(x), traffic_today)
#winds = map(lambda x: float(x), winds)
  
