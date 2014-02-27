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

def get_service_info (port):
	import socket
	return socket.getservbyport(port)

def get_ip_info_senderbase(ip):
	import requests
	from BeautifulSoup import BeautifulSoup
	url =  "http://www.senderbase.org/lookup/?search_string=" + ip
	html_content = requests.get(url).text
	if html_content.find("You must read and agree") != -1:
		payload = {"tos_accepted":"Yes, I Agree"}
		html_content = requests.post(url, data=payload).text
	parsed_html_body = BeautifulSoup(html_content).body
	filas = parsed_html_body.find("table", attrs={'class':'tabular info_table'}).findAll("tr")
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