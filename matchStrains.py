#!/usr/bin/env python

""" Strain id matching script from ANI research.

Find which assemblies are missing from an original list for a Genome Announcement.
"""


import csv


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.2'


file1 = '/home/sim/Projects/GA_assemblies/strainlists/BCW_edit.csv'
file2 = '/home/sim/Projects/GA_assemblies/strainlists/RL_updated_2015_100K_Ecoli_strains.csv'

with open(file1, 'rb') as f, open(file2, 'rb') as g:
    reader1 = csv.reader(f, delimiter=',')
    reader2 = csv.reader(g, delimiter=',')
    list1 = list(reader1)
    list2 = list(reader2)
    myList = []
    rebeccaList = []
    rebeccaHash = {}

    # Generate the strainID lists
    # The hashmap is generated using rebeccaList
    for h in list1:
        myList.append(h[0])
    for n in list2:
        rebeccaList.append(n[1])
    for b in list2:
        bcwID = b[1]
        strainID = b[5]
        standard = b[9]
        if not bcwID in rebeccaHash:
            rebeccaHash[bcwID] = [strainID, standard]

    # Generate the list of strains that I do not have assemblies for
    for y in rebeccaHash:
        oID = rebeccaHash[y][0]
        standardID = rebeccaHash[y][1]
        if y not in myList:
            print(',' + y + ',' + oID + ',' + standardID + ',')

    # Generate the list of strains that I have an assembly for but is not included on Rebecca's list
    for k in myList:
        if k not in rebeccaList:
            print(k + ',' + ',')

    # Generate the list of strains that I have assembled and link it to a strainID from Rebecca's list
    for i in list1:
        for j in list2:
            if i[0] == j[1]:
                print(i[0] + ',', j[1] + ',', j[4] + ',' + j[9] + ',')