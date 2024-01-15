#!/usr/bin/python3

# This script updates the minimum-ifl-processing-weight to 1 and maximum-ifl-processing-weight to 999, whatever there value before.
# And set the initial-ifl-processing-weight value to the given value.
# create: 2024/1/15
# author: ma, yi jie

import sys
import argparse
import zhmcclient
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# Set these variables for your environment:
host = "9.12.35.134"
userid = "apiuser"
password = "apiuser"
cpc_name = "A90"
verify_cert = False

parser = argparse.ArgumentParser(description="For input options from command.")
parser.add_argument("-partname", type=str, help="The name (case sensitive) of the partition.")
parser.add_argument("-weight", type=int, help="New value (1~999) of the processing weight in the partition.")
args = parser.parse_args()

session = zhmcclient.Session(host, userid, password, verify_cert=verify_cert)
client = zhmcclient.Client(session)
cpc = client.cpcs.find_by_name(cpc_name)


# 1. partition exist in the cpc
try:
    parRet = cpc.partitions.find(name = args.partname)
except Exception as e:
    print("There is no partition {} (case sensitive) inside cpc {}".format(args.partname, cpc_name))
    sys.exit(0)

# 2. partition processor in shared mode
try:
    if parRet.get_property('processor-mode') != "shared":
        print ("Only partitions in shared processor mode can update processor weight.")
        sys.exit(0)
except Exception:
    print ("Exception in parRet.get_property method.")
    sys.exit(0)

# 3. weight value in the range 1~999
if args.weight < 1 or args.weight > 999:
    print ("Processor weight should between 1 and 999!")
    sys.exit(0)


# Update the min, max and the init values.
partitionTempl = dict()
partitionTempl["minimum-ifl-processing-weight"] = 1
partitionTempl["initial-ifl-processing-weight"] = args.weight
partitionTempl["maximum-ifl-processing-weight"] = 999

try:
    parRet.update_properties(partitionTempl)
except Exception as exc:
    print ("Exception in parRet.update_properties method.")
    sys.exit(0)

# Double check
try:
    if parRet.get_property('initial-ifl-processing-weight') != args.weight:
        print ("Update failed.")
        sys.exit(0)
except Exception:
    print ("Exception in parRet.get_property method.")
    sys.exit(0)

print ("SUCCESSFUL.")