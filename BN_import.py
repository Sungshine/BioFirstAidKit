__author__ = 'Sung Im'
import csv

bnState = "/home/sim/Downloads/BNimporting/nonExportFix.csv"
ninetySixPointOne = "/home/sim/Downloads/BNimporting/96.5.csv"
# oOneFiveSeven = "/home/sim/Downloads/BNimporting/o157updates.csv"

with open(bnState, "rb") as f, open(ninetySixPointOne, "rb") as g:
    reader1 = csv.reader(f, delimiter=",")
    reader2 = csv.reader(g, delimiter=",")
    list1 = list(reader1)
    list2 = list(reader2)
    cdcList = []
    cdcHash = {}
    for entry in list1:
        BN_key = entry[0]
        BNcdcID = entry[21]
        if "|" in BNcdcID:
            BNcdcID2 = BNcdcID.split("|")
            valueOne = BNcdcID2[0]
            valueTwo = BNcdcID2[1]

            # Append multiple values to a hash map -- not using DefaultDict()

            cdcHash[BN_key] = [valueOne]
            cdcHash[BN_key].append(valueTwo)
        else:
            cdcHash[BN_key] = [BNcdcID]

    for key, value in cdcHash.iteritems():
        for item in list2:
            if item == value:
                print key+","+value[0]+","+item[0]
