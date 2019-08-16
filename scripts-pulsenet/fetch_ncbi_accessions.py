#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


""" Search NCBI Biosample database for SRA and SAMN accession ids.

    Input format: .csv file with pulsenet wgs accessions

"""


import csv
import time
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
    parser.add_argument(
        '-o', '--output-file',
        dest='outfile',
        required=True,
        help='Path to out file, .csv'
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()

    # API parameters
    api_key = 'd49444a436ec8a10255a08f52596634b9107'

    # Base URLs
    esearch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    elink_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
    esummary_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
    efetch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

    # Output list
    outlines = []

    # Print headers for outfile
    outlines.append(['WGS_id', 'SRR_id', 'SAMN_id'])

    # Read input file
    with open(args.infile, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # Skip header row
        for row in reader:
            try:
                wgs_id = row[0]
            except IndexError:
                continue

            # Dispatch esearch request
            esearch = requests.get(
                '{}?retmode=xml&db=biosample&term={}&usehistory=y&api_key={}'.format(
                    esearch_base, wgs_id, api_key)
                )
            # Parse xml response object from esearch
            stree = ElementTree.fromstring(esearch.content)
            for snode in stree.iter('eSearchResult'):
                try:
                    query_key = snode.find('QueryKey').text
                except IndexError, AttributeError:
                    continue
                try:
                    web_env = snode.find('WebEnv').text
                    accession = [x[0].text for x in snode.findall('IdList')]
                except IndexError, AttributeError:
                    outlines.append([wgs_id, 'WGS_Id !exist', 'SAMN unavailable']) 
                    continue

                # Dispatch esummary request
                esummary = requests.get(
                    '{}?retmode=xml&db=biosample&WebEnv={}&query_key={}&api_key={}'.format(
                        esummary_base, web_env, query_key, api_key
                        )
                    )
                # Parse xml response object from esummary.
                sumtree = ElementTree.fromstring(esummary.content)
                for sumnode in sumtree.iter('Accession'):
                    try:
                        samn = sumnode.text
                    except IndexError:
                        samn = False
                        continue

                # Dispatch elink request
                elink = requests.get(
                    '{}?retmode=xml&dbfrom=biosample&db=sra&id={}&api_key={}'.format(
                        elink_base, accession, api_key
                        )
                    )
                # Parse xml response object from elink
                etree = ElementTree.fromstring(elink.content)
                for enode in etree.findall('LinkSet'):
                    link = enode.find('LinkSetDb')
                    if link is None:
                        try:
                            outlines.append([wgs_id, 'SRR unavailable', samn])
                        except NameError:
                            outlines.append([wgs_id, 'NameError', 'elink'])
                            continue
                    else:
                        link = link.find('Link')
                        sraid = link[0].text
                        # Dispatch efetch request
                        efetch = requests.get(
                            '{}?db=sra&id={}&api_key={}'.format(
                                efetch_base, sraid, api_key
                                )
                            )
                        # Parse xml response object from efetch
                        ftree = ElementTree.fromstring(efetch.content)
                        for fnode in ftree.iter('IDENTIFIERS'):
                            primary_id = fnode[0].text
                            if 'SRR' in primary_id:
                                outlines.append([wgs_id, primary_id, samn])

            time.sleep(0.5)
        
    # Write outfile
    with open(args.outfile, 'wB') as out_handle:
        w = csv.writer(out_handle, delimiter=',')
        for row in outlines:
            w.writerow(row)
