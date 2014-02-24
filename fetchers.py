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


class HitronConnectionsFetcher(object):

    SIMPLE_IP_REGEX = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    HITRON_REGEXP = r"(\d+):\s+([A-Z]+)\s+(" + SIMPLE_IP_REGEX + "):(\d+)\s+<-->(" \
        + SIMPLE_IP_REGEX + "):(\d+)\s+\[(" + SIMPLE_IP_REGEX + "):(\d+)\].*"
    USERNAME_TELNET_STRING = "Username:"
    PASSWORD_TELNET_STRING = "Password:"

    def __init__(self,user,password):
        self.user = user
        self.password = password
        self.host = self.get_host_name()

    def get_host_name(self):
        import socket
        import struct
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                    continue
                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

    def get_telnet_dump(self):
        from telnetlib import Telnet
        from time import sleep
        host = get_host_name ()
        tn = Telnet(self.host)
        tn.read_until(USERNAME_TELNET_STRING)
        tn.write(self.user + "\n")
        tn.read_until(PASSWORD_TELNET_STRING)
        tn.write(self.password + "\n\n")
        tn.write("firewall\n\n")
        tn.write("dump\n")
        tn.read_until("Active Connections")
        text = "Active Connections" +  tn.read_until("Returned")
        tn.write("exit\n\nexit\n")
        return text

    def get_connections(self):
        import re
        regexp = re.compile(rexp)
        connections_list = regexp.findall(self.get_telnet_dump())
        return [ConnectionInfo(...) for x in connections_list]