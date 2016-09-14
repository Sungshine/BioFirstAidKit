__author__ = 'Sung Im'
#!/usr/bin/env python
import os
import sys
import subprocess

# Generates hash of trimmed reads and invokes either SE or PE SPAdes de novo assembly.
# Output is a directory containing the contig and scaffold files in FASTA format.
# Usage: module_SPAdes.py </path/to/inputfiles/> </path/to/output directory/>

def wranglePairedEnds(paths):
    for file in paths:
        newfile = ""
        if "R1" in file:
            newfile = file.replace("R1", "R*")
        elif "R2" in file:
            newfile = file.replace("R2", "R*")
        if not newfile in fileHash:
            fileHash[newfile] = [file]
        else:
            fileHash[newfile].append(file)
    return

def moduleSpadesSE(inputfileOne):
    base = os.path.basename(inputfileOne)
    filename = os.path.splitext(base)[0]
    subprocess.call(["spades.py", "--careful", "-s", inputfileOne, "-o", outputDirectory+filename+".spades",])

def moduleSpadesPE(inputfileOne, inputfileTwo):
    base = os.path.basename(inputfileOne)
    filename = os.path.splitext(base)[0]
    subprocess.call(["spades.py", "--careful", "-1", inputfileOne, "-2", inputfileTwo, "-o", outputDirectory+filename+".spades",])


########################################################################################################################
###                                                   MAIN PROGRAM                                                   ###
########################################################################################################################


inputDirectory = "/home/sim/Projects/test/reads/"    #point to directory of trimmed (prinseq) files.
outputDirectory ="/home/sim/Projects/test/assemblies/"   #point to output directory where SPAdes assemblies will be stored.

fileHash = {}
paths = [os.path.join(inputDirectory,fn) for fn in next(os.walk(inputDirectory))[2]]

wranglePairedEnds(paths)    #generates hash of paired-end files

inputfileOne = ""
inputfileTwo = ""

for key in fileHash:

    hashValues = fileHash.get(key)
    sortedValues = sorted(hashValues)   #sorts the file-path(s)-values in hash

    if len(sortedValues) == 1:          #if key in hash has one value, invoke SPAdes for single-end read
        inputfileOne = sortedValues[0]

        moduleSpadesSE(inputfileOne)

    if len(sortedValues) == 2:          #if key in hash has two values, invoke SPAdes for paired-end reads
        inputfileOne = sortedValues[0]
        inputfileTwo = sortedValues[1]

        moduleSpadesPE(inputfileOne, inputfileTwo)
