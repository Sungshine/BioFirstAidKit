#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Create a config file for GDETECT tool in STing.

"""


import os
import argparse


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Build configuration file for STing Indexer utility.'
    )
    parser.add_argument(
        '-d',
        '--input-directory',
        dest='indir',
        required=True,
        help='Path to directory containing gene sequences.'
    )
    parser.add_argument(
        '-o',
        '--output-file',
        dest='outfile',
        required=True,
        help='Full path to desired outfile.'
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()

    paths = [os.path.join(args.indir, fn) for fn in next(os.walk(args.indir))[2]]

    with open(args.outfile, 'w') as config_out:
        config_out.write('[loci]\n')
        for genepath in paths:
            genename = os.path.basename(genepath).split('.')
            gene_id = '_'.join(genename[0:2])
            config_out.write('{}\t{}\n'.format(gene_id, genepath))
