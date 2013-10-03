#!/usr/bin/env python2

from glob import glob
import logging
import os
import re
from urllib import urlopen


DNA_FILENAME_RE = re.compile('^(?P<name>.*).dna$')
DNA_RE = re.compile(r'^(?P<ship_id>\d+):(\d+;\d+:)+:$')
SHIP_IMAGE_URL_FMT = 'http://image.eveonline.com/Render/%d_512.png'


def update_fit(dna_filename, eft_filename, rst_filename):

    logging.info('Updating file (%s, %s) -> %s',
                 dna_filename, eft_filename, rst_filename)

    dna = open(dna_filename).read().strip()
    logging.info('DNA: %s', dna)
    dna_m = DNA_RE.match(dna)
    assert dna_m is not None

    logging.info(dna_m.groups())

    eft = open(eft_filename).read().strip()
    ship_raw_name, fit_name = eft.splitlines()[0].strip()[1:-1].split(',')
    ship_norm_name = '-'.join(re.findall('[a-z0-9]+', ship_raw_name.lower()))
    fit_name = fit_name.strip()

    image_path = os.path.join('images', '%s.png' % ship_norm_name)
    if not os.path.exists(image_path):
        with open(image_path, 'w') as f:
            ship_id = dna_m.group('ship_id')
            ship_image_url = SHIP_IMAGE_URL_FMT % int(ship_id)
            f.write(urlopen(ship_image_url).read())

    with open(rst_filename, 'w') as f:

        s = "`%s <javascript:CCPEVE.showFitting('%s');>`_" % (fit_name, dna)
        f.write('%s\n%s\n\n' % (s, '=' * len(s)))
        #f.write('.. image:: /%s\n\n' % image_path)

        eft_iter = iter(eft.splitlines()[2:])

        low_slots = list(iter(eft_iter.next, ''))
        med_slots = list(iter(eft_iter.next, ''))
        high_slots = list(iter(eft_iter.next, ''))
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
    for fit in os.listdir('fits'):
        m = DNA_FILENAME_RE.match(fit)
        if m is not None:
            name = m.group('name')
            update_fit(os.path.join('fits', '%s.dna' % name),
                       os.path.join('fits', '%s.eft' % name),
                       os.path.join('fits', '%s.rst' % name))
