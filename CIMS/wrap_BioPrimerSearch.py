#!/usr/bin/python3

""" Wrapped BioPython.EMBOSS module to handle EMBOSS PrimerSearch.

"""


import csv
import subprocess
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

seqall = '/home/sim/Projects/CIMS/salmonella/ATCC9150.fasta'
infile = '/home/sim/Projects/CIMS/salmonella/ATCC9150primers.txt'
outfile = '/home/sim/Projects/CIMS/salmonella/ATCC9150.primersearch.out'

mismatchpercentage = 3

emboss = PrimerSearchCommandline(r'/usr/bin/primersearch',
                                 seqall=seqall,
                                 infile=infile,
                                 mismatchpercent=mismatchpercentage,
                                 outfile=outfile
                                 )

# print(emboss)
ps = subprocess.Popen(str(emboss).split(' '))

## Let's parse the output from EMBOSS
handle = open('/home/sim/Projects/CIMS/salmonella/2012K-1420_LargeContigs.fna.emboss.out') # test case

my_dict = read(handle)
no_hits = []
contigHits = []

for name in my_dict.amplifiers:
    # create list of primer pairs that did not amplify
    if len(my_dict.amplifiers[name]) != 0:
        no_hits.append(name)
    for amplifier in my_dict.amplifiers[name]:
        ampliconLen = amplifier.length
        contigId = amplifier.hit_info.split('\n')[0]
        contigLen = amplifier.hit_info.split('\n')[1].replace('\tlength=', '').rsplit()[0]
        fprimer = amplifier.hit_info.split('\n')[2].split(' ')[0].lstrip('\t')
        fstart = amplifier.hit_info.split('\n')[2].split(' ')[5]
        fmismatch = amplifier.hit_info.split('\n')[2].split(' ')[7]
        rprimer = amplifier.hit_info.split('\n')[3].split(' ')[0].lstrip('\t')
        rstart = amplifier.hit_info.split('\n')[3].split(' ')[5].strip('[]')
        rmismatch = amplifier.hit_info.split('\n')[3].split(' ')[7]

        contigHits.append(contigId)

handle.close()

# handle = open("/home/sim/Projects/CIMS/salmonella/2012K-1420_LargeContigs.fna.primersearch", "r")
#     hit_dict = read(handle)
# for name in hit_dict.amplifiers:
#     for amplifier in hit_dict.amplifiers[name]:
#         print(name, "\n", amplifier.hit_info, "\n", amplifier.length, "\n")