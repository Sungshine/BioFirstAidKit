__author__ = 'Sung Im'
#!/usr/bin/env python
import os
import sys
import subprocess
from timeit import default_timer

# Run ani-blast on multiple genome assemblies in a pairwise fashion.
# Writes to STDOUT in csv format for easy importing to excel.
# Usage: python multiANI.py /path/to/data/ /absolute/path/to/ani.script > output.csv

#start = default_timer()
inputDirectory = sys.argv[1]    #"/home/sim/Projects/ANI/aniBlastData/"
aniPath = sys.argv[2]           #"/home/sim/Setup/enveomics-master/Scripts/ani.rb"

paths = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[2]]

aniMatrix = [[[] for i in range(len(paths))] for j in range(len(paths))]    #initialize 2D array

for i in range(len(paths)):
    aniMatrix[i][i] = 100
    for j in range(i+1, len(paths)):
        aniCall = subprocess.check_output([aniPath, '-q', '-1', paths[i], '-2', paths[j],])
        aniScores = aniCall.rstrip().split()
        aniMatrix[i][j] = aniScores[24]
        aniMatrix[j][i] = aniScores[24]

#print "The ANI calculations took: "+`default_timer() - start`
# Print in tab-delimited format, the results from all vs. all average nucleotide comparison.
print " "+",",
for i in range(len(paths)):
    base_query = os.path.basename(paths[i])
    filename_query = os.path.splitext(base_query)[0]
    print `filename_query`+",",

print "\n",

for i in range(len(paths)):
    base_subject = os.path.basename(paths[i])
    filename_subject = os.path.splitext(base_subject)[0]
    print `filename_subject`+",",
    for j in range(len(paths)):
        print `aniMatrix[i][j]`+",",
    print "\n",