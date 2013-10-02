#!/usr/bin/env python2

import os
import re

import logging


FITS_DIR = '/home/ei-grad/raisa/fits'
FIT_FILENAME_RE = re.compile('^(?P<name>.*).eft$')
DNA_RE = re.compile(r'^(\d+:\d+;)+\d+::$')


def update_fit(fit_filename, rst_filename):

    logging.info('Updating file %s -> %s', fit_filename, rst_filename)
    f = open(fit_filename)

    dna = f.readline().strip()

    logging.info('DNA: %s', dna)

    assert DNA_RE.match(dna) is not None

    eft = f.read()

    ship, fit_name = eft.splitlines()[0][1:-1].split(',')

    with open(rst_filename, 'w') as f:
        f.write("%s\n%s\n\n" % (ship, '=' * len(ship)))
        f.write("`%s <javascript:CCPEVE.showFitting('%s');>`\n\n" % (
            ship, dna
        ))
        f.write('.. code-block:: text\n\n')
        for line in eft.splitlines():
            f.write('    ' + line.strip() + '\n')


if __name__ == "__main__":
    logging.basicConfig(format="%(msg)s", level=logging.DEBUG)
    for fit in os.listdir(FITS_DIR):
        m = FIT_FILENAME_RE.match(fit)
        if m is not None:
            update_fit(os.path.join(FITS_DIR, fit),
                       os.path.join(FITS_DIR, '%s.rst' % m.group('name')))
