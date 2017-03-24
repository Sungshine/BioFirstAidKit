#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Efetch wrapper: return formatted data records for a list of input UIDs.

"""


import os
import csv
import argparse
import requests
from xml.etree import ElementTree


def get_args():
    """ Get command line arguments.

    """
    parser = argparse.ArgumentParser(
        description='Return formatted data records for a list of input UIDs.'
    )
    parser.add_argument(
        '-i',
        '--input-file',
        dest='infile',
        required=True,
        help='Path to file containing UIDs.'
    )
    parser.add_argument(
        '-o',
        '--output-directory',
        dest='outdir',
        required=True,
        help='Path to desired output directory.'
    )
    parser.add_argument(
        '-d',
        '--database',
        dest='db',
        required=True,
        help='Desired NCBI database to be searched.'
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()

    # Base URLs
    esearch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    elink_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
    esummary_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
    efetch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

    with open(args.infile, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # Skip header row
        # Globals
        query = False
        for row in reader:
            try:
                uuid = row[0].strip()
                filename = '{}.fa'.format(uuid)
                outfile = os.path.join(args.outdir, filename)
            except IndexError:
                continue
            # Dispatch esearch request
            esearch = requests.get(esearch_base + '?retmod=xml&db={}&term={}'.format(args.db, uuid))
            stree = ElementTree.fromstring(esearch.content)
            for snode in stree.iter('eSearchResult'):
                try:
                    # query_key = snode.find('QueryKey').text
                    # web_env = snode.find('WebEnv').text
                    accession = [x[0].text for x in snode.findall('IdList')]
                    query = accession[0]
                except IndexError, AttributeError:
                    print('No link.')
                    continue
            # Dispatch efetch request
            efetch = requests.get(efetch_base + '?db={}&id={}&rettype=fasta&retmode=text'.format(args.db, query))
            with open(outfile, 'wb') as fasta_out:
                fasta_out.write(efetch.text)

