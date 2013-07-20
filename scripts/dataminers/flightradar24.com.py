#!/usr/bin/env python
#
# Connect to http://db8.flightradar24.com/zones/northatlantic_all.js
# and fetch GPS location of all ships near iceland


import requests
import simplejson as json
url= "http://db8.flightradar24.com/zones/northatlantic_all.js"
destination_directory = "/var/www/html/geolocations"
destination_file = destination_directory + "/flights.json"

content = requests.get(url).content

# The data is a json wrapped in a call-back, so something like:
# pd_callback( JSON_DATA );
#

content = content.replace('pd_callback(','')
content = content.replace(');','')

json_data = json.loads(content)

version = json_data.pop('version')
full_count = json_data.pop('full_count')

result = []
for identifier, data in json_data.items():
  f = flight = {}
  f['unixtime'] = data.pop()
  f['friendlyname'] = data.pop()
  f['longitude'] = data.pop(1)
  f['latitude'] = data.pop(1)
  result.append(f)

open(destination_file,'w').write(json.dumps(result, indent=4))
