#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import psycopg2

if len(sys.argv) != 3 or sys.argv[1] != "--oui-efface":
    print("Vous ne semblez pas bien certain de vouloir tout effacer!")
    exit(22)


try:
    base = os.environ[sys.argv[2]]
except KeyError:
    print("Pas de " + sys.argv[2] + " comme variable d'environnement")
    exit(22)


def efface(base):
    try:
        conn = psycopg2.connect("dbname='" + base + "'")
        conn.set_isolation_level(0)
    except:
        print("Unable to connect to the database.")
        exit(22)
        
    cur = conn.cursor()

    try:
        cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
        rows = cur.fetchall()
        for row in rows:
            print("dropping table: ", row[1])
            cur.execute("drop table " + row[1] + " cascade")
        cur.close()
        conn.close()
    except:
        print("Error: ", sys.exc_info()[1])
        
efface(base)
