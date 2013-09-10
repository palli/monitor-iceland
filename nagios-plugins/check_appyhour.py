#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script connects to Appy Hour's api and counts how many happy hours are
# currently taking place

import requests
import sys
import simplejson
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

from pynag.Plugins import PluginHelper, ok, unknown

p = PluginHelper()


default_url = 'http://appyhour.herokuapp.com/iceland/'

p.parser.add_option('--url', dest='url', default=default_url)
p.parse_arguments()
p.show_legacy = True
try:
    html = requests.get(p.options.url).content
except Exception, e:
    p.status(unknown)
    p.add_summary("%s error encountered while trying to connect to api hour api: %s" % (type(e), e))
    p.exit()


json = simplejson.loads(html)
total_bars = len(json)
open_bars = 0
now = datetime.datetime.now()
current_day = now.weekday()
current_hour = now.hour

for i in json:
    fields = i['fields']
    start = fields.get('happy_hour_start')
    end = fields.get('happy_hour_end')
    days = fields.get('happy_hour_days')

    # format the data a little bit
    start = int(start)
    end = int(end)
    days = days.split(',')
    days = map(lambda x: int(x), days)

    if current_day in days and start <= current_hour < end:
        open_bars += 1

p.add_metric('total bars', value=total_bars)
p.add_metric('ongoing happy hours', value=open_bars)

p.status(ok)
p.add_summary('%s out of %s bars have an ongoing happy hour' % (open_bars,total_bars))
p.check_all_metrics()
p.exit()
