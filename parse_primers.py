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

with open("/home/sim/Projects/CIMS/salmonella/primers/summary.table", "rb") as infile:
    reader = csv.reader(infile, delimiter="\t")

    for line in reader:
        # print line
        # print line[2], line[3], line[4], line[5]

        left_primer.append(line[3])
        right_primer.append(line[5])

    lpu = set(left_primer)
    rpu = set(right_primer)
    print("left primer count = {}".format(len(left_primer)))
    print("left primer unique = {}".format(len(lpu)))
    print("right primer count = {}".format(len(right_primer)))
    print("right primer unique = {}".format(len(rpu)))