""" Copy-paste entry lines from http://aspv-plsn-ce3.cdc.gov:54321/ into text file.
    Remove header line and save.
    Run script and pipe to new file to safe in tab-delimited format.

"""

import csv

f = '/Users/sim/Desktop/new-10.txt'
with open(f, 'r') as fh:
    # r = fh.readlines()
    lines = (line.rstrip() for line in fh)
    lines = (line for line in lines if line)
    
    g = []
    for l in lines:
        g.append(l)

    even = []
    odd = []
    for i, j in enumerate(g):
        if i % 2 == 0:
            even.append(j)
        else:
            odd.append(j)

    final = []
    for i, j in enumerate(even):
        full = '\t'.join([j, odd[i]])
        final.append(full)

    for i in final:
        # print(i.strip().split('\t'))
        h = i.strip().split('\t')
        newline = '\t'.join(h)
        print(newline)

    # print(len(g))
    # print(len(even))
    # print(len(odd))
    
    

