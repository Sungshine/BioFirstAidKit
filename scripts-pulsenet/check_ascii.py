#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


""" Check data in BN entry info fields for non-ascii characters.

"""


import os
import csv
import argparse


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Check BN info entry fields for non-ascii chars.'
    )
    parser.add_argument(
        '-i', '--input-file',
        dest='infile',
        required=True,
        help='Path to input file'
    )
    parser.add_argument(
        '-o', '--output-file',
        dest='outfile',
        required=True,
        help='Path to output file'
    )
    return parser.parse_args()


if __name__ == '__main__':
    
    args = get_args()

    big_dict = {}

    with open(args.infile, 'rU') as fh:
        r = csv.reader(fh, delimiter='\t')

        headers = next(r, None)

        for row in r:
            key = row[0].strip()
            if key not in big_dict.keys():
                big_dict[key] = row
            else:
                print('Duplicate Key Error: {}'.format(key))

    outlines = [['EntryKey', 'FieldId']]

    # check values
    for k, v in big_dict.iteritems():
        for i, col in enumerate(v):
            if any(ord(char) > 127 for char in col):
                outlines.append([k, headers[i]])

    # write results to file
    with open(args.outfile, 'w') as oh:
        w = csv.writer(oh, delimiter='\t')
        for line in outlines:
            w.writerow(line)
