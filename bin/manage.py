#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# exec(open("manage.py").read())

import platform
import sys
from lib.lib import *

VN = 1

ALL_TEAMS = [
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
    'integnano',
    'mat2d',
    'mimed',
    'minao',
    'minaphot',
    'mnoems',
    'nanophotonit',
    'noe',
    'nomade',
    'odin',
    'oxide',
    'panam',
    'phodev',
    'phynano',
    'piment',
    'poem',
    'qcl',
    'qd',
    'qpc',
    'sunlit',
    'test01',
    'test02',
    'test03',
    'toniq',
    'www',
]


if platform.node() == 'ww2':
    TEST_URL = "http://www-test.c2n.u-psud.fr/fr/"
    TEAMS = ['www',]
elif platform.node() == 'webc2n2.c2n.u-psud.fr':
    TEST_URL = "http://www.v2.c2n.science/en/"
    TEAMS = ['www',
            'biosys',
            'cimphonie',
            'crime',
            'elphyse',
            'epla',
            'goss',
            'heterna',
            'mat2d',
            'mimed',
            'minaphot',
            'mnoems',
            'noe',
            'odin',
            'oxide',
            'panam',
            'phynano',
            'piment',
            'poem',
            'qpc',
            'toniq',
            ]
    VN=2
else:
    print("Nom inconnu : " + platform.node())
    sys.exit(22)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "migrate" and sys.argv[2] == "data":
        migrate_data(VN, TEAMS, TEST_URL)
    elif len(sys.argv) == 3 and sys.argv[1] == "start" and sys.argv[2] == "test":
        start_test(VN, TEAMS)
    elif len(sys.argv) == 3 and sys.argv[1] == "stop" and sys.argv[2] == "test":
        stop_test(TEAMS)
    elif len(sys.argv) == 3 and sys.argv[1] == "swap" and sys.argv[2] == "site":
        swap_site(VN, TEAMS, TEST_URL)
    else:
        print(sys.argv[0] + " migrate data, start test, stop test, or swap site", file=sys.stderr)
        exit(22)
