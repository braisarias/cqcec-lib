

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