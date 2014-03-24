#!/usr/bin/python
# -*- coding: utf-8 -*-


import sqlite3
import json

DB_NAME = "/home/ch01/.conn_hist.db"


def get_historic():
    while True:
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cons = conn.execute("SELECT time, conns from Historico" + \
                                    " ORDER BY time").fetchall()
                return [{"time": x[0], "conns": x[1]} for x in cons]
        except:
            import time
            time.sleep(1)


if __name__ == '__main__':
    print 'Content-Type: application/json'
    print 'Access-Control-Allow-Origin: *'
    print 'Access-Control-Allow-Methods: GET'
    print ''

    conns = get_historic()
    print json.dumps(conns)
