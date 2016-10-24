#!/usr/bin/python3

""" Descriptive text goes here

"""


import csv
from Bio.Emboss.PrimerSearch import InputRecord, OutputRecord, Amplifier, read
from Bio.Emboss.Applications import PrimerSearchCommandline


__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


# summaryTable = open('/Users/sungshine/Downloads/summary.table', 'r')
summaryTable = open('/home/sim/Projects/CIMS/salmonella/summary.table', 'r')
reader = csv.reader(summaryTable, delimiter="\t")

inPrimers = InputRecord()

for line in reader:
    inPrimers.add_primer_set(line[1], line[3], line[5])   # id, f_primer, r_primer
# print(inPrimers)
summaryTable.close()

seqall = '/Users/sungshine/Downloads/ATCC9150.fasta'
infile = '/Users/sungshine/Downloads/ATCC9150_Primers.txt'
outfile = '/Users/sungshine/Downloads/atcc9150.primersearch.out'

# seqall = '/home/sim/Projects/CIMS/salmonella/ATCC9150.fasta'
# infile = '/home/sim/Projects/CIMS/salmonella/ATCC9150primers.txt'
# outfile = '/home/sim/Projects/CIMS/salmonella/ATCC9150.primersearch.out'

mismatchpercentage = 3

emboss = PrimerSearchCommandline(r'/usr/bin/primersearch',
                                 seqall=seqall,
                                 infile=infile,
                                 mismatchpercent=mismatchpercentage,
                                 outfile=outfile
                                 )
print(emboss)



# handle = open("/home/sim/Projects/CIMS/salmonella/2012K-1420_LargeContigs.fna.primersearch", "r")  # pulsestar3

    # hit_dict = read(handle)

# for name in hit_dict.amplifiers:
#     for amplifier in hit_dict.amplifiers[name]:
#         print(name, "\n", amplifier.hit_info, "\n", amplifier.length, "\n")