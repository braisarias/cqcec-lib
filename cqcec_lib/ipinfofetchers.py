#!/usr/bin/python
# -*- coding: utf-8 -*-

# "Con quien carallo estoy conectado"
# Copyright (C) 2014  Marcos Chavarría Teijeiro.

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


class IPInfoFetcherSenderBase(object):

    def get_info(self, ip):
        import requests
        from BeautifulSoup import BeautifulSoup
        url = "http://www.senderbase.org/lookup/?search_string=" + ip
        html_content = requests.get(url).text
        if html_content.find("You must read and agree") != -1:
            payload = {"tos_accepted": "Yes, I Agree"}
            html_content = requests.post(url, data=payload).text
        parsed_html_body = BeautifulSoup(html_content).body
        filas = parsed_html_body.find("table", attrs={'class':
                                      'tabular info_table'}).findAll("tr")
        d = {}
        for x in filas:
            columnas = x.findAll("td")
            if len(columnas) != 2:
                continue
            if not columnas[0].text:
                continue
            if columnas[0].find("span"):
                columnas[0].find("span").extract()
            d["SENDERBASE::" + str(columnas[0].text)] = str(columnas[1].text)
        return d


class IPInfoFetcherRIPE(object):
    def get_info(self, ip):
        import urllib2
        from xml.dom import minidom
        ret_dic = {}
        url = "http://rest.db.ripe.net/search.xml?query-string=" + ip
        try:
            xml_text = urllib2.urlopen(url).read()
        except Exception:
            pass
        xmldoc = minidom.parseString(xml_text)
        objs = xmldoc.getElementsByTagName('object')
        objs_dic = {x.attributes["type"].value: x for x in objs}
        try:
            route_obj = objs_dic[u"route"]
        except KeyError:
            route_obj = False
        try:
            inetnum_obj = objs_dic[u"inetnum"]
        except KeyError:
            inetnum_obj = False
        if inetnum_obj:
            inetnum_inf = {x.attributes["name"].value:
                           x.attributes["value"].value for x in
                           inetnum_obj.getElementsByTagName("attribute")}
            ret_dic["RIPE::INetNum_Country"] = inetnum_inf["country"]
            ret_dic["RIPE::INetNum_Description"] = inetnum_inf["descr"]
        if route_obj:
            route_info = {x.attributes["name"].value:
                          x.attributes["value"].value for x in
                          route_obj.getElementsByTagName("attribute")}
            ret_dic["RIPE::Route_Network"] = route_info["route"]
        return ret_dic


class IPInfoFetcherWhois(object):

    def get_info(self, ip):
        import socket
        import whois

        try:
            (host, _, _) = socket.gethostbyaddr(ip)
        except Exception:
            return {}

        try:
            w = whois.whois(host)
        except Exception:
            return {}

        text = w.__dict__["text"]
        d = {}
        for line in text.split("\n"):
            x = line.split(":")
            if len(x) != 2:
                continue
            key = "WHOIS::" + x[0]
            value = x[1].strip()
            if key in d:
                d[key] = d[key] + ", " + value
            else:
                d[key] = value

        return d


class IPInfoFetcherGSafeBrowsing(object):

    def read_params(self):
        import ConfigParser
        cfg = ConfigParser.ConfigParser()
        cfg.read(["/etc/cqcec_config.cfg"])
        try:
            api_key = cfg.get("google_safe_browsing", "api_key")
        except ConfigParser.NoOptionError:
            raise ValueError("The Google Safe Browsing API key is not found " +
                             " in the configuration file.")
        return {"api_key": api_key}

    def get_info(self, ip):
        from safebrowsinglookup import SafebrowsinglookupClient

        config = self.read_params()
        client = SafebrowsinglookupClient(key=config["api_key"])

        res_dic = client.lookup(ip)

        return {"GSB::Status": res_dic[ip]}
