#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Fetch metadata for isolates in dataset from SRA.

"""

import os
import re
import csv
import time
import argparse
from Bio import Entrez
from pprint import pprint
import xml.etree.cElementTree as ET


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Grid-search to find optimal parameter settings.'
    )
    parser.add_argument(
        '-i', '--input-file',
        dest='infile',
        required=True,
        help='Path to file containing list of SRR ids, should contain a header'
    )
    parser.add_argument(
        '-o', '--output-file',
        dest='outfile',
        required=True,
        help='Path to desired output file'
    )
    return parser.parse_args()


def read_input_file(f):
    """ Input file should contain a header and then SRR ids """
    srr_ids = []
    with open(f, 'r') as fh:
        r = csv.reader(fh, delimiter='\t')
        next(r, None)   # skip header row
        for row in r:
            srr_ids.append(row[0].strip())
    assert len(srr_ids) == len(set(srr_ids)), 'Your list of SRR ids contains duplicates!'
    return srr_ids


if __name__ == '__main__':

    args = get_args()
    Entrez.email = 'wla9@cdc.gov'

    header = [
        'sra_id', 'run_accn', 'primary_id', 'pulsenet_id', 'platform', 'bioproject_accn',
        'biosample_accn', 'submission_accn', 'study_accn', 'experiment_accn', 'sample_accn',
        'organism_name', 'instrument_model', 'library_name', 'library_strategy',
        'library_source', 'library_selection', 'library_layout', 'submitter_id', 'submission_date'
        ]

    # Store the results as a list of lists for writing later
    outlines = [header]

    # Load list of sra ids
    list_of_sra_ids = read_input_file(args.infile)
    # list_of_sra_ids = ['SRR1605254', 'SRR1610025', 'SRR1610035']

    # Build dict of { sra id: primary ids }
    empty_sra_ids = []
    sra_to_pid = {}

    for sra_id in list_of_sra_ids:
        handle = Entrez.esearch(db='sra', term=sra_id, max_tries=5, sleep_between_tries=15)
        records = Entrez.read(handle)
        if len(records['IdList']) == 0:
            empty_sra_ids.append(sra_id)
            continue
        if len(records['IdList']) > 1:
            pass
        if len(records['IdList']) == 1:
            if sra_id not in sra_to_pid.keys():
                sra_to_pid[sra_id] = records['IdList'][0]
            else:
                print('Duplicate SRA Id = {}'.format(sra_id))
        handle.close()
        time.sleep(.300)

    # Get metadata information
    for sra_id, pid in sra_to_pid.items():

        # Desired fields
        run_accn = ''           # SRR4300144
        primary_id = ''         # 1048582
        pulsenet_id = ''        # PNUSAE004321, 2014C-3799
        platform = ''           # Illumina MiSeq
        bioproject_accn = ''    # PRJNA218110
        biosample_accn = ''     # SAMN04913827
        submission_accn = ''    # SRA480736
        study_accn = ''         # SRP046387
        experiment_accn = ''    # SRX2194690
        sample_accn = ''        # SRS1716869
        organism_name = ''      # Escherichia coli
        instrument_model = ''   # Illumina MiSeq
        library_name = ''       # NexteraXT
        library_strategy = ''   # WGS
        library_source = ''     # GENOMIC 
        library_selection = ''  # RANDOM 
        library_layout = ''     # PAIRED
        submitter_id = ''       # Centers for Disease Control
        submission_date = ''    # 2016-09-21

        # Grab the submission_date
        handle = Entrez.efetch(db='sra', id=pid, max_tries=5, sleep_between_tries=15)
        xml = ''.join(handle.readlines())
        tree = ET.fromstring(xml)
        for node in tree.iter():    
            # print('{}\t{}\t{}'.format(node.tag, node.attrib, node.text))
            if node.tag == 'RUN':
                try:
                    submission_date = node.attrib['published']
                except Exception as e:
                    submission_date = 'NA'
        handle.close()
        time.sleep(.300)

        # Grab everything else
        handle = Entrez.esummary(db='sra', id=pid, retmode="xml", max_tries=5, sleep_between_tries=15)
        records = Entrez.read(handle)
        for record in records:
            # Format ExpXml string into an actual xml string
            xml = '<?xml version="1.0"?>' + record['ExpXml']
            tree = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")
            for node in tree.iter():

                run_accn = sra_id
                primary_id = pid
                
                if node.tag == 'Platform':
                    try:
                        platform = node.attrib['instrument_model']
                    except Exception as e:
                        platform = 'NA'

                if node.tag == 'Submitter':
                    try:
                        submission_accn = node.attrib['acc']
                    except Exception as e:
                        submission_accn = 'NA'

                if node.tag == 'Submitter':
                    try:
                        submitter_id = node.attrib['center_name']
                    except Exception as e:
                        submitter_id = 'NA'
                
                if node.tag == 'Experiment':
                    try:
                        experiment_accn = node.attrib['acc']
                    except Exception as e:
                        experiment_accn = 'NA'
                
                if node.tag == 'Study':
                    try:
                        study_accn = node.attrib['acc']
                    except Exception as e:
                        study_accn = 'NA'
                
                if node.tag == 'Organism':
                    try:
                        organism_name = node.attrib['ScientificName']
                    except Exception as e:
                        organism_name = 'NA'
                
                if node.tag == 'Sample':
                    try:
                        sample_accn = node.attrib['acc']
                    except Exception as e:
                        sample_accn = 'NA'

                if node.tag == 'Instrument':
                    try:
                        instrument_model = node.attrib['ILLUMINA']
                    except Exception as e:
                        instrument_model = 'NA'

                if node.tag == 'LIBRARY_NAME':
                    try:
                        library_name = node.text.strip()
                    except Exception as e:
                        library_name = 'NA'

                if node.tag == 'LIBRARY_STRATEGY':
                    try:
                        library_strategy = node.text.strip()
                    except Exception as e:
                        library_strategy = 'NA'

                if node.tag == 'LIBRARY_SOURCE':
                    try:
                        library_source = node.text.strip()
                    except Exception as e:
                        library_source = 'NA'
                
                if node.tag == 'LIBRARY_SELECTION':
                    try:
                        library_selection = node.text.strip()
                    except Exception as e:
                        library_selection = 'NA'
                
                if node.tag == 'PAIRED':
                    try:
                        library_layout = 'PAIRED'
                    except Exception as e:
                        library_layout = 'NA'
                
                if node.tag == 'Bioproject':
                    try:
                        bioproject_accn = node.text.strip()
                    except Exception as e:
                        bioproject_accn = 'NA'
                
                if node.tag == 'Biosample':
                    try:
                        biosample_accn = node.text.strip()
                    except Exception as e:
                        biosample_accn = 'NA'
            
        handle.close()
        time.sleep(.300)

        outlines.append(
            [
                sra_id, run_accn, primary_id, pulsenet_id, platform, bioproject_accn,
                biosample_accn, submission_accn, study_accn, experiment_accn, sample_accn,
                organism_name, instrument_model, library_name, library_strategy,
                library_source, library_selection, library_layout, submitter_id, submission_date,
            ]
        )

    # Write results to file
    with open(args.outfile, 'w') as outhandle:
        writer = csv.writer(outhandle, delimiter='\t')
        for line in outlines:
            writer.writerow(line)
