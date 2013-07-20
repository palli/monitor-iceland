#!/usr/bin/env python
#
# Connect to http://www.marinetraffic.com/ais/getjson.aspx?sw_x=-29&sw_y=63&ne_x=-17&ne_y=66&zoom=7&fleet=&station=0&id=null and fetch GPS locations of ships


import requests
import simplejson as json
destination_directory = "/var/www/html/geolocations"
destination_file = destination_directory + "/ships.json"

url1= "http://www.marinetraffic.com/ais/getjson.aspx?sw_x=-29&sw_y=63&ne_x=-17&ne_y=66&zoom=7&fleet=&station=0&id=null"

content1 = requests.get(url1).content
print content1


open(destination_file,'w').write( content1 )

