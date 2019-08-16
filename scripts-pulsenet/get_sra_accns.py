#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


""" Search NCBI's Sequence Read Archive database for meta information.
    Input: csv file with the with either SRA or BioSample id.
    Usage: fetch_ncbi_metadata.py -i < path/to/input/file > | cat > output.csv

"""


import re
import csv
import time
import json
import argparse
from Bio import Entrez
from collections import namedtuple


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Search NCBI for SRA and BioProject accessions.'
    )
    parser.add_argument(
        '-i', '--input-file',
        dest='infile',
        required=True,
        help='Path to input file'
    )
    parser.add_argument(
        '-o', '--output-file',
        dest='outfile',
        required=True,
        help='Path to output file'
    )
    return parser.parse_args()


def parseRun(expStr):
    """ Parse the Run object and return namedtuple of results """
    # Title - Other Sequencing of E. coli
    match = re.search('<Run acc=\"([A-Z0-9]*)\"', expStr)
    if match:
        srr_accn = '{}'.format(match.groups()[0])
        # print(srr_accn)
        return srr_accn
    else:
        return None


if __name__ == '__main__':
    
    # Read in the data  ##################################
    args = get_args()
    master = []
    with open(args.infile, 'rU') as fh:
        r = csv.reader(fh, delimiter='\t')
        next(r, None)   # Skip header
        for row in r:
            master.append(row[0].strip())

    """ One entry says 'Need Files' || Some entries have 'SRR_0000' """
    # for srrid in master:
    #     if srrid not in m.keys():
    #         print(srrid)
    

    # Call NCBI API ########################################
    Entrez.email = 'sungbin401@gmail.com'
    Entrez.api_key = 'd49444a436ec8a10255a08f52596634b9107'

    # We need a continuation method in case the script is stopped
    # Write to a temp file?
    # test = ['SAMN11267869']
    # test = ['PNUSAC008721']

    outlines = []

    for srr_id in master:
        # print('\n{}========'.format(srr_id))
        handle = Entrez.esearch(db='sra', term='{}'.format(srr_id))
        time.sleep(0.1)
        record = Entrez.read(handle)
        if len(record['IdList']) > 1:
            # print('{} returned more than one id in IdList'.format(srr_id))
            pn_id = srr_id
            srr = 'Duplicates found'
            outlines.append([pn_id, srr])
        else:
            try:
                k = record['IdList'][0]
                handle = Entrez.esummary(db='sra', id='{}'.format(k))
                time.sleep(0.1)
                record = Entrez.read(handle)
                # print(record[0])
                # print(record[0].get('Runs'))
                srr_accn = parseRun(record[0].get('Runs'))
                # print('{}\t{}'.format(srr_id, srr_accn))
                outlines.append([srr_id, srr_accn])
                # print(record[0].get('ExpXml'))
                # parseExp(record[0].get('ExpXml'))
            except Exception as e:
                print('{} returned error: {}'.format(srr_id, e))
                pn_id = srr_id
                srr = 'Error'
                outlines.append([pn_id, srr])
            

    with open(args.outfile, 'w') as outhandle:
        w = csv.writer(outhandle, delimiter='\t')
        for line in outlines:
            w.writerow(line)

