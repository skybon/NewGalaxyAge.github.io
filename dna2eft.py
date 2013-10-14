#!/usr/bin/env python2
# coding: utf-8
#
# Скрипт генерит EFT из DNA с указанного .rst-файла.
#

import sys
import os
import re

import logging

from reverence import blue


FIT_LINK_RE = re.compile(r"`(?P<name>[^<`]+) <javascript:CCPEVE.showFitting\('(?P<dna>\d+:(\d+;\d+:)+:)'\);>`_")


def dna2eft(name, dna):

    logging.info("Converting %s %s", name, dna)

    ship = CFG.invtypes.Get(int(dna.split(':')[0])).name

    logging.info("    ship: %s", ship)

    modules = [i.split(';') for i in dna.split(':')[1:] if i]

    modules = [(CFG.invtypes.Get(int(t)), int(q)) for t, q in modules]

    high = []
    med = []
    low = []
    rigs = []
    charges = []
    drones = []

    for t, q in modules:
        category = t.Group().Category().name
        if category == 'Module':
            effects = [CFG.dgmeffects.Get(i.effectID).effectName
                       for i in CFG.dgmtypeeffects[t.typeID]]
            if 'rigSlot' in effects:
                rigs.extend([t.name] * q)
            elif 'hiPower' in effects:
                high.extend([t.name] * q)
            elif 'medPower' in effects:
                med.extend([t.name] * q)
            elif 'loPower' in effects:
                low.extend([t.name] * q)
        elif category == 'Drone':
            drones.append('%s x%d' % (t.name, q))
        elif category == 'Charge':
            charges.append('%s x%d' % (t.name, q))

    names = {
        u'бюджет': 'basic',
        u'средний': 'standard',
        u'ветеран': 'advanced',
        u'снайпер': 'snipe',
        u'активный': 'active',
        u'пассивный': 'passive',
        u'бластерный': 'blaster',
    }

    if ship.lower() != name.lower():
        if name.lower() in names:
            t = names[name.lower()]
            name = u'%s - %s' % (ship, name)
        else:
            logging.warning(u'Bad name: %s', name)
            t = name.lower()
        fname = u'%s-%s.eft' % (ship.lower(), t.lower())
    else:
        fname = u'%s.eft' % ship.lower()

    fname = '-'.join(fname.split())

    with open(os.path.join(sys.argv[2], fname), 'w') as f:
        f.write((u'[%s, %s]\n\n' % (ship, name)).encode('utf-8'))
        f.write('\n\n'.join('\n'.join(group) for group in [
            low, med, high, rigs, charges, drones
        ]))
        f.write('\n')

if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    EVE = blue.EVE(os.path.expanduser('~/.wine/drive_c/Program Files (x86)/CCP/EVE'))
    CFG = EVE.getconfigmgr()
    fits = list((i.group('name'), i.group('dna'))
                for i in FIT_LINK_RE.finditer(
                    open(sys.argv[1]).read().decode('utf-8')
                ))
    for name, dna in fits:
        dna2eft(name, dna)
