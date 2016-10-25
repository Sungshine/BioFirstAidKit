#!/usr/bin/python3

""" Unpack and parse output from Kraken-translate.

"""


import os
import csv
import pickle
import subprocess
from Bio.Emboss.PrimerSearch import InputRecord, OutputRecord, Amplifier, read
from Bio.Emboss.Applications import PrimerSearchCommandline


__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


krakenLabels = '/home/sim/Projects/CIMS/salmonella/2013RAN-169-M947-14-049-Loopy_contigs4.sequence.labels'
unclassifiedLabels = '/home/sim/Projects/CIMS/salmonella/2013RAN-169-M947-14-049-Loopy_contigs4.fasta.unclassified'

with open(krakenLabels) as k, open(unclassifiedLabels) as u:

    otherContigs = {}
    targetContigs = {}
    unclassifiedContigs = []

    for line in k:
        contigId = line.rstrip().split('\t')[0]
        classify = line.rstrip().split('\t')[1].split(';')[-1]
        if "Salmonella" in line:
            targetContigs[contigId] = classify
        elif "Salmonella" not in line:
            otherContigs[contigId] = classify

    for line in u:
        if line.startswith('>'):
            contigId = line.split(' ')[0].lstrip('>')
            unclassifiedContigs.append(contigId)


summaryTable = '/home/sim/Projects/CIMS/salmonella/summary.table'

# TODO the path below needs to be configured for ASPEN environment - seems to be a permission issue to write to the GWA file storage
# inputPrimers = '/scicomp/groups/OID/NCEZID/DFWED/EDLB/share/projects/CIMS/Salmonella/PrimerSpecificity/{}.inputPrimers'\
#     .format(os.path.basename(summaryTable))
# inputPrimers = '/mnt/GWA/projects/CIMS/Salmonella/PrimerSpecificity/{}.inputPrimers'\
#     .format(os.path.basename(summaryTable))

inputPrimers = '/home/sim/Projects/CIMS/salmonella/{}.inputPrimers'.format(os.path.basename(summaryTable))

with open(summaryTable) as s:
    reader = csv.reader(s, delimiter='\t')
    inPrimers = InputRecord()
    for line in reader:
        inPrimers.add_primer_set(line[1], line[3], line[5])
    s.close()

    # InputRecord() parses the summary.tables file, now write it to an inPrimers file
    with open(inputPrimers, 'wb') as w:
        pickle.dump(str(inPrimers), w, pickle.HIGHEST_PROTOCOL)
    w.close()
    # seqall = '/home/sim/GWA/projects/metagenomics/COAL/assembly/2013RAN-169-M947-14-049-Loopy_contigs4.fasta' # This is where I want to work from
    # outfile = '/home/sim/GWA/Salmonella/PrimerSpecificity/embossResults/{}.emboss.out'\
    #     .format(os.path.basename(seqall))

    seqall = '/home/sim/Projects/CIMS/salmonella/2013RAN-169-M947-14-049-Loopy_contigs4.fasta'
    outfile = '/home/sim/Projects/CIMS/salmonella/embossResults/{}.emboss2'.format(os.path.basename(seqall))

    emboss = PrimerSearchCommandline(seqall=seqall,
                                     infile=inputPrimers,
                                     mismatchpercent=3,
                                     outfile=outfile
                                     )
    # print(emboss)
    ps = subprocess.Popen(str(emboss).split(' '))

    with open(outfile) as embossOut:
        my_dict = read(embossOut)
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

for contigId in contigHits:
    print(contigId)