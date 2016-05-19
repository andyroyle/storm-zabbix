#!/usr/bin/env python

import base64
import json
import optparse
import sys
import urllib2

mappings = {
  'topologies': 'topology/summary',
  'topology': 'topology/%(id)s'
}

def getUrl(base, action, protocol):
  return '%(protocol)s://%(base)s/stormui/api/v1/%(action)s' % { 'protocol': protocol, 'base': base, 'action': mappings[action] }

def make_request(url, options):
  req = urllib2.Request(url)

  if options.passwd and options.user :
    req.add_header('Authorization', 'Basic ' + base64.b64encode('%(user)s:%(passwd)s' % { 'user': options.user, 'passwd': options.passwd }));

  return json.loads(urllib2.urlopen(req).read())

def main(argv):
  p = optparse.OptionParser(conflict_handler="resolve", description="This Zabbix plugin checks the health of a storm cluster.")

  p.add_option('-h', '--host', action='store', type='string', dest='host', default=None, help='The hostname you want to connect to')
  p.add_option('-u', '--user', action='store', type='string', dest='user', default=None, help='The username you want to login as')
  p.add_option('-p', '--pass', action='store', type='string', dest='passwd', default=None, help='The password you want to use for that user')
  p.add_option('-s', '--https', action='store_true', dest='https', help='use https to connect to the storm cluster')
  p.add_option('-e', '--include-emitted', action='store_true', dest='include_emitted', help='Include bolt & spout emit statistics')

  options, arguments = p.parse_args()
  options.protocol = 'https' if options.https else 'http'

  if options.host is None:
    p.print_help()
    return

  topologies = get_topologies(options)
  bolts = get_bolts(topologies, options)
  spouts = get_spouts(topologies, options)

  print_topology_count(topologies, options.host)
  print_capacity(bolts, options.host)
  print_execute_latency(bolts, options.host)
  print_process_latency(bolts, options.host)
  if options.include_emitted:
    print_emitted(bolts, spouts, options.host)

def get_topologies(options):
  url = getUrl(options.host, 'topologies', options.protocol)
  res = make_request(url, options)
  return res['topologies']

def get_bolts(topologies, options):
  bolts = []
  for t in topologies:
    top = make_request(getUrl(options.host, 'topology', options.protocol) % { 'id': t['id'] }, options)
    bolts.extend(top['bolts'])
  return bolts

def get_spouts(topologies, options):
  spouts = []
  for t in topologies:
    top = make_request(getUrl(options.host, 'topology', options.protocol) % { 'id': t['id'] }, options)
    spouts.extend(top['spouts'])
  return spouts

def parse_float(object, fieldname):
  return float(object[fieldname])

def capacity(b):
  return parse_float(b, 'capacity')

def execute_latency(b):
  return parse_float(b, 'executeLatency')

def process_latency(b):
  return parse_float(b, 'processLatency')

def print_topology_count(topologies, host):
  print '%s storm.topologies %i' % (host, len(topologies))

def print_capacity(bolts, host):
  print '%s storm.capacity %f' % (host, sorted(list(map(capacity, bolts)))[-1])

def print_execute_latency(bolts, host):
  print '%s storm.executeLatency %f' % (host, sorted(list(map(execute_latency, bolts)))[-1])

def print_process_latency(bolts, host):
  print '%s storm.processLatency %f' % (host, sorted(list(map(process_latency, bolts)))[-1])

def print_emitted(bolts, spouts, host):
  for b in bolts:
    print '%(host)s storm.bolts.%(boltName)s.emitted %(emitted)i' % { 'host': host, 'boltName': b['boltId'].lower(), 'emitted': int(b['emitted']) }

  for s in spouts:
    print '%(host)s storm.spouts.%(spoutName)s.emitted %(emitted)i' % { 'host': host, 'spoutName': s['spoutId'].lower(), 'emitted': int(s['emitted']) }

#
# main app
#
if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
