#!/usr/bin/env python
# This script connects to landspitali.is and collects all metrics
# presented in the "activityNumbers" part of the page
# 

import requests
import sys
import time
from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

url =  'http://landspitali.is'
html = requests.get(url).content

soup = BeautifulSoup(html)
activitylist = soup.find('div', {'class':'activityNumbers activityNumbersNew'})
activities = activitylist.findAll('div', recursive=False)

now = int( time.time() )

for i in activities:
  metric_name = i.get('class')
  metric_value = i.find('div', {'class': "todaysCount"}).text
  heading = i.find('div', {'class': 'heading'})
  text = i.find('div', {'class': 'todaysText'})
  
  print 'landspitali.%s %s %d' %(metric_name, metric_value, now)
