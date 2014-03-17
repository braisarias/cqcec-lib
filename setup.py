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


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

dependency_links = ["https://github.com/juliensobrier/google-safe" +
                    "-browsing-lookup-python.git"]
install_requires = ["requests", "BeautifulSoup", "whois"]

setup(
    name="CQCEC",
    version="0.01alpha",
    scripts=["cqcec"],
    packages=["cqcec_lib"],
    install_requires=["requests", "BeautifulSoup", "whois"],
    dependency_links=[
        "https://github.com/juliensobrier/google-safe"],
    data_files=[('/etc', ["cqcec_config.cfg"])]
)
