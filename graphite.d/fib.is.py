#!/usr/bin/env python
#
# This script connects to fib.is and collect gas prices
# results go to stdout in a graphite compatible way

import requests
import sys

import time
now = int(time.time())
import simplejson as json
reload(sys)
sys.setdefaultencoding('utf-8')


from BeautifulSoup import BeautifulSoup

url = 'http://fib.is'
html = requests.get(url).content
soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)


def print_prices(rows, tag):
    """ Print all prices to stdout """
    for row in rows:
        columns = row.findAll('td')
        price = columns[1].text.replace(',', '.')
        vendor = columns[0].find('a')['title']
        print "fib.%s.%s %s %s" % (tag, vendor, price, now)


bensin = soup.find('table', {'id': 'bensin'})
diesel = soup.find('table', {'id': 'diesel'})

print_prices(bensin.findAll('tr'), 'bensin')
print_prices(bensin.findAll('tr'), 'diesel')
