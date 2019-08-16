#!/usr/bin/ env python2.7

""" """

import os
import csv

__author__  = "Sung Im"
__email__   = "wla9@cdc.gov"
__version__ = "0.1"


def wranglePairedEnds(paths):
    """ Match read mate pairs and return hash.

    """
    filehash = {}
    for file in paths:
        newfile = ""
        if "R1" in file:
            newfile = file.replace("R1", "R*")
        elif "R2" in file:
            newfile = file.replace("R2", "R*")
        if not newfile in filehash:
            filehash[newfile] = [file]
        else:
            filehash[newfile].append(file)
    return filehash


if __name__ == "__main__":

    inputDirectory = "/scicomp/home/wla9/Projects/ReadContamination/jelly_results/jelly_dumps_campy/"
    paths = [os.path.join(inputDirectory,fn) for fn in next(os.walk(inputDirectory))[2]]
    filehash = wranglePairedEnds(paths)

    in_common = []
    r1_mers = []
    r2_mers = []

    for key in filehash.keys():
        readpair = sorted(filehash.get(key))
        r1 = readpair[0]
        r2 = readpair[1]

        with open(r1, "rb") as readone:
            reader1 = csv.reader(readone, delimiter=",")
            for row in reader1:
                r1_mers.append(row[0])

        with open(r2, "rb") as readtwo:
            reader2 = csv.reader(readtwo, delimiter=",")
            for row2 in reader2:
                r2_mers.append(row2[0])

        intersect = set(r1_mers).intersection(r2_mers)
        print intersect
        a = float(len(intersect))
        b = float((len(r1_mers) + len(r2_mers)))

        percent_in_common = (a / b) * 100
        print("Percent in common = {}%".format(percent_in_common))

        # empty the lists before loading next read pair
        del r1_mers[:], r2_mers[:]



