#!/usr/bin/env python
import pynag.Plugins
import pynag.Utils
import socket
__author__ = 'palli'

import dns.resolver


def check_dns(host_name, expected_address=None, expect_authority=False):
    """ Check one specific dns server (wrapper around nagios plugin check_dns)

    Returns a pynag.Utils.PluginOutput instance
    """
    if not expected_address:
        expected_address = socket.gethostbyname(host_name)
    check_command = "/usr/lib64/nagios/plugins/check_dns -H '{host_name}' -A '{expected_address}'"
    code, stdout, stderr = pynag.Utils.runCommand(check_command.format(host_name=host_name, expected_address=expected_address))
    output = pynag.Utils.PluginOutput(stdout)
    output.exit_code = code

    if not output.parsed_perfdata:
        output.parsed_perfdata = pynag.Utils.PerfData()
    else:
        time = output.parsed_perfdata.get_perfdatametric('time')
    return output


def check_many_dns_servers(domain):
    """ Check all nameservers of a single domain. Returns a PluginHelper instance
    """
    pynag.Utils.PluginOutput.parsed_perfdata = pynag.Utils.PerfData()
    helper = pynag.Plugins.PluginHelper()
    helper.add_option("--domain", dest="domain", default="okbeint.is")
    helper.parse_arguments()
    helper.show_legacy = True
    nameservers = dns.resolver.query(helper.options.domain, 'NS')
    nameservers = map(lambda x: str(x), nameservers)
    response_times = []
    helper.add_summary("Checked %s nameservers" % (len(nameservers)))
    if not nameservers:
        return helper
    for i in nameservers:
        pluginoutput = check_dns(i)
        helper.status(pluginoutput.exit_code)
        helper.add_long_output(pluginoutput.summary)
        time = pluginoutput.parsed_perfdata.get_perfdatametric('time')
        time.label = "%stime" % (i)
        response_times.append(float(time.value))
        helper._perfdata.metrics.append(time)
    average_response_time = sum(response_times) / len(response_times)
    helper.add_metric('average response time', average_response_time, uom='s')
    helper.add_metric('highest response time', max(response_times), uom='s', warn="1..inf", crit="2..inf")
    helper.check_all_metrics()
    return helper


helper = check_many_dns_servers('ok.is')
helper.check_all_metrics()
helper.exit()
