#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Merge multiple read pairs from Illumina NextSeq Instrument.
    Concatenate multiple R1/R2 files into a single R1/R2 file.
    Disambiguate lane annotation in file name to '_L999_'.

"""


import os
import shutil
import argparse


def get_args():
    """ Get command line arguments.

    """
    parser = argparse.ArgumentParser(
        description='Merge multiple fastq files.'
    )
    parser.add_argument(
        '-i',
        '--input-directory',
        dest='indir',
        required=True,
        help='Path to directory containing fastq files.'
    )
    parser.add_argument(
        '-o',
        '--output-directory',
        dest='outdir',
        required=True,
        help='Path to desired output directory.'
    )
    return parser.parse_args()


def construct_list(indir, coord):
    """ Return a list of forward or reverse reads.
        Must specify:
        (1) input directory containing read files and
        (2) orientation of reads: 'R1' or 'R2'.

    """
    fpaths = [os.path.join(indir, f) for f in next(os.walk(indir))[2]]
    return filter(lambda readfile: '_{}_'.format(coord) in readfile, fpaths)


def main():
    """ Write merged forward and reverse reads into single mate pair.

    """
    args = get_args()

    r1_files = construct_list(args.indir, 'R1')
    r2_files = construct_list(args.indir, 'R2')

    fname = os.path.basename(sorted(r1_files)[0]).replace('_L001_', '_L999_')
    with open(os.path.join(args.outdir, fname), 'wb') as outfile:
        for read1 in sorted(r1_files):
            shutil.copyfileobj(open(read1), outfile)

    fname = os.path.basename(sorted(r2_files)[0]).replace('_L001_', '_L999_')
    with open(os.path.join(args.outdir, fname), 'wb') as outfile:
        for read2 in sorted(r2_files):
            shutil.copyfileobj(open(read2), outfile)


if __name__ == '__main__':

    main()
