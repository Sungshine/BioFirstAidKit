__author__ = 'Sung Im'
#!/usr/bin/env python
import os
import csv
import subprocess
from timeit import default_timer

# Output is a directory containing the contig and scaffold files in FASTA format.
# Usage: module_SPAdes.py </path/to/inputfiles/> </path/to/output directory/>

# de-identify the R1/R2 tags# de-identify the R1/R2 tags
def wranglePairedEnds(RawReadPaths):
    for file in RawReadPaths:
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

# generate hash from line-list csv file to match up BCW_ID with strain_ID
def matchStrains(file):
    with open(file, "rb") as f:
        reader = csv.reader(f, delimiter=",")
        linelist = list(reader)
        for b in linelist:
            bcwID = b[1]
            strainID = b[2]
            if not bcwID in matchHash:
                matchHash[bcwID] = [strainID]

def moduleSpadesSE(inputfileOne):
    base = os.path.basename(inputfileOne)
    filename = os.path.splitext(base)[0]
    subprocess.call(["spades.py", "--careful", "-s", inputfileOne, "-o", SPAdesOutDirectory+filename+".spades",])

def moduleSpadesPE(inputfileOne, inputfileTwo,):
    base = os.path.basename(inputfileOne)
    filebase = os.path.splitext(base)[0]
    filename = filebase.split("-M")
    file = ""
    for key, value in matchHash.items():
        if filename[0] == value[0]:
             file = key
    subprocess.call(["spades.py", "--careful", "-1", inputfileOne, "-2", inputfileTwo, "-o", SPAdesOutDirectory+file+".spades",])

##################################################    Main Program    ##################################################
# time trials :)
start = default_timer()

# file = "/home/sim/PycharmProjects/genomics/sungRebecsMatchList.csv"   # strainIDs
inputDirectory = "/home/sim/Projects/test/reads/"                     # raw reads
SPAdesOutDirectory = "/home/sim/Projects/test/assemblies/"
RawReadPaths = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[2]]

fileHash = {}
matchHash = {}
wranglePairedEnds(RawReadPaths)
matchStrains(file)

for key in fileHash:

    currentValue = fileHash.get(key)
    sortedValue = sorted(currentValue)

    #call assemblers to execute single-end read
    if len(sortedValue) == 1:
        inputfileOne = sortedValue[0]
        moduleSpadesSE(inputfileOne)

    #execute paired-end reads
    if len(sortedValue) == 2:
        inputfileOne = sortedValue[0]
        inputfileTwo = sortedValue[1]
        moduleSpadesPE(inputfileOne, inputfileTwo)

# print "The SPAdes assemblies took: "+`default_timer() - start`