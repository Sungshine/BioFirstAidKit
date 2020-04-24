#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


""" Download script for allele sequences from PubMLST/BIGSdb.

    pubmlst_vparahaemolyticus_seqdef
    pubmlst_vcholerae_seqdef
    pubmlst_vvulnificus_seqdef -- No cgMLST exists at this time

"""


import os
import csv
import json
import requests
import argparse
from pprint import pprint


def get_args():
    """ Get command line arguments """
    parser = argparse.ArgumentParser(
        description='Download allele sequences from BIGSdb'
    )
    parser.add_argument(
        '-d', '--database-name',
        dest='db',
        required=True,
        help='Name of BIGSdb database i.e. [pubmlst_vparahaemolyticus_seqdef]'
    )
    parser.add_argument(
        '-o', '--output-directory',
        dest='outdir',
        required=True,
        help='Path to desired output directory'
    )
    return parser.parse_args()


def write_to_disk(api_command, out_path, file_name):
    """ Write streaming file content to new file on disk """
    blockSize = 20971520
    try:
        with open(out_path, 'wb') as fastq:
            os.chmod(out_path, 0o755)
            for block in api_command.iter_content(blockSize):
                fastq.write(block)
    except (Exception, KeyboardInterrupt) as e:
        print('{} was unable to be written to disk: {}'.format(out_path, e))
        pass


if __name__ == '__main__':

    args = get_args()

    root = 'http://rest.pubmlst.org'
    endpoint = '{}/db/{}/loci?{}'.format(root, args.db, 'page_size=3000')
    r = requests.get(endpoint)

    for item in r.json()['loci']:
        endpoint = '{}/alleles_fasta'.format(item)
        loci_name = item.split('/')[-1]

        print('Downloading {}'.format(loci_name))
        r = requests.get(endpoint, stream=True)
        outpath = '{}/{}.fasta'.format(args.outdir, loci_name)
        write_to_disk(r, outpath, loci_name)
