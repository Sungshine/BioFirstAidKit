#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


""" Launch STing Detector utility on a directory containing reads.

"""


import os
import errno
import argparse
import subprocess


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Launch STing detector utility on directory of reads.'
    )
    parser.add_argument(
        '-i',
        '--input-directory',
        dest='indir',
        required=True,
        help='Path to directory containing paired read files.'
    )
    parser.add_argument(
        '-d',
        '--database',
        dest='db',
        required=True,
        help='Path to database + prefix.'
    )
    parser.add_argument(
        '-o',
        '--output-directory',
        dest='outdir',
        required=True,
        help='Path to results directory.'
    )
    return parser.parse_args()


def wrangle_paired_ends(fps):
    """ Match paired-end read files. """
    pair_hash = {}
    for fp in fps:
        newfile = ""
        if '_R1' in fp:
            newfile = fp.replace('_R1', '_R*')
        elif '_R2' in fp:
            newfile = fp.replace('_R2', '_R*')
        if newfile not in pair_hash:
            pair_hash[newfile] = [fp]
        else:
            pair_hash[newfile].append(fp)
    return pair_hash


def check_for_directory(path):
    """ Create output directory if it does not exist. """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


if __name__ == '__main__':

    args = get_args()

    # Designate pointers to absolute paths
    read_paths = [os.path.join(args.indir, fn) for fn in next(os.walk(args.indir))[2]]
    reads_hash = wrangle_paired_ends(read_paths)

    check_for_directory(args.outdir)
    wall_timer = '/usr/bin/time'
    database = args.db

    for key in reads_hash:
        r1 = reads_hash.get(key)[0]
        r2 = reads_hash.get(key)[1]
        outname = os.path.basename(key).split('-')[0]
        outlane = os.path.basename(key).split('-')[1]
        outjoin = '{}-{}'.format(outname, outlane)
        outpath = '{}/{}.tsv'.format(args.outdir, outjoin)
        out_handle = open(outpath, 'w')
        ps = subprocess.Popen((wall_timer, '-v', 'detector', '-x', database, '-1', r1, '-2', r2, '-k', '30', '-c', '-p',),
                              stderr=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              )
        err, out = ps.communicate()
        out_handle.write(out)
        out_handle.write(err)
        out_handle.close()