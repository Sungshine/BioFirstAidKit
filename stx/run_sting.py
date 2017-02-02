#!/usr/bin/env python2.7

""" Execute STing detection with varying k-mer lengths.

Script should be executed from inside 'reads' directory.

"""


import os
import errno
import subprocess


__author__ = 'Sung Im'
__email__ = 'sungbin401@gmail.com'


def check_for_directory(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


# Stx1 positive genomes
stx1_list_r1 = 'SRR3232056_1.fastq.gz,SRR2014747_1.fastq.gz,SRR3290009_1.fastq.gz,SRR1570146_1.fastq.gz,SRR3189186_1.fastq.gz'
stx1_list_r2 = 'SRR3232056_2.fastq.gz,SRR2014747_2.fastq.gz,SRR3290009_2.fastq.gz,SRR1570146_2.fastq.gz,SRR3189186_2.fastq.gz'

stx2_list_r1 = 'SRR3290747_1.fastq.gz,SRR3290223_1.fastq.gz,SRR3180699_1.fastq.gz,SRR3178036_1.fastq.gz,SRR3232056_1.fastq.gz'
stx2_list_r2 = 'SRR3290747_2.fastq.gz,SRR3290223_2.fastq.gz,SRR3180699_2.fastq.gz,SRR3178036_2.fastq.gz,SRR3232056_2.fastq.gz'

stx12_list_r1 = 'SRR1999961_1.fastq.gz,SRR3825870_1.fastq.gz,SRR3829545_1.fastq.gz,SRR1999798_1.fastq.gz,SRR1999264_1.fastq.gz'
stx12_list_r2 = 'SRR1999961_2.fastq.gz,SRR3825870_2.fastq.gz,SRR3829545_2.fastq.gz,SRR1999798_2.fastq.gz,SRR1999264_2.fastq.gz'

nostx_list_r1 = 'SRR2015135_1.fastq.gz,SRR1999107_1.fastq.gz,SRR1999886_1.fastq.gz,SRR1999108_1.fastq.gz,SRR1999983_1.fastq.gz'
nostx_list_r2 = 'SRR2015135_2.fastq.gz,SRR1999107_2.fastq.gz,SRR1999886_2.fastq.gz,SRR1999108_2.fastq.gz,SRR1999983_2.fastq.gz'

allstx_list_r1 = 'SRR1570146_1.fastq.gz,SRR1999107_1.fastq.gz,SRR1999108_1.fastq.gz,SRR1999264_1.fastq.gz,SRR1999798_1.fastq.gz,SRR1999886_1.fastq.gz,SRR1999961_1.fastq.gz,SRR1999983_1.fastq.gz,SRR2014747_1.fastq.gz,SRR2015135_1.fastq.gz,SRR3178036_1.fastq.gz,SRR3180699_1.fastq.gz,SRR3189186_1.fastq.gz,SRR3232006_1.fastq.gz,SRR3232056_1.fastq.gz,SRR3290009_1.fastq.gz,SRR3290223_1.fastq.gz,SRR3290747_1.fastq.gz,SRR3825870_1.fastq.gz,SRR3829545_1.fastq.gz'
allstx_list_r2 = 'SRR1570146_2.fastq.gz,SRR1999107_2.fastq.gz,SRR1999108_2.fastq.gz,SRR1999264_2.fastq.gz,SRR1999798_2.fastq.gz,SRR1999886_2.fastq.gz,SRR1999961_2.fastq.gz,SRR1999983_2.fastq.gz,SRR2014747_2.fastq.gz,SRR2015135_2.fastq.gz,SRR3178036_2.fastq.gz,SRR3180699_2.fastq.gz,SRR3189186_2.fastq.gz,SRR3232006_2.fastq.gz,SRR3232056_2.fastq.gz,SRR3290009_2.fastq.gz,SRR3290223_2.fastq.gz,SRR3290747_2.fastq.gz,SRR3825870_2.fastq.gz,SRR3829545_2.fastq.gz'

# Lists of lists
r1s = [stx1_list_r1, stx2_list_r1, stx12_list_r1, nostx_list_r1, allstx_list_r1]
r2s = [stx1_list_r2, stx2_list_r2, stx12_list_r2, nostx_list_r2, allstx_list_r2]

# Path to database
database = '/data/home/sim8/Projects/shigatoxin/database/stx'

for i in range(20, 51):
    kmer = str(i)

    # Create output-results directories.
    out_directory = '/data/home/sim8/Projects/shigatoxin/results/k{}_results'.format(kmer)
    check_for_directory(out_directory)

    # Result filename formatting.
    stx1_outfile = '{}/stx1_k{}_out.csv'.format(out_directory, kmer)
    stx2_outfile = '{}/stx2_k{}_out.csv'.format(out_directory, kmer)
    stx12_outfile = '{}/stx12_k{}_out.csv'.format(out_directory, kmer)
    nostx_outfile = '{}/nostx_k{}_out.csv'.format(out_directory, kmer)
    all_outfile = '{}/all_k{}_out.csv'.format(out_directory, kmer)

    # Execute detector tool.
    for r1, r2 in zip(r1s, r2s):
        r_ones = r1
        r_twos = r2

        if r1s.index(r_ones) == 0:
            outfile = open(stx1_outfile, 'w')
            subprocess.call(['detector', '-l', '-x', database, '-k', kmer, '-1', r_ones, '-2', r_twos], stdout=outfile)
            outfile.close()
        elif r1s.index(r_ones) == 1:
            outfile = open(stx2_outfile, 'w')
            subprocess.call(['detector', '-l', '-x', database, '-k', kmer, '-1', r_ones, '-2', r_twos], stdout=outfile)
            outfile.close()
        elif r1s.index(r_ones) == 2:
            outfile = open(stx12_outfile, 'w')
            subprocess.call(['detector', '-l', '-x', database, '-k', kmer, '-1', r_ones, '-2', r_twos], stdout=outfile)
            outfile.close()
        elif r1s.index(r_ones) == 3:
            outfile = open(nostx_outfile, 'w')
            subprocess.call(['detector', '-l', '-x', database, '-k', kmer, '-1', r_ones, '-2', r_twos], stdout=outfile)
            outfile.close()
        elif r1s.index(r_ones) == 4:
            outfile = open(all_outfile, 'w')
            subprocess.call(['detector', '-l', '-x', database, '-k', kmer, '-1', r_ones, '-2', r_twos], stdout=outfile)
            outfile.close()
