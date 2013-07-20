#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script will discover a top 100 websites according to veflistinn.is
#

import requests
from BeautifulSoup import BeautifulSoup
html = requests.get('http://veflistinn.is').content

soup = BeautifulSoup(html)

table = soup.find('table',id='samvef-list')

hosts = table.findAll('td',{'class':'alignleft web'})
pynaghosts = []
import pynag.Model

for i in hosts:
  host_name = i.text.split()[0]
  host_name = host_name.replace('/...','')
  if host_name.startswith('str'):
    host_name = 'straeto.is'
  
  alias = i.findNext('td').text.encode('utf-8')
  host = pynag.Model.Host.objects.get_by_shortname(host_name)
  if host.alias != alias:
    host.alias = alias
    host.save()
  url = i.find('a')['href'].encode('utf-8')
  if host.action_url != url:
    host.action_url = url
    host.save()
  #print host_name,alias  

  


