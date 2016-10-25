#!/usr/bin/python3

""" Descriptive text goes here

"""


# import statements go here
import csv
import pickle

__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


class InputRecord(object):
    """ Parse and format input file for primersearch program.

    Modified from http://biopython.org/DIST/docs/api/
    """
    def __init__(self):
        self.primer_info = []

    def __str__(self):
        output = ''
        for name, primer1, primer2 in self.primer_info:
            output += '{}\t{}\t{}\n'.format(name, primer1, primer2)
        return output

    def add_primer_set(self, primer_id, f_primer, r_primer):
        """ Add primer information to the record.

        """
        self.primer_info.append((primer_id, f_primer, r_primer))


if __name__ == "__main__":

    # Parse summary.table and format for input into EMBOSS primer search
    mnt = '/mnt/scicomp-groups/OID/NCEZID/DFWED/EDLB/share/projects/CIMS/Salmonella/PrimerSpecificity/'
    inputone = mnt + 'Sal-JEG-FDA00004012_summary.table'

    tmp = '/home/sim/tmp/'
    outputone = tmp + 'Sal-JEG-FDA00004012_summary.table'

    with open(inputone, 'r') as summary_table, \
            open('{}.primed'.format(outputone), 'wb') as inPrimers:

        record = InputRecord()

        reader = csv.reader(summary_table, delimiter='\t')
        for line in reader:
            record.add_primer_set(line[1], line[3], line[5])

        writer = csv.writer(inPrimers, delimiter='\t')
        writer.writerow(record)



