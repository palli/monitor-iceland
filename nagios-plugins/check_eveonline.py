#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script connects to EVE online API and checks if the game is running



import requests
import string
import random  
import sys
import re
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')


from BeautifulSoup import BeautifulSoup
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

p = PluginHelper()


default_url =  'https://api.eveonline.com/server/ServerStatus.xml.aspx/'

p.parser.add_option('--url', dest='url', default=default_url)
p.parse_arguments()
p.show_legacy = True
try:
    html = requests.get(p.options.url).content
except Exception, e:
    p.status(unknown)
    p.add_summary("%s error encountered while trying to connect to EVE api: %s" % (type(e), e))
    p.exit()

soup = BeautifulSoup(html)

serverOpen = soup.findAll('serveropen')
onlinePlayers = soup.findAll('onlineplayers')

if not serverOpen or not onlinePlayers:
    p.status(unknown)
    p.add_summary("Failed to get all metrics from EVE API")
    p.add_long_output("HTTP request returned:")
    p.add_long_output(html)
    p.exit()



server_status = serverOpen[0].text
num_players = onlinePlayers[0].text

p.add_summary('Server open: %s' % (server_status))

if server_status != 'True':
    p.status(critical)

p.add_metric(label='online players', value=num_players)

p.status(ok)
p.check_all_metrics()
p.exit()

