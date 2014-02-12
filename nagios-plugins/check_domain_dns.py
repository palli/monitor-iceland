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
    check_command = "/usr/lib64/nagios/plugins/check_dns -H '{host_name}' -A '{expected_address}'".format(**locals())
    code, stdout, stderr = pynag.Utils.runCommand(check_command)
    output = pynag.Utils.PluginOutput(stdout)
    output.exit_code = code

    if not output.parsed_perfdata:
        output.parsed_perfdata = pynag.Utils.PerfData()
    else:
        time = output.parsed_perfdata.get_perfdatametric('time')
    return output


def check_many_dns_servers():
    """ Check all nameservers of a single domain. Returns a PluginHelper instance
    """
    pynag.Utils.PluginOutput.parsed_perfdata = pynag.Utils.PerfData()
    nameservers = dns.resolver.query(helper.options.domain, 'NS')
    nameservers = nameservers or []
    nameservers = map(lambda x: str(x), nameservers)
    response_times = []
    for i in nameservers:
        pluginoutput = check_dns(i)
        exit_code = pluginoutput.exit_code
        friendly_code = pynag.Plugins.state_text.get(exit_code, 'Unknown')
        helper.status(pynag.Plugins.state.get(exit_code, 2))
        helper.add_long_output("")
        helper.add_long_output("Checking %s: " % i)
        helper.add_long_output("* Exit code: %s (status=%s)" % (exit_code, friendly_code))
        helper.add_long_output("* Output: %s" % pluginoutput.summary)
        time = pluginoutput.parsed_perfdata.get_perfdatametric('time')
        if not time:
            continue
        time.label = "%stime" % (i)
        response_times.append(float(time.value))
        helper._perfdata.metrics.append(time)
    helper.add_summary("%s out of %s nameservers are responding" % (len(response_times), len(nameservers)))
    if not response_times:
        helper.status(2)
        return
    average_response_time = sum(response_times) / len(response_times)
    helper.add_metric('average response time', average_response_time, uom='s')
    helper.add_metric('highest response time', max(response_times), uom='s', warn="1..inf", crit="2..inf")


helper = pynag.Plugins.PluginHelper()
helper.add_option("--domain", dest="domain", default="example.com")
helper.parse_arguments()
check_many_dns_servers()
helper.check_all_metrics()
helper.exit()
