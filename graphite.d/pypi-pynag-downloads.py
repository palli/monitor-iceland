#!/usr/bin/env python

import requests
import sys

import time
import simplejson as json

url =  'https://pypi.python.org/pypi/pynag/json'
html = requests.get(url).content

json = json.loads(html)

print "pypi.pynag.downloads %i %i" % (
    json.get('urls', [])[0]['downloads'], 
    time.time())
