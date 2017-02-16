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
    out_dir = args.outdir

    for file in file_paths:

        outname = '{}R'.format(os.path.basename(file).split('.')[0])
        outpath = '{}/{}'.format(out_dir, outname)

        print('###### Now simulating reads for {}.'.format(outname))
        subprocess.call(['art_illumina', '-p',
                         '-ss', 'MSv3',
                         '-i', file,
                         '-l', '150',
                         '-f', '30',
                         '-o', outpath,
                         '-m', '200',
                         '-s', '10',
                         '-na',
                         ]
                        )
