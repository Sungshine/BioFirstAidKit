#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


""" Search NCBI using SAMN ids and return PNUSA ids.

"""


import csv
import requests
import argparse
from xml.etree import ElementTree


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Search NCBI for SRA and BioProject accessions.'
    )
    parser.add_argument(
        '-i', '--input-file',
        dest='infile',
        required=True,
        help='Path to input file.'
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()

    esearch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    elink_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
    esummary_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
    efetch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

    # input
    d = dict()
    f = '/Users/sim/Downloads/pdg_50k.txt'
    with open(f, 'rU') as fh:
        r = csv.reader(fh, delimiter='\t')
        for row in r:
            samn = row[1]
            wgsid = row[3]
            if wgsid == 'NULL':
                d[samn] = [wgsid]   #TODO There are duplicate keys

    # dispatch requests
    for k in d.iterkeys():
        esearch = requests.get(
            esearch_base + '?retmode=xml&db=biosample&term={}&usehistory=y'
            .format(k)
        )

        stree = ElementTree.fromstring(esearch.content)
        for snode in stree.iter('eSearchResult'):
            try:
                query_key = snode.find('QueryKey').text
                web_env = snode.find('WebEnv').text
                accession = [x[0].text for x in snode.findall('IdList')]
            except (IndexError, AttributeError):
                continue

            esummary = requests.get(
                esummary_base + '?retmode=xml&db=biosample&WebEnv={}&query_key={}'
                .format(web_env, query_key)
            )

            sumtree = ElementTree.fromstring(esummary.content)
            for sumnode in sumtree.iter('Accession'):
                try:
                    samn = sumnode.text



