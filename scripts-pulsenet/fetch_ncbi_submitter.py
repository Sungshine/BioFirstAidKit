#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


""" Search NCBI's Sequence Read Archive database for submitter information.

    Input: csv file with the with SRA accession ids.
    Usage: fetch_ncbi_submitter.py -i | cat > output.csv

"""


import csv
import requests
import argparse
from xml.etree import ElementTree


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Search NCBI for submitter ids.'
    )
    parser.add_argument(
        '-i',
        '--input-file',
        dest='infile',
        required=True,
        help='Path to input file.'
    )
    parser.add_argument(
        '-c',
        '--column-name',
        dest='column',
        required=True,
        help='Column header of data field to be searched.'
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()

    # Base URLs.
    esearch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    elink_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
    esummary_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
    efetch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

    # Print headers for outfile
    # TODO Use the headers in the input file and print those
    print('{},{},{},{},{},{},'
          .format('strain_ID', 'Sequencing_ID', 'O_or_H_standard',
                  'SRA_Accession', 'BioProject_Accession', 'Submitter'))

    # Read input file
    with open(args.infile, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        row_index = False
        for row in reader:
            # Capture column name of field containing ids to be searched
            for field in row:
                if args.column in field:
                    row_index = row.index(field)
                    break
            try:
                srr_id = row[row_index]
            except IndexError:
                continue
            # Dispatch esearch request
            esearch = requests.get(esearch_base + '?retmode=xml&db=sra&term={}&usehistory=y'
                                   .format(srr_id))
            stree = ElementTree.fromstring(esearch.content)
            for snode in stree.iter('eSearchResult'):
                try:
                    query_key = snode.find('QueryKey').text
                    web_env = snode.find('WebEnv').text
                    accession = [x[0].text for x in snode.findall('IdList')]
                    sra_id = accession[0]
                except IndexError, AttributeError:
                    continue
                # Dispatch efetch request
                efetch = requests.get(efetch_base + '?db=sra&id={}'
                                      .format(sra_id))
                ftree = ElementTree.fromstring(efetch.content)
                for fnode in ftree.iter('SUBMITTER_ID'):
                    for value in fnode.attrib.values():
                        print('{},{},{},{},{},{},'
                              .format(row[0].rstrip(' '), row[1].rstrip(' '),
                                      row[2].rstrip(' '), row[3].rstrip(' '),
                                      row[4].rstrip(' '), value.rstrip(' ')))
                        break
                    break
