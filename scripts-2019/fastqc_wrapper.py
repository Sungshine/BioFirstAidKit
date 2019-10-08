#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Parallelized wrapper for FastQC.

    https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

"""


import os
import argparse
import subprocess
import multiprocessing


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Parallelized wrapper for FastQC'
    )
    parser.add_argument(
        '-i', '--input-directory',
        dest='indir',
        required=True,
        help='Path to directory of input sequences'
    )
    parser.add_argument(
        '-o', '--output-dir',
        dest='outdir',
        required=True,
        help='Path to desired output directory'
    )
    parser.add_argument(
        '-p', '--processes',
        dest='procs',
        required=True,
        help='Number process to utilize'
    )
    return parser.parse_args()


def get_files(dir):
    return [os.path.join(dir, fn) for fn in next(os.walk(dir))[2]]


def run_fastqc(f):
    subprocess.call(['fastqc', f, '-o', args.outdir])


if __name__ == '__main__':

    args = get_args()
    read_files = get_files(args.indir)

    proc = int(args.procs)
    pool = multiprocessing.Pool(processes=proc)
    r = pool.map_async(run_fastqc, read_files)
    r.wait()

