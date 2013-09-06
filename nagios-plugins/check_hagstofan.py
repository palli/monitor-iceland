#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script collects key figure metrics from hagstofan.is

from pynag.Plugins import PluginHelper, ok, unknown
import requests
from BeautifulSoup import BeautifulSoup

url = 'http://hagstofan.is'

p = PluginHelper()
p.parse_arguments()
p.show_legacy = True

tmp = requests.get(url)
html = tmp.content
soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)

keyfigures_table = soup.find('table', {'class': 'keyfigures_small'})
if not keyfigures_table:
    p.exit(unknown, "Could not find any table with class=keyfigures_small'")
rows = keyfigures_table.findAll('tr')

for row in rows:
    textdata = row.find('td', {'class': 'textdata'})
    numberdata = row.find('td', {'class': 'numberdata'})

    if not textdata or not numberdata:
        continue
    # Get the text content out of the <td> cells
    textdata = textdata.text
    numberdata = numberdata.text

    # clear some formatting
    numberdata = numberdata.replace('.', '').replace(',', '')

    # Add the keyfigure data to longoutput
    output = "%-30s %s" % (textdata, numberdata)
    p.add_long_output(output)

    # Now lets find those keyfigures, the content of textdata is dynamic so
    # some guesswork is required
    if 'Mannfj' in textdata:
        p.add_metric(label="mannfjoldi", value=numberdata)
    elif "Hagv" in textdata:
        p.add_metric(label="hagvoxtur", value=numberdata)
    elif "VLF" in textdata:
        p.add_metric("verg landsframleidsla", value=numberdata, uom="Mkr")
    elif "VNV" in textdata:
        p.add_metric(label="VNV", value=numberdata)
    elif "Launav" in textdata:
        p.add_metric(label="launavisitala", value=numberdata)
    elif "Bygg.v" in textdata:
        p.add_metric(label="byggingavisitala", value=numberdata)
    elif "sit. framl" in textdata:
        p.add_metric(label="visitala framleidsluverds", value=numberdata)
    elif "Fiskafli" in textdata:
        p.add_metric(label="fiskafli", value=numberdata, uom="tonn")
    elif "ruskipti" in textdata:
        p.add_metric(label="voruskipti", value=numberdata, uom="Mkr")

summary = "%s metrics collected from hagstofan" % (len(p._perfdata.metrics))
p.add_summary(summary)

p.status(ok)


p.check_all_metrics()
p.exit()
