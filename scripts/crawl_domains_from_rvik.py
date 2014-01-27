#!/usr/bin/env python
#
# Crawl a list of domains from rvik.is
#

import requests
import re
import BeautifulSoup
__author__ = 'palli'


html = requests.get('http://www.rvik.com/ymsir.html').content
soup = BeautifulSoup.BeautifulSoup(html)

links = soup.findAll('a')
hosts = []
for i in links:
    action_url = i['href']
    alias = i.text
    host_name = action_url.replace('http://', '')
    host_name = re.sub('\/.*','', host_name)
    hosts.append(host_name)
    print host_name, action_url, alias


open('/tmp/domainlist','w').write('\n'.join(hosts))