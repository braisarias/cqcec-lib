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

    def __init__(self):

        config = self.read_params()

        self.cache_file = config["name"]
        self.expired_time = config["timeout"]

    def read_params(self):
        import ConfigParser
        cfg = ConfigParser.ConfigParser()
        cfg.read(["config_params.cfg"])
        try:
            timeout = cfg.get("cache", "timeout")
            name = cfg.get("cache", "name")
        except ConfigParser.NoOptionError:
            raise ValueError("There are some missing config params in the " +
                             "configuration file.")
        return {"timeout": timeout, "name": name}

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
                if (c is None):
                    return {}
                (ip_db, info, the_time) = c

                assert(ip == ip_db)

                if int(time()) - the_time > self.expired_time:
                    return {}

                return json.loads(info)
            except sqlite3.OperationalError:
                return {}

    def get_mac_manufacter(self, mac):
        with sqlite3.connect(self.cache_file) as conn:
            try:
                c = conn.execute("SELECT * FROM MACCache WHERE mac=:mac",
                                 {"mac": mac}).fetchone()
                if (c is None):
                    return {}
                (mac_db, vendor) = c

                assert(mac == mac_db)

                return vendor
            except sqlite3.OperationalError:
                return ""

    def set_mac_manufacter(self, mac, manufacter):
        with sqlite3.connect(self.cache_file) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS MACCache (mac text, " +
                      "manufacter text)")
            c.execute("DELETE FROM MACCache WHERE mac=:mac", {"mac": mac})
            c.execute("INSERT INTO MACCache VALUES (:mac, :manufacter)",
                      {"mac": mac, "manufacter": manufacter})
            conn.commit()
