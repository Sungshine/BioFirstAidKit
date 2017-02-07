#!/usr/bin/env python2.7

""" Merge each result file into one csv.

"""


import os
import csv
import errno
import argparse
import operator
import subprocess


__author__ = 'Sung Im'
__email__ = 'sungbin401@gmail.com'


if __name__ == '__main__':


    # Command line arguments.
    opt_parse = argparse.ArgumentParser(description='Launch STing Utilities on a directory of reads.')
    opt_parse.add_argument('-i', '--input-directory', dest='indir', required=True, help='Path to results directory.')
    # opt_parse.add_argument('-o', '--outdir', dest='outdir', required=True, help='Path to output directory.')
    args = opt_parse.parse_args()

    result_paths = [os.path.join(args.indir, fn) for fn in next(os.walk(args.indir))[2]]

    final_out = '/Users/sim/Projects/stx/tmp/final.csv'

    tuplist = []

    with open(final_out, 'wa') as final_result:
        writer = csv.writer(final_result, delimiter=',')
        for result_file in result_paths:
            tmplist = []
            with open(result_file, 'r') as csvin:
                reader = csv.reader(csvin, delimiter=',')
                for row in reader:
                    tmplist.append(str(row[0]))

                for i in tmplist:
                    print(format(i))
                # print(tmplist[:-3])
                # print(len(tmplist))
                # print(len(tmplist[:-3]))
                # print(tmplist[:-1])
                # tophit = max(tmplist[:-1])
                # print(os.path.basename(result_file), tophit)
                # topindex = [i for i, j in enumerate(tmplist) if j == tophit]
                # print(os.path.basename(result_file), tophit, topindex)

                # index, value = max(enumerate(tmplist[:-3]), key=operator.itemgetter(1))
                # print(index, value)

                tuplist.append(tmplist)

