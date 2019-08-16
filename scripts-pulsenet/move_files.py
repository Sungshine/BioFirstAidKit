#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Move files from one location to another.

"""


import csv
import shutil
import argparse


def get_args():
    """ Get command line arguments.

    """
    parser = argparse.ArgumentParser(
        description='Copy files to desired location.'
    )
    parser.add_argument(
        '-i', '--input-file',
        dest='infile',
        required=True,
        help='File with list of file names.'
    )
    parser.add_argument(
        '-d', '--source-directory',
        dest='source',
        required=True,
        help='Path to source directory of files.'
    )
    parser.add_argument(
        '-o', '--output-dir',
        dest='outdir',
        required=True,
        help='Path to target directory.'
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()

    # Read file
    with open(args.infile, 'rU') as ih:
        r = csv.reader(ih, delimiter=',')
        for line in r:
            id = line[0].strip()
            infmt = '{}/{}'.format(args.source, id)
            outfmt = '{}/{}'.format(args.outdir, id)
            print('Moving file: {}'.format(id))
            shutil.copy(infmt, outfmt)
