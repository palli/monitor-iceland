#!/usr/bin/env python
# A plugin to check gamma radiation levels in Iceland
# It fetches eurdep messages from opid-ftp.gr.is
# You need to have eurdep module installed (pip install eurdep)

import sys
from ftplib import FTP
import os
import eurdep
import datetime
import time

datadir="/tmp/eurdep-data"

ftp = FTP('opid-ftp.gr.is')
ftp.login(user='almenningur', passwd='')

result = []
wtf = lambda x: result. append(x)
s = ftp.retrlines('LIST Gammastodvar', callback=result.append)

if not os.path.isdir(datadir):
    os.makedirs(datadir)

def save_file(full_path, data):
    open(full_path, 'a').write(data)
    pass



for i in result:
    if i.startswith('d'):
        continue
    columns = i.split()
    filename = columns.pop()
    full_path = datadir + "/" + filename
    if os.path.isfile(full_path):
        #print filename, "is already here"
        continue
    callback = lambda x: save_file(full_path, x)
    ftp.retrbinary('RETR Gammastodvar/' + filename, callback=callback)


graphite_key = "geislavarnir.gammastodvar"

for filename in os.listdir(datadir)[:]:
    if not filename.startswith('IS'):
        continue
    with open(datadir + "/" + filename) as f:
        data = eurdep.load(f.read())
        for i in data.get('EURDEP', []):
            value = i['RADIOLOGICAL'][0]['field_list'][0]['VALUE']
            end_time = i['RADIOLOGICAL'][0]['field_list'][0]['END']
            locality_code = i['RADIOLOGICAL'][0]['field_list'][0]['LOCALITY_CODE']

            value = float(value)
            timestamp = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%MZ').strftime("%s")


            # We already have location code, lets find location name
            for location in i['LOCALITY'][0]['field_list']:
                if location['LOCALITY_CODE'] == locality_code:
                    location_name = location['LOCALITY_NAME']
                    location_name = location_name.replace(' ', '_')
                    location_name = location_name.replace(' ', '')
                    break
            else:
                location_name = "unknown"
            print "{graphite_key}.{location_name} {value} {timestamp}".format(**locals())





