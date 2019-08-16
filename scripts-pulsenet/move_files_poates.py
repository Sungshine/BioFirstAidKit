#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


"""

"""


import os
import csv
import shutil
import argparse


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='.'
    )
    parser.add_argument(
        '-i', '--input-file',
        dest='infile',
        required=True,
        help='Path to input file.'
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()
    errors = []
    with open(args.infile, 'rU') as fh:
        r = csv.reader(fh, delimiter='\t')
        for row in r:
            source = '/{}/{}/{}/{}/{}/{}'.format(row[1], row[2], row[3], row[4], row[5], row[6])
            dest = '/mnt/CalculationEngineReads.test/notForProduction/Validation/kit_validation/{}/{}/{}'.format(row[11], row[10], row[9])

            print('COPYING {} to {}'.format(source, dest))
            try:
                shutil.copy(source, dest)
            except IOError as e:
                errors.append([source, dest, e])
                continue

    ef = '/mnt/CalculationEngineReads.test/notForProduction/Validation/kit_validation/error_files.txt'
    with open(ef, 'w') as oh:
        w = csv.writer(oh, delimiter='\t')
        for i in errors:
            w.writerow(i)



        #     one = False
        #     two = False
        #     if row[7] == 'Nextera DNA Flex':
        #         one = 'flex'
        #         if row[8] == '151':
        #             two = '300'
        #         elif row[8] == '251':
        #             two = '500'
        #     elif row[7] == 'Nextera XT':
        #         one = 'xt'
        #         if row[8] == '151':
        #             two = '300'
        #         elif row[8] == '251':
        #             two = '500'
        #     elif row[7] == 'MiniSeq':
        #         one = 'miniseq'
        #     elif row[7] == 'Nextera XT v2 Set A':
        #         one = 'xt'
        #         if row[8] == '151':
        #             two = '300'
        #         elif row[8] == '251':
        #             two = '500'
        #     l.append(row + ['{}{}'.format(one, two)])
        #
        # with open('/Users/sim/Downloads/POATES4.txt', 'w') as oh:
        #     w = csv.writer(oh, delimiter='\t')
        #     for i in l:
        #         w.writerow(i)



