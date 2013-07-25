#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script connects to vedur.is and checks if there is an avalance alert



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

chars = string.letters + string.digits
randomstring=  ''.join([random.choice(chars) for i in xrange(4)]) # avoid cache
default_url =  'http://www.vedur.is/ofanflod/snjoflodaspa'

p.parser.add_option('--url', dest='url', default=default_url)
p.parse_arguments()
p.show_legacy = True
html = requests.get(p.options.url).content

# Initial Status is OK, unless avalanche threats detected.
p.status(ok)

# We are going to parse the html and look for certain divs, according to the vedur.is page
# it should have the following threat codes:
# <div class="lev1"> <!-- Low risk -->
# <div class="lev2"> <!-- some risk-->
# <div class="lev3"> <!-- Considerable risk -->
# <div class="lev4"> <!-- High risk -->
# <div class="lev5"> <!-- Very high risk -->

soup = BeautifulSoup(html)
lev1 = soup.findAll('div', {'class':'lev1'})
lev2 = soup.findAll('div', {'class':'lev2'})
lev3 = soup.findAll('div', {'class':'lev3'})
lev4 = soup.findAll('div', {'class':'lev4'})
lev5 = soup.findAll('div', {'class':'lev5'})

all_levels = (lev1,lev2,lev3,lev4,lev5)
# First a little sanity check, if any of the above divs are not found
# It means the layout of the site has changed so we exit with unknown
for level in all_levels:
  if not level:
    p.add_summary("Could not find a <div class=lev...> .. Layout of vedur.is must have changed")
    p.status(unknown)
    p.exit()

p.add_metric("lev1", len(lev1)-1)
p.add_metric("lev2", len(lev2)-1, warn="1..inf")
p.add_metric("lev3", len(lev3)-1, warn="1..inf")
p.add_metric("lev4", len(lev4)-1, crit="1..inf")
p.add_metric("lev5", len(lev5)-1, crit="1..inf")

total_areas = sum(map(lambda x: len(x), all_levels))
p.add_summary("Avalance statistics successfully gathered for %s areas" % total_areas)
p.status(ok)
p.check_all_metrics()
p.exit()

