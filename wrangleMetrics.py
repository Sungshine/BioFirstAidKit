__author__ = 'Sung Im'
#!/usr/bin/env python
import os
import csv

inputDirectory = "/home/sim/Projects/GA_assemblies/completeAssemblies"
folders = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[1]]

def file2dict(resultFile, filename):
    with open(resultFile, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        resultData = list(reader)

        for item in resultData:
            sauceList.append(item[1])

        noContigs = sauceList[5]
        largestContig = sauceList[6]
        totalLength = sauceList[7]
        gc = sauceList[8]
        nFifty = sauceList[9]
    f.close()

    # open the output csv file handle
    with open("/home/sim/Projects/GA_assemblies/QuastLog.csv", "a") as csvout:
        fieldnames = ["strainID", "#contigs", "largestContig", "totalLength", "GC%", "N50"]
        writer = csv.DictWriter(csvout, fieldnames = fieldnames)
        # writer.writeheader()
        writer.writerow({"strainID": filename,
                         "#contigs": noContigs,
                         "largestContig": largestContig,
                         "totalLength": totalLength,
                         "GC%": gc,
                         "N50": nFifty})
        del sauceList[:]
    csvout.close()

sauceList = []

for f in next(os.walk(inputDirectory))[1]:
    try:
        base = os.path.basename(f)
        filename = os.path.splitext(base)[0]
        filePath = os.path.join(inputDirectory, f) + "/report.tsv"
        file2dict(filePath, filename)
    except:
        pass