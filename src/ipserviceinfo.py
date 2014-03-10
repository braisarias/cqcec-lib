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


def get_ip_info(ip):

    cachefetcher = cache.Cache("cache_db", 60)

    info = cachefetcher.get_info(ip)
    if info:
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
        return info


def get_service_info(port):
    portinfofetcher = portinfofetchers.PortInfoFetcher()
    return portinfofetcher.get_info(port)
