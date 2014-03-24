#!/usr/bin/python
# -*- coding: utf-8 -*-

# "Con quien carallo estoy conectado"
# Copyright (C) 2014  Marcos Chavarria Teijeiro.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from cqcec_lib import fetchers
from cqcec_lib import ipserviceinfo
import cgi


def read_hitron_config():
    import ConfigParser
    cfg = ConfigParser.ConfigParser()
    cfg.read(["/etc/cqcec_config.cfg"])

    try:
        usuario = cfg.get("login_hitron", "usuario")
        password = cfg.get("login_hitron", "password")
    except ConfigParser.NoOptionError:
        raise ValueError("Some options were not found at config file.")

    return {"user": usuario, "pass": password}


def get_router_ip():
    import socket
    import struct
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))


def router_connections_info(direction):
    import json
    import socket
    hitron_config = read_hitron_config()
    ip_router = get_router_ip()
    mac_router = ipserviceinfo.get_mac_from_local_ip(ip_router)

    if mac_router[:8] in ("00:26:5b", "68:b6:fc"):
        client = fetchers.HitronConnectionsFetcher(hitron_config["user"],
                                                   hitron_config["pass"],
                                                   ip_router)
    else:
        raise NotImplementedError("Router not supported.")

    connections = []

    for x in client.get_connections():
        if not x.dir == direction:
            continue
        try:
            proto = socket.getservbyport(int(x.port_dest), x.proto.lower())
        except Exception:
            proto = str(x.port_dest) + "/" + str(x.proto.lower())

        connections.append({"ip_origen": x.ip_orig,
                            "ip_dest": x.ip_dest,
                            "proto": proto})

    return json.dumps(connections)

if __name__ == '__main__':
    print 'Content-Type: application/json'
    print 'Access-Control-Allow-Origin: *'
    print 'Access-Control-Allow-Methods: GET'
    print ''

    arguments = cgi.FieldStorage()

    try:
        direct = arguments["direction"].value
        if direct not in ("Outgoing", "Incoming"):
            direct = "Outgoing"
    except:
        direct = "Outgoing"

    try:
        print router_connections_info(direct)
    except Exception, e:
        print e
