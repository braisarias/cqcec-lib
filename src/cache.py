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

import sqlite3
import json
from time import time


class Cache(object):

    def __init__(self, cache_file, expired_time):
        self.cache_file = cache_file
        self.expired_time = expired_time

    def set_info(self, ip, info):
        with sqlite3.connect(self.cache_file) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS IPCache (ip text, " +
                      "info text, time int)")
            c.execute("DELETE FROM IPCache WHERE ip=:ip", {"ip": ip})
            c.execute("INSERT INTO IPCache VALUES (:ip, :info, :time)",
                      {"ip": ip, "info": json.dumps(info), "time":
                       int(time())})
            conn.commit()

    def get_info(self, ip):
        with sqlite3.connect(self.cache_file) as conn:
            try:
                c = conn.execute("SELECT * FROM IPCache WHERE ip=:ip", {"ip":
                                 ip}).fetchone()
                return {}
                (ip_db, info, the_time) = c

                assert(ip == ip_db)

                if int(time()) - the_time > self.expired_time:
                    return {}

                return json.loads(info)
            except sqlite3.OperationalError, TypeError:
                return {}
