#!/usr/bin/env python

""" Search NCBI Biosample database for SRR ids.

Given a csv file containing a header and PulseNet WGS ids.
Usage: python eutils_helper.py < path/to/inputfile > | cat > < path/to/outputfile >
"""

import sys
import csv
import requests
from xml.etree import ElementTree


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.1'


# globals
esearch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
elink_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
efetch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

inputcsv = sys.argv[1]

# Print output file csv header
print('{}, {}'.format('WGS_id', 'SRR_id'))

# Read in csv file containing PulseNet WGS ids
with open(inputcsv, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)  # skips the header
    for row in reader:
        wgs_id = row[0]

        # The esearch api call
        esearch_resp = requests.get(esearch_base
                                    +'?retmode=xml&db=biosample&term={}&usehistory=y'
                                    .format(wgs_id))
        # Parse xml response object from esearch
        s_tree = ElementTree.fromstring(esearch_resp.content)
        for s_node in s_tree.iter('IdList'):
            try:
                s_id = s_node[0].text
            except IndexError, KeyError:
                print('{}, {}'.format(wgs_id, 'WGS id does not exist'))

            # The elink api call
            elink_resp = requests.get(elink_base + '?retmode=xml&dbfrom=biosample&db=sra&id={}'.format(s_id))
            # Parse xml response object from elink
            e_tree = ElementTree.fromstring(elink_resp.content)
            for e_node in e_tree.findall('LinkSet'):
                # If no links exist, move on to next id
                link = e_node.find('LinkSetDb')
                if link is None:
                    print('{}, {}'.format(wgs_id, 'No SRR id linked'))
                    continue
                else:
                    link = link.find('Link')
                    e_id = link[0].text

                    # The efetch api call
                    efetch_resp = requests.get(efetch_base + '?db=sra&id={}'.format(e_id))
                    # Parse xml response object from efetch
                    f_tree = ElementTree.fromstring(efetch_resp.content)
                    for f_node in f_tree.iter('IDENTIFIERS'):
                        primary_id = f_node[0].text
                        if 'SRR' in primary_id:
                            print('{}, {}'.format(wgs_id, primary_id))