__author__ = 'Sung Im'
#!usr/bin/env python
import os
import subprocess

# inputDirectory = "/home/sim/Projects/GA_assemblies/completeAssemblies"
inputDirectory = "/home/sim/Projects/vibrio/assemblies/"
folders = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[1]]

for folder in folders:
    try:
        filePath = folder + "/contigs.fasta"
        subprocess.call(["/opt/quast-2.3/quast.py", "-o", folder, filePath])
    except:
        pass