#!/usr/bin/env python

# This script screen all the FCP storage groups in complete state in the cpc, run the discover_fcp() method for the storage groups, if the duration exceed the timeout value, it output "timer expired", or else, it output the discover duration.
# If you'd like to designate a single storage group, add this filter in line #30 : "str(sg.get_property('name')) == "A257_Longevity_Shared_XIV_SG" and "
# usage: python3 discoverFcp.py
# create: 2023/8/24
# author: ma, yi jie

import zhmcclient
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

import time

# Set these variables for your environment:
host = "9.12.35.135"
cpc = "A257"
userid = "apiuser"
password = "apiuser"
verify_cert = False
timeout = 600
cnt = 100

session = zhmcclient.Session(host, userid, password, verify_cert=verify_cert)
client = zhmcclient.Client(session)
console = client.consoles.console
cpc = client.cpcs.find_by_name(cpc)

for sg in cpc.list_associated_storage_groups():
    if "A257_Longevity_Shared_XIV_SG" and str(sg.get_property('type')) == "fcp" and str(sg.get_property('fulfillment-state')) == "complete":
        sgName = str(sg.get_property('name'))
        try:
            tBegin = int(time.time())
            sg.discover_fcp(force_restart=False, wait_for_completion=True, operation_timeout=timeout)
            tEnd = int(time.time())

            print (sgName + " LUN discovery takes " + str(tEnd - tBegin) + " seconds.")
        except (Exception) as e:
            print (sgName + " start Fcp Storage Discovery expired !!!")
