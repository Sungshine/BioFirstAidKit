#!/usr/bin/env python

from Bio.Emboss.PrimerSearch import InputRecord, OutputRecord, Amplifier, read

handle = open("/Users/sungshine/Downloads/2012K-1420_LargeContigs.fna.primersearch", "r")

obj = read(handle)

# print(obj)
# for k, v in obj:
#     print(k, v)

for i in obj:
    print(i)