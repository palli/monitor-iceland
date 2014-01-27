#!/usr/bin/env python
#
# Take in a list of domain names and create appropriate http/mx/dns checks for that host
#
domain_list = open("/tmp/domainlist")
destination_dir = "/etc/nagios/okconfig/hosts/domains"


import socket
import os.path
import pynag.Model
import requests
import okconfig.network_scan

for i in domain_list:
    if os.path.isfile("%s/%s.cfg" % (destination_dir, i)):
        continue
    address = socket.gethostbyname(i)
    address2 = socket.gethostbyname("www.%s" % i)

    str_buffer = ''
    host = pynag.Model.Host(host_name=i, address=i, use="generic-domain")
    host.action_url = "http://%s" % i
    host.hostgroups = 'domains,nameservers,mailservers'
    # Add http check
    if okconfig.network_scan.check_tcp(address, 80):
        host.hostgroups += ',http-servers'
        #url = "http://%s" % i
        #service = pynag.Model.Service(host_name=i)
        #service.service_description = url
        #service.action_url = url
        #service.use = "okc-check_http"
        #str_buffer += str(service)
    # Add https check
    if okconfig.network_scan.check_tcp(address, 443):
        host.hostgroups += ',https-servers'
        #url = "https://%s" % i
        #service = pynag.Model.Service(host_name=i)
        #service.service_description = url
        #service.action_url = url
        #service.use = "okc-check_https"
        #str_buffer += str(service)

        #service = pynag.Model.Service(host_name=i)
        #service.use = "okc-check_https_certificate"
        #service.service_description = "ssl certificate"
        #service.action_url = url
    # Add nameserver check

    str_buffer += str(host)

    print str_buffer
    break


