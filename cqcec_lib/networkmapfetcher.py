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


class HitronNetworkMapFetcher(object):

    def __init__(self, user, password, host):
        self.user = user
        self.password = password
        self.host = host

    def get_telnet_dump(self):
        from telnetlib import Telnet
        USERNAME_TELNET_STRING = "Username:"
        PASSWORD_TELNET_STRING = "Password:"
        tn = Telnet(self.host)
        tn.read_until(USERNAME_TELNET_STRING)
        tn.write(self.user + "\n")
        tn.read_until(PASSWORD_TELNET_STRING)
        tn.write(self.password + "\n\n")
        if "wifimedia-R" not in tn.read_until("wifimedia-R", 1):
            raise EnvironmentError("Not able to fetch connections " +
                                   "from Hitron.")
        tn.write("conf\n\n")
        tn.write("cliprint /dev\n")
        text = tn.read_until("Returned")
        tn.write("exit\n\nexit\n")
        return text

    def get_networkmap(self):
        import re
        HITRON_REGEXP = r"conf set \"dev/(.+)/dhcps/lease/(\d+)/(.+)\" \"(.+)\""
        regexp = re.compile(HITRON_REGEXP)
        text = self.get_telnet_dump()
        l = regexp.findall(text)
        d = {}
        for x in l:
            key = x[0] + "/" + x[1]
            if key not in d:
                d[key] = {}
            d[key][x[2]] = x[3]
        d = {d[x]["ip"]: d[x] for x in d}
        return d
