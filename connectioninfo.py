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

    COMPLEX_IP_REGEX = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(" \
    + "[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"

    def check_ip (ip):
        import re
        regex = re.compile(COMPLEX_IP_REGEX)
        return regex.match(ip) != None
        return False

    def check_proto (proto):
        if proto.lower() in ("tcp", "udp"):
            return False
        return True

    def check_port (port):
        try:
            num = int(port)
            return num > 0 && num < 65535
        except ValueError:
            return False

    def __init__(self, ip, proto, port):
        super(ConnectionInfo, self).__init__()

        if ! (check_port(port) && check_proto(proto) && check_ip(ip)):
            raise ValueError

        self.ip = ip
        self.proto = proto
        self.port = port

    def json_dump (self):
        import json
        return jsom.dump ({"ip":self.ip,"proto":self.proto,"port":self.port})
