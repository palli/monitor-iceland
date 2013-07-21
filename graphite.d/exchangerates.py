#!/usr/bin/env python

import requests
import sys

import time
now = int( time.time() )
import simplejson as json
reload(sys)
sys.setdefaultencoding('utf-8')


from BeautifulSoup import BeautifulSoup

url =  'http://apis.is/currency/m5'
html = requests.get(url).content

json = json.loads(html)

results = json.get('results',[])
for i in results:
  name = i['shortName']
  for k,v in i.items():
    try:
      v = float(v)
    except Exception:
      continue
    print "exchangerates.%s.%s %s %s" % (name,k,v,now)
