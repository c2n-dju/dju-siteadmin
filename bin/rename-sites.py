#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import sys


if platform.node() == "ww2":
    DOMAIN = ".c2n.universite-paris-saclay.fr"
elif platform.node() == "vps430313":
    DOMAIN = ".c2n.science"
elif platform.node() == "webc2n2.c2n.u-psud.fr":
    DOMAIN = ".c2n.universite-paris-saclay.fr"
else:
    sys.exit(22)


sys.path.append(os.environ['DJU_DIR'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dju.settings")

import django
django.setup()

from django.contrib.sites.models import Site

sites = {
    1: 'www',
    6: 'minao',
    7: 'cimphonie',
    8: 'crime',
    9: 'experfo',
    10: 'biosys',
    11: 'comics',
    12: 'dynanets',
    13: 'elphyse',
    14: 'ephycas',
    15: 'epla',
    16: 'goss',
    17: 'instrum',
    18: 'mat2d',
    19: 'mimed',
    20: 'minaphot',
    21: 'mnoems',
    22: 'integnano',
    23: 'toniq',
    24: 'nanophotonit',
    25: 'piment',
    26: 'nomade',
    27: 'oxide',
    28: 'phodev',
    29: 'phynano',
    30: 'qcl',
    31: 'qd',
    32: 'poem',
    33: 'panam',
    34: 'seeds',
    35: 'sunlit',
    36: 'odin',
    37: 'test01',
    38: 'test02',
    39: 'test03',
    40: 'qpc',
    41: 'noe',
}

s = Site.objects.get(id=1)
if s.domain != 'edith-cms.c2n.universite-paris-saclay.fr' and s.domain != 'edith-www.c2n.universite-paris-saclay.fr':
    print(s.domain + ' != edith-cms.c2n.universite-paris-saclay.fr or edith-www.c2n.universite-paris-saclay.fr')
    exit
s.domain = 'www' + DOMAIN
s.save()

# code bricolé !
lasti = sorted(sites.keys())[-1]
print('--- NOW renaming until ' + str(lasti))
if DOMAIN == ".c2n.science":
    for site in range(6,lastii+1):
        s = Site.objects.get(id=site)
        if s.domain != 'edith-' + sites[site] + '.c2n.science':
            print(s.domain + ' != edith-' + sites[site] + '.c2n.science')
            exit
        s.domain = sites[site] + DOMAIN
        s.save()
if platform.node() == "webc2n2.c2n.u-psud.fr":
    print('platform.node() == "webc2n2.c2n.u-psud.fr"')
    for site in [1] + list(range(6,lasti+1)):
        s = Site.objects.get(id=site)
        if s.domain != 'edith-' + sites[site] + '.c2n.universite-paris-saclay.fr':
            print(s.domain + ' != edith-' + sites[site] + '.c2n.universite-paris-saclay.fr')
            exit
        s.domain = sites[site] + DOMAIN
        print(s.domain)
        s.save()
    
