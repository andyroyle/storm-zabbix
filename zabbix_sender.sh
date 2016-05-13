#!/bin/bash
dirBase="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
datasend_zabbix="$dirBase/dataSend_zabbix_$2.conf"
storminfo=`$dirBase/storm.py -h $2 -u $3 -p $4 -s`

echo "$storminfo" > $datasend_zabbix
zabbix_sender -z $1 -i $datasend_zabbix
