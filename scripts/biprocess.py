#!/usr/bin/env python

__author__ = 'palli'

import pprint
import os
import sys
import urlparse
import simplejson

sys.path.append('/opt/pynag')
sys.path.append('/opt/adagios')
from adagios.pnp.functions import run_pnp
import adagios.bi

print "Content-type:text/html\r\n\r\n"

querystring = os.environ.get('QUERY_STRING', '')
kwargs = urlparse.parse_qs(querystring)
process_name = kwargs.get('name', ['ok.is'])[0]
process_type = kwargs.get('type', ['domain'])[0]
if process_name == 'undefined':
    process_name = 'ok.is'
if process_type == 'undefined':
    process_type = 'domain'


process = adagios.bi.get_business_process(process_name, process_type=process_type)

process.data['state'] = process.get_status()
process.data['human_friendly_status'] = process.get_human_friendly_status()

tmp = []
for i in process.get_processes():
    i['state'] = i.get_status()
    i['process_name'] = i.name
    i['process_type'] = i.process_type
    i['human_friendly_status'] = i.get_human_friendly_status()
    i['display_name'] = i._service.get('description').replace('HOSTNAME', process_name)
    tmp.append(i.data)


def get_graph_urls(bp):
    """ Returns a json with urls to all graphs of a specific business process """
    graphs = []
    if not bp.graphs:
        return []
    for graph in bp.graphs or []:
        if graph.get('graph_type') == 'pnp':
            host_name = graph.get('host_name')
            service_description = graph.get('service_description')
            metric_name = graph.get('metric_name')
            pnp_result = run_pnp('json', host=graph.get(
                'host_name'), srv=graph.get('service_description'))
            json_data = simplejson.loads(pnp_result)
            for i in json_data:
                if i.get('ds_name') == graph.get('metric_name'):
                    notes = graph.get('notes')
                    last_value = bp.get_pnp_last_value(
                        host_name, service_description, metric_name)
                    i['last_value'] = last_value
                    i['notes'] = notes
                    graphs.append(i)
    return graphs


process.data['processes'] = tmp
process.data['graph_data'] = get_graph_urls(process)
json_data = simplejson.dumps(process.data, indent=4)
print json_data
