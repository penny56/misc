#!/usr/bin/env python

# This script is for the test case: Maximum number of certificates in the system is 100.
# Get the current number of certificate already imported in the cpc
# Get the number of certificate can be imported: (max_number - imported)
# Import the certificates

# usage: python3 importCertificate.py
# create: 2023/10/19
# author: Yi Jie

import zhmcclient
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import random

# Set these variables for your environment:
host = "9.12.35.135"
cpc_name = "A257"
userid = "apiuser"
password = "apiuser"
verify_cert = False
max_imported_cert = 100


session = zhmcclient.Session(host, userid, password, verify_cert=verify_cert)
client = zhmcclient.Client(session)
console = client.consoles.console
cpc = client.cpcs.find_by_name(cpc_name)

# All certs managed by this hmc, include all cpcs. 
# If one cert imported to two cpcs, there will be 2 entities in certsInHmc.
certsInHmc = console.certificates.list()

# All certs imported by this specified cpc == cpc_name.
certsInCpc = set()
for cert in certsInHmc:
    cpc_name_temp = cert.get_properties_local('parent-name')
    if cpc_name_temp == cpc_name:
        certsInCpc.add(cert)

addable = max_imported_cert - len(certsInCpc)

# Do import
certTempl = dict()
certTempl["description"] = "Hi there."
certTempl["type"] = "secure-boot"
certTempl["certificate"] = 'MIIDfzCCAmegAwIBAgIJAO+/FZMoQsoyMA0GCSqGSIb3DQEBCwUAME0xJzAlBgNVBAMTHlJlZCBIYXQgU2VjdXJlIEJvb3QgKENBIGtleSAxKTEiMCAGCSqGSIb3DQEJARYTc2VjYWxlcnRAcmVkaGF0LmNvbTAeFw0xNDExMDcxMDE1MjdaFw0zNzExMDExMDE1MjdaMFIxLDAqBgNVBAMTI1JlZCBIYXQgU2VjdXJlIEJvb3QgKHNpZ25pbmcga2V5IDIpMSIwIAYJKoZIhvcNAQkBFhNzZWNhbGVydEByZWRoYXQuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1zr3ts9B2RE3FJZMHJPKl0VWvYybc/EdttVuS2H29ptfhZ1AzB8ycDFVaad6qTvbOcKRwXkWZXL5670NV4p7YjHFteJayY4farFhykbecNbBli6+uYakD0fKt0cI4O6LxGYWzfTi4O3NCOsreK2QNeSpONNoy6lwLG6mnK0kAiy4HVw1tEpFaGfaodvnBPliuxKI00Ua5r1qRpdXavbJjrpQaWIeZc5y+ey9lamepU+m+gZQHBk77WZkqsI40amgUkg1dmWEg+0sz6jpMyJSMy+4JDhxado8tl8efBfq3yBZOX5iAQO8YzFhZV/HIzlJOS6eyknHDjHcyf/aduTVBwIDAQABo10wWzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIHgDAdBgNVHQ4EFgQUgNWY19ho76rvuWhTSpmz10kNqeYwHwYDVR0jBBgwFoAUQBaEFkTOOoEECAUHZuj4opxl+FwwDQYJKoZIhvcNAQELBQADggEBADMoG/id1x5EHraDCGNuse/6r8GwSIufngPj4GShYJd/rXFVh6jSKgisVekPw7ySGc1TXmWJKyBsY0pkuJlje0rvIPWdk8ONvPb7paKylROZ7VWHMd5zrpbNCnUlmdBG0wKg+hasCn5E25sIDoXl42mwFzBxJblJ07M0mf/Fwd6tkF8/g+8m1gMzRlHXjdE7zYRG71mQNG3kCr/hCrKUxcwaGy2G3zH6lU2f1g9B8iT5tqcrPvtIAGLhlgJEjfH1lAX5M7S17vxrSkyWsut4VMv4DLidabeEusXe/Rc2zymhSO7poVTHCXC2qcfpRbspr5D7zjGnnSG14CQbuevFmY4='

while addable > 0:

    certTempl["name"] = cpc_name + '-' + 'temp' + str(random.randint(0, 99999))
    try:
        cert_obj = console.certificates.import_certificate(cpc, certTempl)
    except Exception as e:
        print (e)
    
    addable -= 1
    print ("addable = " + str(addable))


print ("OK")