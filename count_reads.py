#!/usr/bin/env python2.7

""" Calculate number of reads in fastq file.

"""


import os
import errno
import argparse
import subprocess


__author__ = 'Sung Im'
__email__ = 'sungbin401@gmail.com'


if __name__ == '__main__':


    # Command line arguments.
    opt_parse = argparse.ArgumentParser(description='Calculate read counts on a directory of reads.')
    opt_parse.add_argument('-i', '--input-directory', dest='indir', required=True,
                           help='Path to directory containing paired read files.')
    opt_parse.add_argument('-o', '--outdir', dest='outdir', required=True, help='Path to results directory.')
    args = opt_parse.parse_args()

    # Designate pointers to absolute paths.
    read_paths = [os.path.join(args.indir, fn) for fn in next(os.walk(args.indir))[2]]

    outfile = '{}/readcounts.csv'.format(args.outdir)
    out_handle = open(outfile, 'wa')

    for file in read_paths:

        filename = os.path.basename(file)
        filesize = os.stat(file).st_size

        cat = subprocess.Popen(('cat', file), stdout=subprocess.PIPE)
        grep = subprocess.Popen(('grep', '\@'), stdin=cat.stdout, stdout=subprocess.PIPE)
        count = subprocess.Popen(('wc', '-l'), stdin=grep.stdout, stdout=subprocess.PIPE)

        out = count.communicate()[0]

        out_handle.write('{},{},{}'.format(filename, out, filesize))

    out_handle.close()
