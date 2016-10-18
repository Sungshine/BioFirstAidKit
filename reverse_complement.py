#!/usr/bin/env python
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna


myseq = "agctgtgtgcacacaacatganggggcacacatgcacatgcacacatgcccacatgcata" \
        "tgcacacacacacacacacacacacacacattcatgcccaagcacgcccaccctcatgtc" \
        "tcaccatgtgcacataacacacagtcacatataccctggcacacatgcccacatgcagac" \
        "acgaaacacaggcccacgnttncatgcacacaggtatgggcacacataccatgcacacat" \
        "aangacaaataccaggccagacatgatttgcccctgctggtgtcactgttaagtgtgaca" \
        "gacaagcagaggacacacacccacctgggacgcggggcttcaggagagaggcagacctaa" \
        "tagggcccggattcggggctggggaggct"

mydna = Seq(myseq, generic_dna)
print(mydna.reverse_complement())

