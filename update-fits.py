#!/usr/bin/env python2

from glob import glob
import logging
import os
import re

import ujson


SHIP_IMAGE_URL_FMT = 'http://image.eveonline.com/Render/%d_512.png'

TYPES = ujson.load(open('types.json'))


def update_fit(eft_filename, rst_filename):

    logging.info('Updating file %s -> %s', eft_filename, rst_filename)

    eft = open(eft_filename).read().strip()
    ship_name, fit_name = eft.splitlines()[0].strip()[1:-1].split(',')
    ship_name = ship_name.strip()
    fit_name = fit_name.strip()

    modules = {}
    for item in eft.splitlines()[2:]:
        if not item:
            continue
        elif item.lower() in [
            '[empty high slot]',
            '[empty low slot]',
            '[empty med slot]',
        ]:
            continue
        elif item in TYPES:
            modules[TYPES[item]] = modules.get(TYPES[item], 0) + 1
        elif re.match('x\d+', item.split()[-1]) is not None and item.rsplit(' ', 1)[0] in TYPES:
            modules[TYPES[item.rsplit(' ', 1)[0]]] = modules.get(TYPES[item.rsplit(' ', 1)[0]], 0) + int(item.split()[-1][1:])

    dna = '%d:%s' % (
        TYPES[ship_name],
        ';'.join('%d:%d' % (type_id, quantity)
                 for type_id, quantity in modules.items())
    )

    with open(rst_filename, 'w') as f:

        s = "`%s <javascript:CCPEVE.showFitting('%s');>`_" % (fit_name, dna)
        f.write('%s\n%s\n\n' % (s, '=' * len(s)))

        eft_iter = iter(eft.splitlines()[2:])

        low_slots = list(iter(eft_iter.next, ''))
        med_slots = list(iter(eft_iter.next, ''))
        high_slots = list(iter(eft_iter.next, ''))
        rigs = list(iter(eft_iter.next, ''))
        ammo = list(iter(eft_iter.next, ''))
        drones = list(iter(eft_iter.next, ''))

        f.write('High slots\n----------\n\n')
        for line in high_slots:
            f.write('- %s\n' % line.strip())
        f.write('\n')

        f.write('Med slots\n---------\n\n')
        for line in med_slots:
            f.write('- %s\n' % line.strip())
        f.write('\n')

        f.write('Low slots\n---------\n\n')
        for line in low_slots:
            f.write('- %s\n' % line.strip())
        f.write('\n')

        if rigs:
            f.write('Rigs\n----\n\n')
            for line in rigs:
                f.write('- %s\n' % line.strip())
            f.write('\n')

        if ammo:
            f.write('Ammo\n----\n\n')
            for line in ammo:
                f.write('- %s\n' % line.strip())
            f.write('\n')

        if drones:
            f.write('Drones\n------\n\n')
            for line in drones:
                f.write('- %s\n' % line.strip())
            f.write('\n')


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    for i in glob('fits/*.rst'):
        logging.info('Removing %s', i)
        os.unlink(i)
    for fname in os.listdir('fits'):
        m = re.match(r'^(?P<name>.*)\.eft$', fname)
        if m is not None:
            name = m.group('name')
            update_fit(os.path.join('fits', '%s.eft' % name),
                       os.path.join('fits', '%s.rst' % name))
