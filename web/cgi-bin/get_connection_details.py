#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
from cqcec_lib import ipserviceinfo
import json

if __name__ == '__main__':
    print 'Content-Type: application/json'
    print 'Access-Control-Allow-Origin: *'
    print 'Access-Control-Allow-Methods: GET'
    print ''

arguments = cgi.FieldStorage()

if "ip_origen" not in arguments or "ip_destino" not in arguments:
    print "MERDA!!"

org_info = ipserviceinfo.get_ip_info(arguments["ip_origen"].value)
des_info = ipserviceinfo.get_ip_info(arguments["ip_destino"].value)

org_info = {key: org_info[key] for key in org_info if org_info[key]}
des_info = {key: des_info[key] for key in des_info if des_info[key]}

ret_dic = {"origen": org_info, "destino": des_info}

print json.dumps(ret_dic)
