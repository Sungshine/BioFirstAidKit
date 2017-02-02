#!/usr/bin/env python2.7

""" Execute STing detection with varying k-mer lengths.

Script should be executed from inside 'reads' directory.

"""


import os
import errno
import argparse
import subprocess


__author__ = 'Sung Im'
__email__ = 'sungbin401@gmail.com'


def wranglePairedEnds(path):
    """ Match paired-end read files.

    """
    pair_hash = {}
    for file in path:
        newfile = ""
        if '_R1' in file:
            newfile = file.replace('R1', 'R*')
        elif '_R2' in file:
            newfile = file.replace('R2', 'R*')
        if newfile not in pair_hash:
            pair_hash[newfile] = [file]
        else:
            pair_hash[newfile].append(file)
    return pair_hash


def check_for_directory(path):
    """ Create output directory if it does not exist.

    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


if __name__ == '__main__':


    # Command line arguments.
    opt_parse = argparse.ArgumentParser(description='Launch STing Utilities on a directory of reads.')
    opt_parse.add_argument('-i', '--input-directory', dest='indir', required=True, help='Path to directory containing paired read files.')
    opt_parse.add_argument('-d', '--database', dest='db', required=True, help='Path to database + prefix.')
    opt_parse.add_argument('-o', '--outdir', dest='outdir', required=True, help='Path to results directory.')
    args = opt_parse.parse_args()

    # Designate pointers to absolute paths.
    readpaths = [os.path.join(args.indir, fn) for fn in next(os.walk(args.indir))[2]]
    reads_hash = wranglePairedEnds(readpaths)

    # Path to database
    database = args.db

