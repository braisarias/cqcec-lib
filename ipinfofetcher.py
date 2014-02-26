



def get_tag(num):
	try:
		return {0 : 'version_number',
			1 : 'org_name',
			2 : 'org_daily_magnitude',
			3 : 'org_monthly_magnitude',
			4 : 'org_id',
			5 : 'org_category',
			6 : 'org_first_message',
			7 : 'org_domains_count',
			8 : 'org_ip_controlled_count',
			9 : 'org_ip_used_count',
			10 : 'org_fortune_1000',
			20 : 'hostname',
			21 : 'domain_name',
			22 : 'hostname_matches_ip',
			23 : 'domain_daily_magnitude',
			24 : 'domain_monthly_magnitude',
			25 : 'domain_first_message',
			26 : 'domain_rating',
			40 : 'ip_daily_magnitude',
			41 : 'ip_monthly_magnitude',
			43 : 'ip_average_magnitude',
			44 : 'ip_30_day_volume_percent',
			45 : 'ip_in_bonded_sender',
			46 : 'ip_cidr_range',
			47 : 'ip_blacklist_score',
			50 : 'ip_city',
			51 : 'ip_state',
			52 : 'ip_postal_code',
			53 : 'ip_country',
			54 : 'ip_longitude',
			55 : 'ip_latitude'}[num]
	except KeyError:
		return 'unknown(' + str(num) +')'

def get_info(ip):
	import dns.resolver
	url = ip + ".query.senderbase.org"
	print url
	try:
		info = str(dns.resolver.query(url, 'TXT')[0])
	except dns.exception.Timeout:
		return {}
	return {get_tag(int(t.split("=")[0])):t.split("=")[1] for t in info[3:-1].split("|")}

