__author__ = 'Sung Im'
#!/usr/bin/env python
import os
import shutil
# from collections import Counter

# Copy a list of files to target directory
isolates = open("/home/sim/Downloads/170_ANIb.txt", "r")

inputDirectory = "/mnt/monolith0ECOLI/2014-11-24_ecoli_cgp_annotations/cgp.gbk/"
paths = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[2]]

destinationDir = "/home/sim/Projects/ANI/aniBlastData/"
# arr = []
# existing = []

for line in isolates:

    identifier = line.rstrip()
    # arr.append(identifier)

    for file in paths:

        base = os.path.basename(file)
        filename = os.path.splitext(base)[0]
        next = os.path.splitext(filename)[0]

        if identifier == next:

            # existing.append(identifier)
            shutil.copy(file, destinationDir)

# found = Counter(arr)
# expected = Counter(existing)
# print list((found - expected).elements())