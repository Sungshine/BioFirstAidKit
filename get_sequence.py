#!/usr/bin/env python2.7

"""
"""

import csv
import requests

__author__  = "Sung Im"
__email__   = "wla9@cdc.gov"

csv_path = "/scicomp/home/wla9/Projects/Poo/285_stx_masterlist.tsv"

accns = []

with open(csv_path, "rb") as tsvin:
    reader = csv.reader(tsvin, delimiter="\t")

    for row in reader:
        accns.append(row[3])

for accn in accns:

    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    url = base + "esearch.fcgi?db=nucleotide&term={}&usehistory=y".format(accn)

    r = requests.get(url)
    j = r.json()
    print j