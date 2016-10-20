#!/usr/bin/python3

""" Descriptive Text Goes Here

"""

# import statements go here
import csv

__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


primer_dict = {}
primer_sets = {}


class OutputRecord(object):
    """

    """
    def __init__(self):
        self.items = {}


class GeneInfo(object):
    """

    """
    def __init__(self):
        self.id = ""
        self.f_primer = ""
        self.r_primer = ""
        self.pairs = []



def parse(handle):

    primer_dict = OutputRecord()

    reader = csv.reader(handle, delimiter="\t")

    for line in reader:
        id = line[1]
        f_primer = line[3]
        r_primer = line[5]
        prokka_id = id.split(".")[3]
        prokka_id_pair = id.split(".")[9]

        primer_dict.items[prokka_id] = []
        geneinfo = GeneInfo()
        primer_dict.items[prokka_id].append(geneinfo)
        geneinfo.id = id
        geneinfo.f_primer = f_primer
        geneinfo.r_primer = r_primer

        # if prokka_id in primer_dict:
        geneinfo.pairs.append(prokka_id_pair)

    return primer_dict


if __name__ == "__main__":

    with open("/Users/sungshine/Downloads/summary.table", "r") as infile:

        my_dict = parse(infile)

        for name in my_dict.items:
            for geneinfo in my_dict.items[name]:
                print(name)
                print(geneinfo.id)
                print(geneinfo.f_primer)
                print(geneinfo.r_primer)
                print(geneinfo.pairs)


# with open("/home/sim/Projects/CIMS/salmonella/summary.table", "r") as infile:
#     reader = csv.reader(infile, delimiter="\t")
#
#     for line in reader:
