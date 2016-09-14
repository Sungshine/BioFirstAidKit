__author__ = 'Sung Im'
#!/usr/bin/env python
#from Bio import SeqIO
import os

inputDirectory = "/home/sim/Projects/mumVSani/data"
paths = [os.path.join(inputDirectory,fn) for fn in next(os.walk(inputDirectory))[2]]

for file in paths:

    basename = os.path.basename(file)
    newFilename = os.path.splitext(basename)[0]

    inputHandle = open(file, "rU")
    outputHandle = open("/home/sim/Projects/mumVSani/%s.headers.fasta" % (newFilename,), "w")

    for line in inputHandle:
        if line.startswith('>'):
            outputHandle.write()

    inputHandle.close()
    outputHandle.close()