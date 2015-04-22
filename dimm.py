#!/usr/bin/env python

import os
import socket
import subprocess

str_hostname = socket.gethostname()

if ".linkedin.com" in str_hostname:
        str_con = str_hostname.replace(".","-con.",1)
else:
        str_con = str_hostname.replace(".","-con.",1)
        str_con += '.linkedin.com'


if 'eat1' in str_hostname:
        fabric_site = 'corp-eat1'
elif 'ltx1' in str_hostname:
        fabric_site = 'prod-ltx1'
elif 'esv4' in str_hostname:
        fabric_site = 'corp-esv4'
elif 'lva1' in str_hostname:
        fabric_site = 'prod-lva1'
elif 'lca1' in str_hostname:
        fabric_site = 'corp-lca1'
elif 'ela4' in str_hostname:
        fabric_site = 'prod-ela4'


app_status_call = ['app-status', '-f', fabric_site, '-H', str_hostname]
getent_call = "getent hosts %s" % str_con
dmi_system_call = "dmidecode -t system"
dmi_memory_call = "dmidecode -t memory"
ipmi_sdr_call = "ipmitool sdr"
mcelog_call =  "mcelog --client"
ps_call = "ps ax"
manufacturer = 'bob'
has_error = False

dmi_memory_out,dmi_memory_errors = subprocess.Popen(dmi_memory_call.split(),stdout=subprocess.PIPE).communicate()
mcelog_out,mcelog_errors = subprocess.Popen(mcelog_call.split(),stdout=subprocess.PIPE).communicate()
dmi_system_out,dmi_system_errors = subprocess.Popen(dmi_system_call.split(),stdout=subprocess.PIPE).communicate()
ipmi_sdr_out,ipmi_sdr_errors = subprocess.Popen(ipmi_sdr_call.split(),stdout=subprocess.PIPE).communicate()
getent_out,getent_errors = subprocess.Popen(getent_call.split(),stdout=subprocess.PIPE).communicate()


for line in dmi_system_out.splitlines():
        if 'Cisco' in line:
                manufacturer = 'Cisco'
        if 'SUN' in line:
                manufacturer = 'SUN'
        if 'Supermicro' in line:
                manufacturer = 'ShittyMicro'

print "\nDo any of my DIMMs have errors? If so, plese fix me I'm dying!"

if manufacturer=='Cisco':
        print "\nThis box is made by %s , so we can check if IPMI reveals my wounds" % manufacturer
        for line in ipmi_sdr_out.splitlines():
                if 'error' in line:
                        print line
                if 'error' in line and ' 0 ' not in line:
                        has_error = True

if not(has_error) or manufacturer=='ShittyMicro':
        print "\nLooks like IPMITOOL isnt't revealing errors, lets try mcelog:"
        if not mcelog_out:
                print "\t Mcelog is empty. are you sure there is a dimm error?"
        else:
                for line in mcelog_out.splitlines():
                     print line
                if manufacturer=='Cisco':
                        print "\nIn case mcelog didn't map DIMMS for you, I'll show you"
                        for line in dmi_memory_out.splitlines():
                                if 'Locator' in line:
                                        print line
"""                                        
                                if 'Clock Speed' in line and 'Unknown' not in line:
                                        print '^^^ DIMM INSTALLED ^^^'

if manufacturer=='ShittyMicro':
        print "\nThis box is made by %s , ipmitool won't help, decipher mcelog for errors:" % manufacturer
        for line in mcelog_out.splitlines():
                        print line

        print "\nIn case mcelog didn't map DIMMS for me, I'll show you just in case:"
        for line in dmi_memory_out.splitlines():
                if 'Locator' in line:
                        print line
"""

print "\nMy Location:"
for line in getent_out.splitlines():
                print line