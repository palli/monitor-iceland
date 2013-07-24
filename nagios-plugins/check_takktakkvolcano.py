#!/usr/bin/env python

import requests
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from BeautifulSoup import BeautifulSoup
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

p = PluginHelper()

default_url =  'http://www.isanicelandicvolcanoerupting.com'
p.parser.add_option('--url', dest='url', default=default_url)
p.parse_arguments()
p.show_legacy = True
html = requests.get(p.options.url).content
soup = BeautifulSoup(html)

answer = soup.find('h3').text

p.add_summary('Source says: "%s"' % answer)
if 'yes' in answer.lower():
  p.status(warning)
elif 'no' in answer.lower():
  p.status(ok)
else:
  p.status(unknown)

p.check_all_metrics()
p.exit()
