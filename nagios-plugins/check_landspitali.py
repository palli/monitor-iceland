#!/usr/bin/env python

import requests
import string
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from BeautifulSoup import BeautifulSoup
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

p = PluginHelper()

chars = string.letters + string.digits
randomstring=  ''.join([random.choice(chars) for i in xrange(4)]) # avoid cache
default_url =  'http://landspitali.is'
p.parser.add_option('--url', dest='url', default=default_url)
p.parse_arguments()
p.check_all_metrics()
p.show_legacy = True
html = requests.get(p.options.url).content
soup = BeautifulSoup(html)
activitylist = soup.find('div', {'class':'activityNumbers activityNumbersNew'})
activities = activitylist.findAll('div', recursive=False)

p.add_metric('metrics_found', value=len(activities), warn='0..1')
p.add_summary('%s metrics found on landspitali website' % (len(activities)))

for i in activities:
  metric_name = i.get('class')
  metric_value = i.find('div', {'class': "todaysCount"}).text
  heading = i.find('div', {'class': 'heading'})
  text = i.find('div', {'class': 'todaysText'})
  
  # If string dag... is found, this is a counter for the whole day
  if 'dag...' in heading.text:
    uom = 'c'
  else:
    uom = ''
  p.add_metric(metric_name, metric_value, uom=uom)
  p.add_long_output("%s: %s %s %s" % (metric_name, heading.text, metric_value, text.text))

  
p.status(ok)
p.exit()

