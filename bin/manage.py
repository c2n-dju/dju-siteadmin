#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# exec(open("manage.py").read())

import platform
import sys
ALL_TEAMS = [
    'www',
    'anamat',
    'biosys',
    'cimphonie',
    'comics',
    'crime',
    'dynanets',
    'elabmat',
    'elphyse',
    'ephycas',
    'epla',
    'experfo',
    'goss',
    'heterna',
    'instrum',
    'mat2d',
    'micromed',
    'minao',
    'minaphot',
    'mnoems',
    'integnano',
    'nanophotoniq',
    'nanophotonit',
    'nanotech',
    'nomade',
    'oxide',
    'phodev',
    'phynano',
    'qcl',
    'qd',
]
if platform.node() == 'vps430313':
    TEST_URL = "http://www-test.c2n.science/fr/"
    TEAMS = [
        'www',
        'anamat',
        'biosys',
        'cimphonie',
        'comics',
        'crime',
        'dynanets',
        'elabmat',
        'elphyse',
        'ephycas',
        'epla',
        'experfo',
        'goss',
        'heterna',
        'instrum',
        'mat2d',
        'micromed',
        'minao',
        'minaphot',
        'mnoems',
        'integnano',
        'nanophotoniq',
        'nanophotonit',
        'nanotech',
        'nomade',
        'oxide',
        'phodev',
        'phynano',
        'qcl',
        'qd',
    ]
elif platform.node() == 'ww2':
    TEST_URL = "http://www-test.c2n.universite-paris-saclay.fr/fr/"
    TEAMS = ['www',]
else:
    print("Nom inconnu : " + platform.node())
    sys.exit(22)


from lib.lib import *

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "migrate" and sys.argv[2] == "data":
        migrate_data(TEAMS, TEST_URL)
    elif len(sys.argv) == 3 and sys.argv[1] == "start" and sys.argv[2] == "test":
        start_test(TEAMS)
    elif len(sys.argv) == 3 and sys.argv[1] == "stop" and sys.argv[2] == "test":
        stop_test(TEAMS)
    elif len(sys.argv) == 3 and sys.argv[1] == "swap" and sys.argv[2] == "site":
        swap_site(TEAMS, TEST_URL)
    else:
        print(sys.argv[0] + " migrate data, start test, stop test, or swap site", file=sys.stderr)
        exit(22)
