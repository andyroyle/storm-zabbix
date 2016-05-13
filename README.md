storm-zabbix
---

A python script to monitor the health of a storm cluster from zabbix.

usage:
```shell
> storm.py -u username -p password -h my-storm-cluster.domain.net --https
my-storm-cluster.domain.net storm.topolgies 1
my-storm-cluster.domain.net storm.capacity 0.009000
my-storm-cluster.domain.net storm.executeLatency 0.091000
my-storm-cluster.domain.net storm.processLatency 0.00000
```

```shell
> storm.py -u username -p password -h my-storm-cluster.domain.net --https --include-emitted
my-storm-cluster.domain.net storm.topolgies 1
my-storm-cluster.domain.net storm.capacity 0.009000
my-storm-cluster.domain.net storm.executeLatency 0.091000
my-storm-cluster.domain.net storm.processLatency 0.00000
my-storm-cluster.domain.net storm.bolts.mybolt.emitted 3724180
my-storm-cluster.domain.net storm.spouts.myspout.emitted 13416000
```

```shell
Usage: storm.py [options]

This Zabbix plugin checks the health of a storm cluster.

Options:
  --help                show this help message and exit
  -h HOST, --host=HOST  The hostname you want to connect to
  -u USER, --user=USER  The username you want to login as
  -p PASSWD, --pass=PASSWD
                        The password you want to use for that user
  -s, --https           use https to connect to the storm cluster
  -e, --include-emitted
                        Include bolt & spout emit statistics
```
