#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Extract CDS from BioNumerics 7.6 exported annotation file.

"""


import os
import csv
import argparse


def get_args():
    """ Get command line arguments.

    """
    parser = argparse.ArgumentParser(
        description='Extract CDS from BioNumerics exported annotation file.'
    )
    parser.add_argument(
        '-i', '--input-file',
        dest='infile',
        required=True,
        help='Path to exported annotation file.'
    )
    parser.add_argument(
        '-o', '--output-dir',
        dest='outdir',
        required=True,
        help='Path to desired output directory.'
    )
    parser.add_argument(
        '-l', '--loci-file',
        dest='loci',
        required=True,
        help='Path to file containing loci.'
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()

    # Extract & concatenate entire sequence
    sq = []
    with open(args.infile, 'r') as infile:
        for line in infile:
            if line.startswith(' '):
                s = ''.join(line.strip().split(' ')[:-1]).strip()
                sq.append(s)
    newseq = ''.join(sq)

    # Extract cds
    d = {}
    lt = False
    start = False
    stop = False
    with open(args.infile, 'r') as infile:
        for line in infile:
            if line.startswith('FT'):
                if 'CDS' in line:
                    locate = line.strip().split(' ')[-1].strip()
                    if 'complement' in locate:
                        start = locate.split('(')[1].strip(')').split('..')[0]
                        stop = locate.split('(')[1].strip(')').split('..')[1]
                    else:
                        start = locate.split('..')[0]
                        stop = locate.split('..')[1]
            if '/locus_tag' in line:
                lt = line.strip().split(' ')[-1].split('=')[-1].strip('"')

            if lt in d.iterkeys():
                continue
            else:
                d[lt] = [start, stop]

    # Open loci file
    queries = []
    with open(args.loci, 'r') as inloci:
        reader = csv.reader(inloci, delimiter=',')
        for row in reader:
            # print(row)
            queries.append(row[0])


    # Print sequence to file
    for i in queries:
        start = int(d[i][0])
        stop = int(d[i][1])

        outpath = '{}/{}.fa'.format(args.outdir, i)
        with open(outpath, 'w') as oh:
            oh.write('>{}\n'.format(i))
            oh.write('{}\n'.format(newseq[start:stop]))
