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


class ConnectionInfo(object):
    """Class that encapsulates info about a connection."""

    def check_ip (self, ip):
        import re
        COMPLEX_IP_REGEX = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(" \
            + "[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
        regex = re.compile(COMPLEX_IP_REGEX)
        return regex.match(ip) != None

    def check_proto (self, proto):
        if proto.lower() in ("tcp", "udp", "igmp"):
            return False
        return True

    def check_port (self, port):
        try:
            num = int(port)
            return num > 0 and num < 65535
        except ValueError:
            return False

    def __init__(self, ip_orig, port_orig, ip_dest, port_dest, proto):
        super(ConnectionInfo, self).__init__()
        if not self.check_ip(ip_orig):
            raise ValueError("IP origen")
        if not self.check_ip(ip_dest):
            raise ValueError("IP dest")
        if port_orig != "" and not self.check_port(port_orig):
            raise ValueError("port origen")
        if port_dest != "" and not self.check_port(port_dest):
            raise ValueError("Port dest")
        self.ip_orig = ip_dest
        self.port_orig = port_dest
        self.proto = proto
        self.ip_dest = ip_dest
        self.port_dest = port_dest

    def json_dump (self):
        import json
        return json.dumps({"ip_orig":self.ip_orig, "port_orig":self.port_orig, \
            "ip_dest":self.ip_dest, "port_dest":self.port_dest, "proto":self.proto})
