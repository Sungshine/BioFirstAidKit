#!/usr/bin/env python2.7

""" Run SPAdes on directory of assemblies.

"""


import os
import csv
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
            newfile = file.replace('_R1', '_R*')
        elif '_R2' in file:
            newfile = file.replace('_R2', '_R*')
        if newfile not in pair_hash:
            pair_hash[newfile] = [file]
        else:
            pair_hash[newfile].append(file)
    return pair_hash


if __name__ == '__main__':


    # Command line arguments.
    opt_parse = argparse.ArgumentParser(description='Launch SPAdes on read pair files.')
    opt_parse.add_argument('-i', '--input-directory', dest='indir', required=True, help='Path to directory containing paired read files.')
    opt_parse.add_argument('-o', '--outdir', dest='outdir', required=True, help='Path to results directory.')
    args = opt_parse.parse_args()

    # Designate pointers to absolute paths.
    read_paths = [os.path.join(args.indir, fn) for fn in next(os.walk(args.indir))[2]]
    reads_hash = wranglePairedEnds(read_paths)

    print(reads_hash)