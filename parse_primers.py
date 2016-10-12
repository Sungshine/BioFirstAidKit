#!/usr/bin/env python

""" Parse primer pairs from summary.table

"""

import re
import sys
import csv

__author__  = "Sung Im"
__email__   = "wla9@cdc.gov"

left_primer = []
right_primer = []
leftright_primer = []
primer_dict = dict()

with open("/Users/sungshine/Downloads/summary.table", "rb") as infile:
# with open("/home/sim/Projects/CIMS/salmonella/primers/summary.table", "rb") as infile:
    reader = csv.reader(infile, delimiter="\t")

    for line in reader:

        l_primer = line[3]
        r_primer = line[5]

        # dict = { key : [ left_primer, right_primer ] }
        if line[1] in primer_dict:
            primer_dict[line[1]].append([l_primer, r_primer])
        else:
            primer_dict[line[1]] = [ l_primer, r_primer ]

for key, value in primer_dict.items():
    print(key, value)



    # Sanity checking the unique combinations of primer pairs
    #
        # left_primer.append(line[3])
        # right_primer.append(line[5])
        # leftright_primer.append(l_primer+r_primer)
    #
    # lpu = set(left_primer)
    # rpu = set(right_primer)
    # lru = set(leftright_primer)
    # print(len(left_primer))         # left primer count = 10035
    # print(len(lpu))                 # left primer unique = 5358
    # print(len(right_primer))        # right primer count = 10035
    # print(len(rpu))                 # right primer unique = 5226
    # print(len(leftright_primer))    # left + right = 10035
    # print(len(lru))                 # left + right unique = 10024