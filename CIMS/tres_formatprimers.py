#!/usr/bin/python3

""" Wrapped BioPython.EMBOSS module to handle EMBOSS PrimerSearch.

"""


import csv


__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


def format_primers(handle):
    """ Format primer sets for input into primersearch program.

    """
    record = []
    reader = csv.reader(handle, delimiter='\t')
    for line in reader:
        primer_set = '{}\t{}\t{}\n'.format(line[1], line[3], line[5])
        record.append(primer_set)
    return record


if __name__ == "__main__":

    # print the list of records out to a file
    with open('/home/sim/Projects/CIMS/salmonella/summary.table', 'r') as summarytable, \
            open('/home/sim/Projects/CIMS/salmonella/summary.table.format', 'wb') as formatted:
            primer_sets = format_primers(summarytable)
            for item in primer_sets:
                formatted.write(bytes(item, 'UTF-8'))