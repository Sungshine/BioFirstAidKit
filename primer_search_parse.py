#!/usr/bin/python3

from Bio.Emboss.PrimerSearch import InputRecord, OutputRecord, Amplifier, read

# handle = open("/Users/sungshine/Downloads/2012K-1420_LargeContigs.fna.primersearch", "r")
handle = open("/home/sim/Projects/CIMS/salmonella/2012K-1420_LargeContigs.fna.primersearch", "r")  # pulsestar3

hit_dict = read(handle)

for name in hit_dict.amplifiers:
    for amplifier in hit_dict.amplifiers[name]:
        print(name, "\n", amplifier.hit_info, "\n", amplifier.length, "\n")