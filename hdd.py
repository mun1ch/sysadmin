#!/usr/bin/env python

import os
import socket
import subprocess

str_hostname = socket.gethostname()

if "corp" in str_hostname:
        str_con = str_hostname.replace(".corp","-con.corp")
        str_hostname = str_hostname.replace(".corp",".corp.linkedin.com")
else:
        str_con = str_hostname.replace(".prod","-con.prod")
        str_hostname = str_hostname.replace(".prod",".prod.linkedin.com")


host_call = ['host', str_con]
dmi_system_call = "dmidecode -t system"
mdstat_read = " cat /proc/mdstat"
json_read = "cat /etc/locally_attached_storage.json"
smartctl_sda_call = "smartctl -H /dev/sda"
smartctl_sdb_call = "smartctl -H /dev/sdb"

if "corp" in str_hostname:
        str_con = str_hostname.replace(".corp","-con.corp")
        str_hostname = str_hostname.replace(".corp",".corp.linkedin.com")
else:
        str_con = str_hostname.replace(".prod","-con.prod")
        str_hostname = str_hostname.replace(".prod",".prod.linkedin.com")

host_out,host_errors = subprocess.Popen(host_call,stdout=subprocess.PIPE).communicate()
dmi_system_out,dmi_system_errors = subprocess.Popen(dmi_system_call.split(),stdout=subprocess.PIPE).communicate()
mdstat_read_out,mdstat_read_errors = subprocess.Popen(mdstat_read.split(),stdout=subprocess.PIPE).communicate()
smartctl_sdb_call_out,smartctl_sdb_call_errors = subprocess.Popen(smartctl_sdb_call.split(),stdout=subprocess.PIPE).communicate()
smartctl_sda_call_out,smartctl_sda_call_errors = subprocess.Popen(smartctl_sda_call.split(),stdout=subprocess.PIPE).communicate()
json_read_out,json_read_errors = subprocess.Popen(json_read.split(),stdout=subprocess.PIPE).communicate()

print "\nSome information about me:"

for line in host_out.splitlines():
        if 'alias' in line:
                print line

for line in dmi_system_out.splitlines():
        if 'Cisco' in line:
                manufacturer = 'Cisco'
        if 'SUN' in line:
                manufacturer = 'SUN'
        if 'Supermicro' in line:
                manufacturer = 'ShittyMicro'
        if 'Product Name' in line or 'Serial Number' in line or 'Manufacturer' in line:
                print line

print "\nHere are all my arrays, and which partitions from which hard drives belong to those arrays:"

for line in mdstat_read_out.splitlines():
        print line

print "\n/sda HEALTH:"
for line in smartctl_sda_call_out.splitlines():
        if 'ealth' in line:
                print line
        if 'No such device' in line:
                print "The system wasn't able to find a disk in location /sda , it must be UBER fucked or already ejected"

print "/sdb HEALTH:"
for line in smartctl_sdb_call_out.splitlines():
        if 'ealth' in line:
                print line
        if 'No such device' in line:
                print "The system wasn't able to find a disk in location /sdb , it must be UBER fucked or already ejected"

if manufacturer == 'Cisco':
        print "\nPredictive failues & ligh led commands. If missing, the drive has already been ejected or the box can't read from it"
        for line in json_read_out.splitlines():
                if 'light_led' in line or 'logical_name' in line or'predictive_failure_count' in line:
                        print line
elif manufacturer == 'ShittyMicro':
        print "\nLight led commands. If missing, the drive has already been ejected or the box can't read from it."
        for line in json_read_out.splitlines():
                if 'light_led' in line or 'logical_name' in line or'predictive_failure_count' in line:
                        print line
elif manufacturer == 'SUN':
        print "\nPredictive failues & ligh led commands. If missing, the drive has already been ejected or the box can't read from it"
        for line in json_read_out.splitlines():
                if 'light_led' in line or 'logical_name' in line or'uncorrected' in line or 'total_uncorrected_errors' in line:
                        print line

print "\n*****Manual Commands when hardware_failure.py doesn't do the trick.*****\n......\nFAIL a partition: mdadm --manage /dev/mdx --fail /dev/sdxx\nREMOVE FAILED: mdadm --manage /dev/mdx --remove failed\nFORCE partion from /old to new/: sfdisk --dump /dev/sdx | sfdisk --force /dev/sdx\n ADD new partiton to active array: mdadm --manage /dev/mdx --add /dev/sdxx\n STOP erroneously created array: mdadm --stop /dev/mdx\n"

