#!/usr/bin/env python
#
# This script connects to gsmbensin and collect gas prices
# results go to stdout in a graphite compatible way

import requests
import sys

import time
now = int( time.time() )
import simplejson as json
reload(sys)
sys.setdefaultencoding('utf-8')


from BeautifulSoup import BeautifulSoup

base_url =  'http://www.gsmbensin.is/gsmbensin_web.php?region='
regions = ('city','sv','s','a','n','vf','v')

def parse_and_print_table(soup, div_id,region):
	rows = soup.findAll('tr')
	for row in rows:
		columns = row.findAll('td')
		if len(columns) != 3:
			continue
		felag = columns[0].text
		location = columns[1].text
		price = columns[2].text
		#print "gas.prices.%s.%s.%s %s %s" %(div_id,location,felag,price,now)
		metric_name = "gas.regions.%s.%s.%s.%s" % (region,location,felag,div_id)
		metric_name = metric_name.replace(',','_')
		metric_name = metric_name.replace(' ', '_')
		print metric_name,price,now
	
	

for region in regions:
	url = base_url + region
	html = requests.get(url).content
	soup = BeautifulSoup(html)
        header = soup.find('div',{'class':'header'}).text
	okt95 = soup.find('div',{'id':'okt95'})
	disel = soup.find('div',{'id':'disel'})
	parse_and_print_table(okt95, 'okt95',header)
	parse_and_print_table(disel, 'diesel',header)
