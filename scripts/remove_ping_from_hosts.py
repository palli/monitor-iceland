import pynag.Parsers
import pynag.Model

l = pynag.Parsers.mk_livestatus()
downhosts = l.get_hosts('Filter: state != 0')
hostlist = map(lambda x: x.get('name'), downhosts)

for i in hostlist:
  i = i.strip()
  if not i:
    continue  # skip empty lines
  print "changing", i
  host = pynag.Model.Host.objects.get_by_shortname(i)
  if 'nameservers' in host.get_filename():
    host.check_command = "check_dns_server"
  else:
    host.check_command = 'check_http'
  host.save()
  try:
    service = pynag.Model.Service.objects.get_by_shortname("%s/Ping" % (i))
    service.delete()
  except KeyError:
    continue
