#!/usr/bin/python3

import csv
from Bio.Emboss.PrimerSearch import InputRecord, OutputRecord, Amplifier, read
from Bio.Emboss.Applications import PrimerSearchCommandline

summaryTable = open('/Users/sungshine/Downloads/summary.table', 'r')
reader = csv.reader(summaryTable, delimiter="\t")

inPrimers = InputRecord()

for line in reader:
    inPrimers.add_primer_set(line[1], line[3], line[5])   # id, f_primer, r_primer
# print(inPrimers)
summaryTable.close()

seqall = '/Users/sungshine/Downloads/sakai.fasta'
infile = '/Users/sungshine/Downloads/sakaiPrimers.txt'
outfile = '/Users/sungshine/Downloads/sakai.primersearch.out'
mismatchpercentage = 5
emboss = PrimerSearchCommandline(seqall=seqall,
                                 infile=infile,
                                 mismatchpercent=mismatchpercentage,
                                 outfile=outfile
                                 )
# print(emboss)



# handle = open("/home/sim/Projects/CIMS/salmonella/2012K-1420_LargeContigs.fna.primersearch", "r")  # pulsestar3

    # hit_dict = read(handle)

# for name in hit_dict.amplifiers:
#     for amplifier in hit_dict.amplifiers[name]:
#         print(name, "\n", amplifier.hit_info, "\n", amplifier.length, "\n")