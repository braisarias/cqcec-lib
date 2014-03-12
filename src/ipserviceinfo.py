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


import cache
import ipinfofetchers
import portinfofetchers


def get_mac_from_local_ip(ip):
    import subprocess
    try:
        subprocess.check_output(["ping", "-c 1", ip])
    except:
        return ""
    arp_table = subprocess.check_output(["arp", "-an"]).strip().split("\n")
    for line in arp_table:
        fields = line.split(" ")
        if fields[1][1:-1] == ip:
            return fields[3]
    return ""


def get_device_manufacter_from_mac(mac):
    import requests
    url = "http://www.macvendorlookup.com/api/v2/" + mac.replace(":", "-")
    resp = requests.get(url)
    if resp.ok:
        try:
            return str(resp.json()[0][u"company"])
        except:
            pass
    return ""

def get_hostname_from_local_ip(ip):
    return ""


def get_local_ip_info(ip):
    mac = get_mac_from_local_ip(ip)
    mac_vendor = get_device_manufacter_from_mac(mac) if mac else ""
    hostname = get_hostname_from_local_ip(ip)

    return {"ip": ip, "mac": mac, "mac_vendor": mac_vendor,
            "hostname": hostname}


def get_ip_info(ip):
    import sys

    sys.stderr.write("Fetching info about %15s :: " % ip)

    if ip.startswith("10.") or ip.startswith("192.168.") or \
       (ip.startswith("172.") and ip.split(".")[1] in range(16, 31)):
       sys.stderr.write("Done! (LOCAL)\n")
       return get_local_ip_info(ip)

    cachefetcher = cache.Cache()

    info = cachefetcher.get_info(ip)
    if info:
        sys.stderr.write("Done! (CACHE)\n")
        return info
    else:
        lista = []
        lista.append(ipinfofetchers.IPInfoFetcherSenderBase())
        lista.append(ipinfofetchers.IPInfoFetcherRIPE())
        lista.append(ipinfofetchers.IPInfoFetcherWhois())
        lista.append(ipinfofetchers.IPInfoFetcherGSafeBrowsing())

        for fetcher in lista:
            fet_info = fetcher.get_info(ip)
            info = dict(info.items() + fet_info.items())

        cachefetcher.set_info(ip, info)
        sys.stderr.write("Done!\n")
        return info


def get_service_info(port):
    portinfofetcher = portinfofetchers.PortInfoFetcher()
    return portinfofetcher.get_info(port)
