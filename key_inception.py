#!/usr/bin/env python

""" Identify substring matches within PulseNet keys
    Given a concatenated list of all keys across:
    E. coli O157, E. coli Non-O157, Shigella & S. flexneri

    Trims off the State Id prefix and searches the remaining key id
    across all keys and hashes all possible partial key matches.

    Usage: python key_inception.py < csv.file > | cat > < out.file >
"""

import re
import sys
import csv
import timeit

start = timeit.timeit()

infile = sys.argv[1]

e = []  # E. coli
n = []  # Non-O157
f = []  # S. flexneri
s = []  # Shigella

with open("/home/sim/Downloads/Ecoli.csv", "rb") as efile:
    e_reader = csv.reader(efile, delimiter=",")
    for i in e_reader:
        e.append(i[0])
    efile.close()

with open("/home/sim/Downloads/NonO157.csv", "rb") as nfile:
    n_reader = csv.reader(nfile, delimiter=",")
    for i2 in  n_reader:
        n.append(i2[0])
    nfile.close()

with open("/home/sim/Downloads/Sflexneri.csv", "rb") as ffile:
    f_reader = csv.reader(ffile, delimiter=",")
    for i3 in f_reader:
        f.append(i3[0])
    ffile.close()

with open("/home/sim/Downloads/Shigella.csv", "rb") as sfile:
    s_reader = csv.reader(sfile, delimiter=",")
    for i4 in s_reader:
        s.append(i4[0])
    sfile.close()


## string-ify the key ids removing the prefix possibilities
str_master = []

with open(infile, "rb") as master:
    master_reader = csv.reader(master, delimiter=",")

    for id in master_reader:
        fmtid = id[0]
        if fmtid.startswith("DBS__"):
            str_master.append(fmtid[10:])
        elif fmtid.startswith("DBS_"):
            str_master.append(fmtid[9:])
        elif fmtid.startswith("_", 4):
            str_master.append(fmtid[5:])
        elif fmtid.startswith("_", 3):
            str_master.append(fmtid[4:])
        else:
            if re.match("^[a-zA-Z0-9]", fmtid):
                str_master.append(fmtid)

# make str_master unique
str_master2 = set(str_master)

# trim str_master with anything less than 6
for i in str_master2.copy():
    if len(i) < 7:
        str_master2.remove(i)

mydict = dict()

for txt in str_master2:
    for id in e:
        if txt in id:
            # print("{} in {}".format(txt, id))
            if txt in mydict:
                mydict[txt].append(id)
            else:
                mydict[txt] = [id]
    for id in n:
        if txt in id:
            if txt in mydict:
                mydict[txt].append(id)
            else:
                mydict[txt] = [id]
    for id in f:
        if txt in id:
            if txt in mydict:
                mydict[txt].append(id)
            else:
                mydict[txt] = [id]
    for id in s:
        if txt in id:
            if txt in mydict:
                mydict[txt].append(id)
            else:
                mydict[txt] = [id]

mytrimdict = dict((k, v) for k, v in mydict.items() if len(v) > 1)

for key, value in mytrimdict.items():
    print("{} | {}".format(key, value))

print("First dict length = {}".format(len(mydict)))
print("Trimmed dict length = {}".format(len(mytrimdict)))

end = timeit.timeit()
print("####TIME TO PROCESS = {}".format(end - start))