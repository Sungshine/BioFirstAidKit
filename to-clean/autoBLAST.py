#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


""" BLAST fasta files against the O and H serotype finder database.

    Acknowledgement:    DTU - Center for Genomic Epidemiology
                        http://www.genomicepidemiology.org/
"""


import os
import argparse
import subprocess


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Run BLASTn search.'
    )
    parser.add_argument(
        '-i',
        '--input-directory',
        dest='indir',
        required=True,
        help='Path to directory containing query sequences.'
    )
    parser.add_argument(
        '-o',
        '--out-directory',
        dest='outdir',
        required=True,
        help='Path to output directory.'
    )
    parser.add_argument(
        '-db',
        '--database',
        required=True,
        help='Path to BLAST databases.'
    )
    return parser.parse_args()


def o_blaster(query, outpath):
    """ Blast query against CGE O-antigen database """
    subprocess.call(['blastn', '-query', query, '-db', o_db,
                     '-outfmt', '10', '-out', outpath])


def h_blaster(query, outpath):
    """ Blast query against CGE H-antigen database. """
    subprocess.call(['blastn', '-query', query, '-db', h_db,
                     '-outfmt', '10', '-out', outpath])


if __name__ == '__main__':

    # Get command line arguments
    args = get_args()

    o_db = '{}/O_type'.format(args.database)
    h_db = '{}/H_type'.format(args.database)

    dir = [os.path.join(args.indir, f) for f in next(os.walk(args.indir))[2]]

    for f in dir:
        base = os.path.basename(f)
        filename = os.path.splitext(base)[0]
        out_O = args.outdir + filename + '.resultO'
        out_H = args.outdir + filename + '.resultH'

        if '_O' in filename and '_H' in filename:
            o_blaster(f, out_O)
            h_blaster(f, out_H)
        elif '_H' not in filename:
            o_blaster(f, out_O)
        elif '_O' not in filename:
            h_blaster(f, out_H)
