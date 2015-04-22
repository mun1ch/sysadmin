#!/usr/bin/env python

import os
import socket
import subprocess

ps_call = "ps ax"
range_call = "cat /etc/range_classes.conf"
whatami_call = "cat /etc/cfe.d/whatami"
inops_state = "blah"
my_fabric = "blah"
my_location ="blah"
nothing_running = True
no_range = True
no_apps = True
no_prod = True
no_mysql = True
no_memcache = True
no_couchbase = True
no_java = True
no_agent = True
no_kafka = True
str_hostname = socket.gethostname()

# Find between function
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Grab the host name and fabric
if ".linkedin.com" in str_hostname:
        str_con = str_hostname.replace(".","-con.",1)
else:
        str_con = str_hostname.replace(".","-con.",1)
        str_con += '.linkedin.com'
        str_hostname += '.linkedin.com'

whatami_out,whatami_errors = subprocess.Popen(whatami_call.split(),stdout=subprocess.PIPE).communicate()
for line in whatami_out.splitlines():
        if 'FABRIC_NAME' in line:
                my_fabric = line.split("=")[1]

host_call = ['host', str_con]
getent_call = "getent hosts %s" % str_con
dmi_system_call = "dmidecode -t system"
app_status_call = ['app-status', '-f', my_fabric, '-H', str_hostname]


host_out,host_errors = subprocess.Popen(host_call,stdout=subprocess.PIPE).communicate()
dmi_system_out,dmi_system_errors = subprocess.Popen(dmi_system_call.split(),stdout=subprocess.PIPE).communicate()
app_status_out,app_status_errors = subprocess.Popen(app_status_call,stdout=subprocess.PIPE).communicate()
ps_out,ps_errors = subprocess.Popen(ps_call.split(),stdout=subprocess.PIPE).communicate()
range_out,range_errors = subprocess.Popen(range_call.split(),stdout=subprocess.PIPE).communicate()
getent_out,getent_errors = subprocess.Popen(getent_call.split(),stdout=subprocess.PIPE).communicate()
 
print ("(1) My inops.state and [who|what] I belong to by parsiny my range_classes.conf file:")
for line in range_out.splitlines():
        if 'inops_state' in line:
                no_range = False
                inops_state = line
                print ('\t %s' % line)
        if 'inops_state' in line or 'WAR_GROUPS' in line or 'couchbase' in line or 'memcache' in line or 'mysql' in line:
                no_range = False
                print '\t %s' % line
if '.state.production' in inops_state:
        no_prod = False
if (no_range):
        print "WHOOPS! Looks like my range_classes.conf file doesn't have what we are looking for."

print "\n(2) Searching for apps running on %s network:" % my_fabric
print '\t %s' % app_status_out
for line in app_status_out.splitlines():
        if 'No matches for' or 'agent' in line:
                no_apps = True
        else:
                no_apps = False
                nothing_running = False

print "\n(3) The output of 'ps ax' has the following instances corresponding to apps: (mysql,memcached,couchbase,java)"
for line in ps_out.splitlines():
        if (no_java) and 'java' in line and 'agent' not in line:
                print "\tI'm running java ! Please notify my owner for maintenance. "
                nothing_running = False
                no_java = False
        if (no_memcache) and 'memcache' in line:
                print "\tI'm running MEMCACHE ! Please notify my owner for maintenance. "
                nothing_running = False
                no_memcache = False
        if (no_couchbase) and 'couchbase' in line:
                print "\tI'm running COUCHBASE ! Please notify my owner for maintenance. "
                nothing_running = False
                no_couchbase = False
        if (no_couchbase) and 'mysql' in line:
                print "\tI'm running MYSQL ! Please notify my owner for maintenance. "
                nothing_running = False
                no_mysql = False          
        if (no_kafka) and 'kafka' in line:
                print "\tI'm running KAFKA ! Please notify my owner for maintenance."
                no_kafka = True
        if (no_agent) and 'java' in line and 'agent' in line:
                print "\tI'm running AGENT. You can ignore me, nurse will restart me when I am rebooted."
                no_agent = True
        else:
                pass

if (nothing_running):
        print "\t I lied, no instances, looks like I'm not doing anything :("

print "\n(4) Some things you should know about me:"
for line in dmi_system_out.splitlines():
        if 'Product Name' in line or 'Serial Number' in line or 'Manufacturer' in line:
                print line

print "\n(5) My Location:"
for line in getent_out.splitlines():
        my_location = find_between( line, " ", "-con")
        print '\t%s\n' % my_location

print("no apps: %s") % no_apps
print("no prod: %s") % no_prod
print("no nothing_running: %s") % nothing_running

if (no_apps) and (no_prod) and (nothing_running):
        print "(^_^) Looks like this box:\n\t (1) is not in production (2) has no apps running and (3) 'ps' doesn't have memcache,mysql,couchbase, or java instances.\n ****THE VERDICT**** : You are safe to shutdown the box.\n"
elif (no_apps) and not (no_prod) and (nothing_running):
        print "(^_^) Looks like this box:\n\t (1) is in PRODUCTION (2) has no apps running and (3) 'ps' doesn't have memcache,mysql,couchbase, or java instances.\n ****THE VERDICT**** : No visible services running, but in production. Ask in #maintenance if scheduling down time is necessary.\n"
else:
        print "(^_^) This box has services running on it.\n **THE VERDICT** : You need to schedule maintenance.\n"
