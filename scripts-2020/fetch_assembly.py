#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Fetch genome assemblies from NCBI Assembly database.
    
    Esearch -> Esummary -> Urllib to grab from RefSeq FTP site
    https://dmnfarrell.github.io/bioinformatics/assemblies-genbank-python

"""

import os
import re
import csv
import time
import argparse
import urllib
from Bio import Entrez
from pprint import pprint
import xml.etree.cElementTree as ET


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Download assembly files from RefSeq'
    )
    parser.add_argument(
        '-i', '--input-file',
        dest='infile',
        required=True,
        help='Path to file containing list of SRR ids, should contain a header'
    )
    parser.add_argument(
        '-o', '--output-directory',
        dest='outdir',
        required=True,
        help='Path to desired output directory'
    )
    return parser.parse_args()


def read_input_file(f):
    """ Input file should contain a header and then SRR ids """
    ids = []
    with open(f, 'r') as fh:
        r = csv.reader(fh, delimiter='\t')
        next(r, None)   # skip header row
        for row in r:
            ids.append(row[2].strip())
    assert len(ids) == len(set(ids)), 'Your list of SRR ids contains duplicates!'
    return ids


if __name__ == '__main__':

    args = get_args()
    Entrez.email = 'wla9@cdc.gov'

    # Load list of assembly ids
    # list_of_ids = ['GCA_002076425.1', 'GCA_002076705.1', 'GCA_000754625.1']
    print('Reading input file...')
    list_of_ids = read_input_file(args.infile)
    
    print('Starting requests...')
    for id in list_of_ids:
        esearch_handle = Entrez.esearch(db='assembly', term=id, max_tries=5, sleep_between_tries=15)
        esearch_record = Entrez.read(esearch_handle)

        pid = esearch_record['IdList'][0]
        time.sleep(.300)
        
        # Get the FTP link using the 
        esummary_handle = Entrez.esummary(db='assembly', id=pid, report='full')
        esummary_record = Entrez.read(esummary_handle)

        url = esummary_record['DocumentSummarySet']['DocumentSummary'][0]['FtpPath_RefSeq']
        if url == '':
            print('EmptyLink = {},{}'.format(id, pid))
            continue
        
        time.sleep(.300)
        label = os.path.basename(url)
        # Get the fasta formatted link
        link = os.path.join(url, '{}_genomic.fna.gz'.format(label))
        
        # outpath = '/Users/sim/Desktop/sra_tooling'
        outpath = args.outdir
        urllib.request.urlretrieve(link, '{}/{}.fasta.gz'.format(outpath, label))
        print('Complete download = {},{}'.format(id, pid))
        time.sleep(.300)
