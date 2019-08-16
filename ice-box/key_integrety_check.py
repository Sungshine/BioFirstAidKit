#!/usr/bin/env python

""" Identify duplicate keys across the PN organism databases:
    E. coli O157, E. coli Non-O157, Shigella & S. flexneri

    Also checks for trailing white spaces.

    Usage: python key_integrity_check.py < csv.file > | cat > < out.file >
"""


import re
import sys
import csv


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'


infile = sys.argv[1]

e = []  # E. coli
n = []  # Non-O157
f = []  # S. flexneri
s = []  # Shigella

with open('/home/sim/Downloads/Ecoli.csv', 'rb') as efile:
    e_reader = csv.reader(efile, delimiter=',')
    for i in e_reader:
        e.append(i[0])
    efile.close()

with open('/home/sim/Downloads/NonO157.csv', 'rb') as nfile:
    n_reader = csv.reader(nfile, delimiter=',')
    for i2 in  n_reader:
        n.append(i2[0])
    nfile.close()

with open('/home/sim/Downloads/Sflexneri.csv', 'rb') as ffile:
    f_reader = csv.reader(ffile, delimiter=',')
    for i3 in f_reader:
        f.append(i3[0])
    ffile.close()

with open('/home/sim/Downloads/Shigella.csv', 'rb') as sfile:
    s_reader = csv.reader(sfile, delimiter=',')
    for i4 in s_reader:
        s.append(i4[0])
    sfile.close()

# print('Ecoli.csv contains {} ids.'.format(len(e)))
# print('NonO157.csv contains {} ids.'.format(len(n)))
# print('Sflexneri.csv contains {} ids.'.format(len(f)))
# print('Shigella.csv contains {} ids.'.format(len(s)))
# print('Now comparing all the things and building your master hash! This may take a while...')

masterdict = dict()

# Open the master list and compare
with open(infile, 'rb') as master:
    master_reader = csv.reader(master, delimiter=',')

    # Checking for ids with trailing white space.
    # for i in reader:
    #     id = i[0]
    #     if re.match(r'.+\s+\Z', id):
    #         print(id)

    for id in master_reader:
        fmtid = id[0]
        if fmtid in e:
            if fmtid in masterdict:
                masterdict[fmtid].append('e')
            else:
                masterdict[fmtid] = ['e']
        if fmtid in n:
            if fmtid in masterdict:
                masterdict[fmtid].append('n')
            else:
                masterdict[fmtid] = ['n']
        if fmtid in f:
            if fmtid in masterdict:
                masterdict[fmtid].append('f')
            else:
                masterdict[fmtid] = ['f']
        if fmtid in s:
            if fmtid in masterdict:
                masterdict[fmtid].append('s')
            else:
                masterdict[fmtid] = ['s']

    master.close()

for key, value in masterdict.items():
    print('{} | {}'.format(key, value))