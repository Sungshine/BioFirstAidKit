#!/usr/bin/env python2.7

""" Execute STing Detector utility.

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
            newfile = file.replace('_R1', '_R*')
        elif '_R2' in file:
            newfile = file.replace('_R2', '_R*')
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
    read_paths = [os.path.join(args.indir, fn) for fn in next(os.walk(args.indir))[2]]
    reads_hash = wranglePairedEnds(read_paths)

    wall_timer = '/usr/bin/time'
    database = args.db

    for key in reads_hash:
        r1 = reads_hash.get(key)[0]
        r2 = reads_hash.get(key)[1]

        outname = os.path.basename(key).split('_')[0]
        outpath = '{}/{}.tsv'.format(args.outdir, outname)
        out_handle = open(outpath, 'w')

        ps = subprocess.Popen((wall_timer, '-v', 'detector', '-x', database, '-1', r1, '-2', r2, '-k', '30', '-c', '-p',
                               '>', outpath, '2>&1'),
                              # stderr=subprocess.PIPE,
                              # stdout=subprocess.PIPE,
                              )

        # out, err = ps.communicate()
        #
        # out_handle.write(err)
        # out_handle.write(out)
        # out_handle.close()
