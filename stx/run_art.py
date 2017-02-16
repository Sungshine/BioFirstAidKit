#!/usr/bin/env python2.7

""" Execute ART read simulator.

"""


import os
import errno
import argparse
import subprocess


__author__ = 'Sung Im'
__email__ = 'sungbin401@gmail.com'


if __name__ == '__main__':


    # Command line arguments.
    opt_parse = argparse.ArgumentParser(description='Run ART on a directory of concatenated genome files.')
    opt_parse.add_argument('-i', '--input-directory', dest='indir', required=True, help='Path to directory containing fasta files.')
    opt_parse.add_argument('-o', '--outdir', dest='outdir', required=True, help='Path to output directory.')
    args = opt_parse.parse_args()

    # Designate pointers to absolute paths.
    file_paths = [os.path.join(args.indir, fn) for fn in next(os.walk(args.indir))[2]]

    for file in file_paths:
        print(file)