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

def set_ip_info_cache(ip, info):
	import sqlite3
	import json
	with sqlite3.connect('cache_db') as conn:
		c = conn.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS IPCache (ip text, info text)")
		c.execute("INSERT INTO IPCache VALUES (:ip, :info)", {"ip":ip, "info":json.dumps(info)})
		conn.commit()

def get_ip_info_cache(ip):
	import sqlite3
	import json
	with sqlite3.connect('cache_db') as conn:
		try:
			c = conn.execute("SELECT * FROM IPCache WHERE ip=:ip", {"ip":ip}).fetchone()
			if c == None:
				return {}
			(ip_db, info) = c
		except sqlite3.OperationalError, TypeError:
			return {}
	assert(ip == ip_db)
	return json.loads(info)

