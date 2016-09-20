#!/usr/bin/env python2.7

""" Given a list of NCBI accession ids, download in fasta format using
Python Requests library & NCBI's API.

"""

import os
import csv
import requests
import xml.etree.ElementTree as ET

__author__  = "Sung Im"
__email__   = "wla9@cdc.gov"


csv_path = "/scicomp/home/wla9/Projects/Poo/285_stx_masterlist.tsv"
storage_path = "/scicomp/home/wla9/Projects/Poo/data/stx_genes/"

accns = []
hash = {}

with open(csv_path, "rb") as tsvin:
    reader = csv.reader(tsvin, delimiter="\t")
    next(reader, None)
    for row in reader:
        accns.append(row[3])
        hash[row[3]] = row[0]

for accn in accns:
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_url = base + "esearch.fcgi?db=nucleotide&term={}&usehistory=y".format(accn)
    r0 = requests.get(search_url, timeout=25)
    # xml object conversion
    root = ET.fromstring(r0.text)
    # capture necessary info from xml to pass to ncbi-efetch
    query_key = root[3].text
    web_env = root[4].text
    fetch_url = base + "efetch.fcgi?db=nucleotide&query_key={}&WebEnv={}&rettype=fasta&retmode=text".format(query_key, web_env)
    blocksize = 20971520
    r1 = requests.get(fetch_url, stream=True, timeout=25)
    out_path = storage_path + "{}_{}.fasta".format(accn, hash[accn])
    try:
        with open(out_path, "wb") as fasta:
            os.chmod(out_path, 0o755)
            for block in r1.iter_content(blocksize):
                fasta.write(block)
    except (Exception, KeyboardInterrupt) as e:
        print("Unable to download {}: {}".format(accn, e))