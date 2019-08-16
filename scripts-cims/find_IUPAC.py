#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


""" Report gene sequence files that contain IUPAC alphabet characters.
    Reports file name, offending line location, offending character location.

"""


import os
import argparse


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Replace IUPAC alphabet with N.'
    )
    parser.add_argument(
        '-i',
        '--input-directory',
        dest='indir',
        required=True,
        help='Path to input file.'
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()

    nuc = ['A', 'T', 'C', 'G']
    fps = [os.path.join(args.indir, f) for f in next(os.walk(args.indir))[2]]
    for fp in fps:
        with open(fp, 'r') as infile:
            reader = infile.readlines()
            for line in reader:
                if line.startswith('>'):
                    continue
                else:
                    for char in line.strip():
                        if char not in nuc:
                            print(os.path.basename(fp))
                            print(char, reader.index(line), line.index(char))
