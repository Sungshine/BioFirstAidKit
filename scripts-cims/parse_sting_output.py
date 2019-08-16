#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Parse output from STing detector utility.
    Argument options include flags for parsing time, kmer count, kmer perc.

"""


import os
import csv
import argparse
import itertools


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Parses results from STing detector utility.'
    )
    parser.add_argument(
        '-i',
        '--input-file',
        dest='infile',
        required=False,
        help='Path to result file.'
    )
    parser.add_argument(
        '-d',
        '--input-directory',
        dest='indir',
        required=True,
        help='Path to directory containing result files.'
    )
    parser.add_argument(
        '-o',
        '--output-directory',
        dest='outdir',
        required=True,
        help='Path to desired output directory.'
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()

    results_out = os.path.join(args.outdir, 'amr_results_k30.txt')
    time_out = os.path.join(args.outdir, 'amr_time_results_k30.txt')

    fps = [os.path.join(args.indir, f) for f in next(os.walk(args.indir))[2]]

    results = {}
    timers = {}

    for fp in fps:
        with open(fp, 'rU') as input_file:
            reader = csv.reader(input_file, delimiter='\t')

            genes = False
            wall_time = False
            memory = False
            hits = False
            kmer_count = False
            kmer_percent = False

            for row in itertools.islice(reader, 0, 1):
                genes = row
            for row in itertools.islice(reader, 4, 5):
                wall_time = row
            for row in itertools.islice(reader, 4, 5):
                memory = row
            for row in itertools.islice(reader, 13, 14):
                hits = row
            for row in itertools.islice(reader, 0, 1):
                kmer_count = row
            for row in itertools.islice(reader, 0, 1):
                kmer_percent = row

            with open(time_out, 'a') as time_file:
                time_file.write('{}\t{}\t{}\n'.format(os.path.basename(fp), wall_time[1].strip(), memory[1].strip()))

            for gene in genes[:-1]:
                gene_name = gene.split(' ')[0].strip()
                hit = hits[genes.index(gene)]
                kmer_ct = kmer_count[genes.index(gene)]
                kmer_perc = kmer_percent[genes.index(gene)]

                if genes.index(gene) == len(genes[:-2]):
                    hit = hit.replace(',', '|')
                    kmer_ct = kmer_ct.replace(',', '|')
                    kmer_perc = kmer_perc.replace(',', '|')

                if gene_name not in results.keys():
                    results[gene_name] = [[hit, kmer_ct, kmer_perc]]
                else:
                    results[gene_name].append([hit, kmer_ct, kmer_perc])

    with open(results_out, 'wb') as result_file:
        writer = csv.writer(result_file, delimiter='\t')
        for key, values in results.iteritems():
            writer.writerow([key, values])
