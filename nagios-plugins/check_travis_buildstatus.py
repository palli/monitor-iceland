#!/usr/bin/python

import pynag.Plugins
import requests
import simplejson as json

default_url = "https://api.travis-ci.org/repositories/pynag/pynag.json"

helper = pynag.Plugins.PluginHelper()

helper.parser.add_option('--url',dest='url',default=default_url)
helper.parse_arguments()

# Check logic starts here
content = requests.get(helper.options.url).content
try:
  json = json.loads(content)
except ValueError,e:
  helper.status(unknown)
  helper.add_summary("Could not decode json from travis servers")
  helper.add_long_output(str(e))
last_build_status = json.get("last_build_status",3)

helper.status(last_build_status)
helper.add_summary("Last build status: %s" % (last_build_status))
#helper.add_metric("example_perfdata=1;2..5;5..10")

# Exit boilerplate
helper.check_all_metrics()
helper.exit()
