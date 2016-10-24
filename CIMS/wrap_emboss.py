#!/usr/bin/python3

""" Attempt at wrapping BioPython.EMBOSS module.

Used for testing specificity of primer sets.

"""

# import statements go here
import csv

__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


gene_dict = {}

with open("/Users/sungshine/Downloads/summary.table", "r") as f:
    reader = csv.reader(f, delimiter="\t")

    for line in reader:

        id = line[0]
        fid = line[1]
        lp = line[3]
        rp = line[5]
        prokka_id = id.split(".")[3]
        prokka_id_pair = fid.split(".")[9]
        pair_id = prokka_id+"."+prokka_id_pair

        if id in gene_dict.keys():
            gene_dict[id].append({pair_id: [lp, rp]})
        else:
            gene_dict[id] = [{pair_id: [lp, rp]}]

for k, v in gene_dict.items():
    print(k, v)
