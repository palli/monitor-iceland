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



helper = PluginHelper()
helper.parse_arguments()

now = time.time()
url =  'http://hraun.vedur.is/ja/skjalftar/skjlisti.html'
html = requests.get(url).content
soup = BeautifulSoup(html)
tables = soup.findAll('table')
earthquakes = tables[2]
rows = earthquakes.findAll('tr')

header_row = rows.pop(0)
lines = []
recent_earthquakes = 0
major_earthquakes = 0
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
  timesince = now-timestamp
  if timesince > 60*60:  # Less than one hour since earthquake
    continue
  if row.find('ATHUGI') > 0:
    major_earthquakes += 1
  recent_earthquakes += 1
  helper.add_long_output("%s %s: scale=%s depth=%s quality=%s %s %s" % (str_date, str_time, scale, depth, quality, distance, location))

helper.add_summary('%s major earthquakes. %s total earthquakes' % (major_earthquakes, recent_earthquakes))
helper.add_metric('major earthquakes', value=major_earthquakes, crit='1..inf')
helper.add_metric('recent earthquakes', value=recent_earthquakes, warn='3..inf')

helper.check_all_metrics()
helper.exit()
