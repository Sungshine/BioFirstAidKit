__author__ = 'Sung Im'
#!/usr/bin/env python
import os
from Bio import SeqIO

# Convert sequence files from genbank format to fasta format.
inputDirectory = "/home/sim/Projects/ANI/tmp"
paths = [os.path.join(inputDirectory,fn) for fn in next(os.walk(inputDirectory))[2]]
    
for file in paths:

    base = os.path.basename(file)
    next = os.path.splitext(base)[0]
    keyname = os.path.splitext(next)[0]

    input_handle = open(file, "rU")
    output_handle = open("/home/sim/Projects/ANI/tmp/%s.fasta" % (keyname,), "w")
    
    sequences = SeqIO.parse(input_handle, "genbank")
    count = SeqIO.write(sequences, output_handle, "fasta")
    
    input_handle.close()
    output_handle.close()
    print "Conversion of "+keyname+" to fasta format has completed."
