#!/usr/bin/python
# Crawl nameservers from isnic

url = "https://www.isnic.is/is/domain/test"


import requests
import BeautifulSoup
import okconfig
import re
import pynag.Model

html = requests.get('https://www.isnic.is/is/domain/test').content
soup = BeautifulSoup.BeautifulSoup(html)

# There is a select field called "isp" which we use to map from "company number"
# to "comapny name"

select_field = soup.find('select', id='isp')
options = select_field.findAll('option')

companynames = {}
for i in options:
  number = i.get('value')
  name = i.getText()
  companynames[number] = name
  




# The list of nameservers is in a javascript at the bottom of the file
# We know who they are because every line starts with isps[
#
# Example
# 
# isps[67] = new isp('ns0.123.is','ns1.123.is','','');

# Split into lines
lines = html.splitlines()

# Only look at lines starting with isps[
isp_lines = filter(lambda x: x.startswith('isps['), lines)

isp_regex = "^isps.(?P<isp_id>\\d+)..* new isp.'(?P<ns1>.*?)','(?P<ns2>.*?)','(?P<ns3>.*?)','(?P<ns4>.*?)'.;"


hostnames = map(lambda x: x.host_name, pynag.Model.Host.objects.all)
# Lets iterate through 
for isp_line in isp_lines:
  m = re.search(isp_regex, isp_line)
  id = m.group('isp_id')
  ns1 = m.group('ns1')
  ns2 = m.group('ns2')
  ns3 = m.group('ns3')
  ns4 = m.group('ns4')
  #print companynames[id], ns1,ns2,ns3,ns4
  alias = companynames[id].encode('utf-8')
  print str(alias)
  for host in ns1,ns2,ns3,ns4:
    if not host:
      continue  # skip empty hostnames
    elif host in hostnames:
      print host, "already here, skipping"
      continue
    else:
      print host, "not found... adding it...",
      try:
        okconfig.addhost(host_name=host, alias=alias, group_name="nameservers", templates=["dnsserver"])
        print "done"
      except Exception, e:
        print "Could not add host:", e

