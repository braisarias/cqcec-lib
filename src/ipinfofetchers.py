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
            d[str(columnas[0].text)] = str(columnas[1].text)
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
            ret_dic["INetNum Country"] = inetnum_inf["country"]
            ret_dic["INetNum Description"] = inetnum_inf["descr"]
        if route_obj:
            route_info = {x.attributes["name"].value:
                          x.attributes["value"].value for x in
                          route_obj.getElementsByTagName("attribute")}
            ret_dic["Route Network"] = route_info["route"]
        return ret_dic
