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


class HypoGene(object):
    """

    """
    def __init__(self):
        self.id = ""



def parse(handle):

    primer_dict = OutputRecord()
    # primer_sets = OutputRecord()

    reader = csv.reader(handle, delimiter="\t")

    for line in reader:
        id = line[1]
        f_primer = line[3]
        r_primer = line[5]
        prokka_id = id.split(".")[3]
        prokka_id_pair = id.split(".")[9]





# with open("/home/sim/Projects/CIMS/salmonella/summary.table", "r") as infile:
#     reader = csv.reader(infile, delimiter="\t")
#
#     for line in reader:
