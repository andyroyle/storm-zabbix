storm-zabbix
---

A python script to monitor the health of a storm cluster from zabbix.

Itended to be called from zabbix as a user-parameter.

usage: 
```shell
> storm.py -u username -p password -h https://my-storm-cluster.domain.net -a execute
0.02000
```

```shell
Usage: storm.py [options]

This Zabbix plugin checks the health of a storm cluster.

Options:
  --help                    Show this help message and exit
  -h HOST, --host=HOST      The hostname you want to connect to
  -u USER, --user=USER      The username you want to login as
  -p PASSWD, --pass=PASSWD  The password you want to use for that user
  -a ACTION, --action=ACTION The action you want to take
```

###actions

- `topologies`: count the number of toplogies (int)
- `capacity`: return the highest capacity value from all components (float, 0 = good, 1 = bad)
- `execute`: return the highest execute latency value from all components (float, lower is better)
- `process`: return the highest process latency value from all components (float, lower is better)
- `emitted <componentname>`: return the emitted value from summary for the given component (int)
