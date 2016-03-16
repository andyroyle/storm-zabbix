#!/usr/bin/python

import base64
import json
import optparse
import sys
import urllib2

mappings = {
  'topologies': 'topology/summary',
  'topology': 'topology/%(id)s'
}

def getUrl(base, action):
  return '%(base)s/stormui/api/v1/%(action)s' % { 'base': base, 'action': mappings[action] }

def make_request(url, options):
  req = urllib2.Request(url)

  if options.passwd and options.user :
    req.add_header('Authorization', 'Basic ' + base64.b64encode('%(user)s:%(passwd)s' % { 'user': options.user, 'passwd': options.passwd }));

  return json.loads(urllib2.urlopen(req).read())

def main(argv):
  p = optparse.OptionParser(conflict_handler="resolve", description="This Zabbix plugin checks the health of a storm cluster.")

  p.add_option('-h', '--host', action='store', type='string', dest='host', default='127.0.0.1', help='The hostname you want to connect to')
  p.add_option('-u', '--user', action='store', type='string', dest='user', default=None, help='The username you want to login as')
  p.add_option('-p', '--pass', action='store', type='string', dest='passwd', default=None, help='The password you want to use for that user')

  p.add_option('-a', '--action', action='store', type='choice', dest='action', default=None, help='The action you want to take',
		                   choices=['topologies', 'capacity', 'emitted', 'execute', 'process'])

  options, arguments = p.parse_args()

  if options.action == 'topologies':
    return get_topology_count(options)
  elif options.action == 'capacity':
    return get_capacity(options)
  elif options.action == 'emitted':
    return get_emitted(options, arguments[0])
  elif options.action == 'execute':
    return get_execute_latency(options)
  elif options.action == 'process':
    return get_process_latency(options)
  else:
    p.print_help()

def get_topology_count(options):
  url = getUrl(options.host, options.action)
  res = make_request(url, options)
  print len(res['topologies'])

def parse_float(object, fieldname):
  return float(object[fieldname])

def capacity(b):
  return parse_float(b, 'capacity')

def execute_latency(b):
  return parse_float(b, 'executeLatency')

def process_latency(b):
  return parse_float(b, 'processLatency')

def emitted(s):
  return int(s['emitted'])

def get_capacity(options):
  url = getUrl(options.host, 'topologies')
  res = make_request(url, options)
  bolts = []
  for t in res['topologies']:
    top = make_request(getUrl(options.host, 'topology') % { 'id': t['id'] }, options)
    bolts.extend(top['bolts'])
  print '%f' % sorted(list(map(capacity, bolts)))[-1]

def get_execute_latency(options):
  url = getUrl(options.host, 'topologies')
  res = make_request(url, options)
  bolts = []
  for t in res['topologies']:
    top = make_request(getUrl(options.host, 'topology') % { 'id': t['id'] }, options)
    bolts.extend(top['bolts'])
  print '%f' % sorted(list(map(execute_latency, bolts)))[-1]

def get_process_latency(options):
  url = getUrl(options.host, 'topologies')
  res = make_request(url, options)
  bolts = []
  for t in res['topologies']:
    top = make_request(getUrl(options.host, 'topology') % { 'id': t['id'] }, options)
    bolts.extend(top['bolts'])
  print '%f' % sorted(list(map(process_latency, bolts)))[-1]

def get_emitted(options, spout):
  url = getUrl(options.host, 'topologies')
  res = make_request(url, options)
  spouts = []
  for t in res['topologies']:
    top = make_request(getUrl(options.host, 'topology') % { 'id': t['id'] }, options)
    spouts.extend(top['spouts'])
  for s in spouts:
    if s['spoutId'].lower() == spout.lower():
      print int(s['emitted'])

#
# main app
#
if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
