#!/usr/bin/env python
#
# Connect to http://api.gulur.is/ and fetch GPS locations of stops and busses


import requests
import simplejson as json
destination_directory = "/var/www/html/geolocations"

url1= "http://api.gulur.is/stops/"
url2= "http://api.gulur.is/buses/?geo=true&latitude=64.12519569999999&longitude=-21.8107866&accuracy=20&range=restOfDay&radius=7500000"
destination_file = destination_directory + "/busstops.json"
destination_file2 = destination_directory + "/buses.json"

content1 = requests.get(url1).content
content2 = requests.get(url2).content


open(destination_file,'w').write( content1 )
open(destination_file2,'w').write( content2 )