# def parseExp(expStr):
#     """ Parse the ExpXml object and return namedtuple of results """
#     srr_meta = namedtuple('srrid', ['title', 'submitter', 'center','lab', 'experiment', 'platform', 'library', 'strategy', 'source', 'selection', 'layout', 'length', 'protocol', 'spots', 'bases', 'size', 'bioproject', 'biosample'])
#     # Title - Other Sequencing of E. coli
#     match = re.search('<Title>([A-Za-z0-9_\. \(\)]*)</Title>', expStr)
#     if match:
#         title = 'Title: {}'.format(match.group()[7:-8])
#         print(title)
#     # Submitter accession - SRA431725
#     match = re.search('<Submitter acc=\"([A-Z0-9]*)\"', expStr)
#     if match:
#         submitter = 'Submitter accession: {}'.format(match.groups()[0])
#         print(submitter)
#     # Center name - edlb-cdc
#     match = re.search('center_name=\"([A-Za-z0-9_\. \(\)\-]*)\"', expStr)
#     if match:
#         center_name = 'Center Name: {}'.format(match.groups()[0])
#         print(center_name)
#     # Lab name - Enteric Diseases Laboratory Branch
#     match = re.search('lab_name=\"([A-Za-z0-9_\. \(\)]*)\"', expStr)
#     if match:
#         lab_name = 'Lab Name: {}'.format(match.groups()[0])
#         print(lab_name)
#     # Experiment accession - SRX706426
#     match = re.search('<Experiment acc=\"([A-Z0-9]*)\"', expStr)
#     if match:
#         acc = 'Experiment accession: {}'.format(match.groups()[0])
#         print(acc)
#     # Platform - Illumina MiSeq
#     match = re.search('<Platform ([A-Za-z0-9_=\" \(\)]*)>([A-Za-z0-9_\(\)]*)</Platform>', expStr)
#     if match:
#         m = re.search('<Instrument {}=\"([A-Za-z0-9_\. \(\)]*)\"'.format(match.groups()[1]), expStr)
#         platform = 'Instrument: {}'.format(m.groups()[0])
#         print(platform)
#     # Library name - NexteraXT
#     match = re.search('<LIBRARY_NAME>([A-Za-z0-9_=\" \(\)]*)</LIBRARY_NAME>', expStr)
#     if match:
#         src = 'Library name: {}'.format(match.groups()[0])
#         print(src)
#     # Library strategy - WGS
#     match = re.search('<LIBRARY_STRATEGY>([A-Za-z0-9_=\" \(\)]*)</LIBRARY_STRATEGY>', expStr)
#     if match:
#         src = 'Library strategy: {}'.format(match.groups()[0])
#         print(src)
#     # Library source - GENOMIC
#     match = re.search('<LIBRARY_SOURCE>([A-Za-z0-9_=\" \(\)]*)</LIBRARY_SOURCE>', expStr)
#     if match:
#         src = 'Library source: {}'.format(match.groups()[0])
#         print(src)
#     # Library selection - RANDOM
#     match = re.search('<LIBRARY_SELECTION>([A-Za-z0-9_=\" \(\)]*)</LIBRARY_SELECTION>', expStr)
#     if match:
#         src = 'Library selection: {}'.format(match.groups()[0])
#         print(src)
#     # Library layout - PAIRED
#     match = re.search('<LIBRARY_LAYOUT> <([A-Za-z0-9]*)\/> <\/LIBRARY_LAYOUT>', expStr)
#     if match:
#         src = 'Library layout: {}'.format(match.groups()[0])
#         print(src)
#     # Nominal length 
#     match = re.search('<LIBRARY_LAYOUT> <([A-Za-z0-9]* )NOMINAL_LENGTH=\"([0-9]*)\"\/> <\/LIBRARY_LAYOUT>', expStr)
#     if match:
#         src = 'Nominal length: {}'.format(match.groups()[1])
#         print(src)
#     else:
#         src = 'Nominal length: {}'.format(' ')
#         print(src)
#     # Library construction protocol
#     match = re.search('<LIBRARY_CONSTRUCTION_PROTOCOL>([A-Za-z0-9_=\" \- \. ]*)<\/LIBRARY_CONSTRUCTION_PROTOCOL>', expStr)
#     if match:
#         src = 'Library protocol: {}'.format(match.groups()[0])
#         print(src)
#     # Sequence statistics
#     match = re.search('total_spots=\"([0-9]*)\" total_bases=\"([0-9]*)\" total_size=\"([0-9]*)\"', expStr)
#     if match:
#         spots = 'Total spots: {}'.format(match.groups()[0])
#         bases = 'Total bases: {}'.format(match.groups()[1])
#         size = 'Total size: {}'.format(match.groups()[2])
#         print(spots)
#         print(bases)
#         print(size)
#     # Bioproject
#     match = re.search('<Bioproject>([A-Za-z0-9]*)<\/Bioproject>', expStr)
#     if match:
#         bioproject = 'Bioproject: {}'.format(match.groups()[0])
#         print(bioproject)
#     # Biosample
#     match = re.search('<Biosample>([A-Za-z0-9]*)<\/Biosample>', expStr)
#     if match:
#         biosample = 'Biosample: {}'.format(match.groups()[0])
#         print(biosample)
