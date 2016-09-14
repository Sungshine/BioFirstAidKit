__author__ = 'Sung Im'
import os
import csv
import shutil

file = "/home/sim/PycharmProjects/genomics/OH_MasterList.csv"
outdir = "/home/sim/Projects/GA_assemblies/new/"

with open(file, "rb") as f:
    reader = csv.reader(f, delimiter=',')
    arr = list(reader)

    for item in arr:
        bcwID = item[0]
        x = "/home/sim/Projects/GA_assemblies/"+bcwID+".spades"
        # x = "/home/sim/Projects/gaTest/"+bcwID+".spades"

        if os.path.exists(x) == True:
            # print x
            shutil.move(x, outdir)