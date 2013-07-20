#!/usr/bin/env python
# Check and graph the number of users on einkamal.is


from dateutil.parser import parse
import requests
import sys
import time

from BeautifulSoup import BeautifulSoup
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

reload(sys)
sys.setdefaultencoding('utf-8')



helper = PluginHelper()
helper.parse_arguments()

now = time.time()
url =  'http://www.einkamal.is'
html = requests.get(url).content
soup = BeautifulSoup(html)
tables = soup.find('div', {'class':'welcomemsg'})
p = tables.findAll('p')

li = soup.find('li',{'class':'accounts'})
active_accounts = li.find('b').text
active_accounts = active_accounts.replace('.','')

li = soup.find('li',{'class':'active'})
logged_in = li.find('b').text
logged_in = logged_in.replace('.','')

helper.add_metric('active users', active_accounts)
helper.add_metric('logged in users', logged_in)
helper.status(ok)
helper.add_summary("%s logged in users. %s active accounts" % (logged_in,active_accounts))
helper.exit()

