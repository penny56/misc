#!/usr/bin/env python

# This script update the partition init memory and max memory, the partitions are filtered by part_name_re variable
# create: 2023/12/11
# author: ma, yi jie

import re, time
import zhmcclient
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# Set these variables for your environment:
host = "9.12.35.135"
userid = "apiuser"
password = "apiuser"
verify_cert = False

cpc_name = "A257"
part_name_re = "^A257-(SE-|NVME|LNXT|RHEL|SUSE|SLES|UBUT).*"

linux_memory = 16
kvm_memory = 32

session = zhmcclient.Session(host, userid, password, verify_cert=verify_cert)
client = zhmcclient.Client(session)
console = client.consoles.console

partitions = console.list_permitted_partitions(filter_args={'cpc-name': cpc_name, 'name': part_name_re})

cnt = 0

for part in partitions:
    cpc = part.manager.parent
    print("{} {}".format(cpc.name, part.name))
    
    # Stop the partition.
    if part.properties['status'] == 'active':
        try:
            part.stop(wait_for_completion = True, operation_timeout = 600)
            time.sleep(1)
        except Exception as exc:
            print (exc)

    # modify the partition init and max memory to 16GB/32GB
    partitionTempl = dict()
    if re.search('KVM', part.name) == None:
        partitionTempl['initial-memory'] = linux_memory * 1024
        partitionTempl['maximum-memory'] = linux_memory * 1024
    else:
        partitionTempl['initial-memory'] = kvm_memory * 1024
        partitionTempl['maximum-memory'] = kvm_memory * 1024
    try:
        part.update_properties(partitionTempl)
    except Exception as exc:
        print (exc)

    # start the partition.
    '''
    if part.properties['status'] == 'stopped':
        try:
            time.sleep(1)
            part.start(wait_for_completion = True, operation_timeout = 600)
        except Exception as exc:
            print (exc)
    '''
    cnt += 1
    print(cnt)