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


def get_mac_fom_arp_table(ip):
    import subprocess
    arp_table = subprocess.check_output(["arp", "-an"]).strip().split("\n")
    for line in arp_table:
        fields = line.split(" ")
        if fields[1][1:-1] == ip:
            return fields[3]
    return ""


def _do_ping(ip):
    import subprocess
    import time
    with open("/dev/null") as devnull:
        proc = subprocess.Popen(["ping", "-c 1", ip], stdout=devnull, stderr=devnull)
        t = time.time()
        while time.time() - t < 1.5 and proc.poll() is None:
            pass
        if proc.returncode is None:
            proc.terminate()
            return False
        else:
            return True


def get_mac_from_local_ip(ip):
    mac = get_mac_fom_arp_table(ip)
    if mac != "":
        return mac
    try:
        _do_ping(ip)
    except:
        pass
    return get_mac_fom_arp_table(ip)


def get_device_manufacter_from_mac(mac):
    c = cache.Cache()

    mac_vendor = c.get_mac_manufacter(mac[:8])

    if not mac_vendor:
        mac_vendor = _get_device_manufacter_from_mac(mac)
        c.set_mac_manufacter(mac[:8], mac_vendor)

    return mac_vendor


def _get_device_manufacter_from_mac(mac):
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
    import nmap
    try:
        nm = nmap.PortScanner()
        host = nm.scan(hosts=ip, arguments='-sP')
        return host['scan'][unicode(ip)]['hostname']
    except Exception:
        return None


def get_local_ip_info(ip):
    mac = get_mac_from_local_ip(ip)
    mac_vendor = get_device_manufacter_from_mac(mac) if mac else ""
    hostname = get_hostname_from_local_ip(ip)

    return {"ip": ip, "mac": mac, "mac_vendor": mac_vendor,
            "hostname": hostname}


def get_my_hostname():
    import subprocess
    return subprocess.check_output(["hostname"])


def get_my_info(ip):
    import ifcfg
    int_dic = ifcfg.get_parser().interfaces
    for inte in int_dic:
        if int_dic[inte]["inet"] != ip:
            continue
        return {"ip": ip,
                "mac": int_dic[inte]["ether"],
                "mac_vendor": get_device_manufacter_from_mac(int_dic[inte]["ether"]),
                "hostname": get_my_hostname()}
    return {}


def ip_is_multicast(ip):
    if int(ip.split(".")[0]) in range(224, 240):
        return True
    return False


def ip_is_me(ip):
    import ifcfg
    int_dic = ifcfg.get_parser().interfaces
    ips = [int_dic[x]["inet"] for x in int_dic]
    return ip in filter(lambda x: x is not None, ips)


def ip_is_local(ip):
    if ip.startswith("10."):
        return True
    if ip.startswith("192.168."):
        return True
    if ip.startswith("172.") and ip.split(".")[1] in range(16, 31):
        return True
    return False


def get_ip_info(ip):
    import sys

    if ip_is_me(ip):
        sys.stderr.write("Done! (ME)\n")
        return get_my_info(ip)

    if ip_is_local(ip):
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
