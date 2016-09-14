__author__ = 'Sung Im'
import sys

inputFile = sys.argv[1]

fastq = open(inputFile, "r")
line = fastq.readline()

while line != "":
    if line.startswith("@"):


# with open(inputFile, "r") as f:
#     line = f.readline()
#     while line != "":


# def find_kmers(string, k):
#     kmers = []
#     n = len(string)
#     for i in range(0, n-k+1):
#         kmers.append(string[i:i+k])
#     return kmers
#
# find_kmers(inputFile, 11)