#!/usr/bin/env python
# This script connects to hraun.vedur.is and
# Graphs all earthquake measures found


from dateutil.parser import parse
import requests
import sys
import time

from BeautifulSoup import BeautifulSoup
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

reload(sys)
sys.setdefaultencoding('utf-8')




url =  'http://hraun.vedur.is/ja/skjalftar/skjlisti.html'
html = requests.get(url).content
soup = BeautifulSoup(html)
tables = soup.findAll('table')
earthquakes = tables[2]
rows = earthquakes.findAll('tr')

header_row = rows.pop(0)
lines = []
for row in rows:
  columns = row.findAll('td')
  str_date = columns[0].text
  str_time = columns[1].text
  latitude = columns[2].text
  longitude = columns[3].text
  depth = columns[4].text
  scale = columns[5].text
  quality = columns[6].text
  distance = columns[7].text.strip()
  direction = columns[8].text 
  location = columns[9].text 

  depth = depth.replace(',','.')
  scale = scale.replace(',','.')
  quality = quality.replace(',','.')
  latitude = latitude.replace(',','.')
  longitude = longitude.replace(',','.')
  distance = distance.replace(',','.') 
  # manipulate location, well.. at least remove spaces
  location = location.replace(' ','_')
  
  datetimestr = str_date + " " + str_time.split(',',1)[0]
  timestamp = time.mktime( parse(datetimestr).timetuple() )
  timestamp = int(timestamp)
  distance = distance.replace(' km','')
  metric = "earthquakes.%skm_%s_%s" % (distance.replace('.','_'),direction,location)
  metric = metric.replace(' ', '').strip('.')
  print "%s.longitude %s %s" % (metric,longitude,timestamp) 
  print "%s.latitude %s %s" % (metric,latitude,timestamp) 
  print "%s.depth %s %s" % (metric,depth,timestamp)
  print "%s.scale %s %s" % (metric,scale,timestamp)
  print "%s.quality %s %s" % (metric,quality,timestamp) 
  print "%s.distance %s %s" % (metric,distance,timestamp) 
 

