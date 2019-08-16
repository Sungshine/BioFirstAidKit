#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Print list of states that have recently been added.

"""


import os
import sys
import argparse


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Remove directories where modified dates before desired date.'
    )
    parser.add_argument(
        '-d', '--root-dir',
        dest='rootdir',
        required=True,
        help='Path to target directory: [ /data/ceroot/execute, /data/shared/CDC_EDLB_RefId_v1/temp ]'
    )
    return parser.parse_args()


if __name__ == '__main__':

    # args object holds the arguments passed into the command line
    args = get_args()

    current_states = ['CDC', 'Genotyping', 'ANI', 'searchdata', 'Contamination', 'CO', 'CT', 'DE', 'FL', 'KS', 'KY', 'MA', 'MD', 'MI', 'MN', 'NY', 'NYC', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'UT', 'VA', 'WA', 'WY']

    dirs = [os.path.join(args.rootdir, f) for f in next(os.walk(args.rootdir))[1]]

    big_d = {}

    for d in dirs:
        dname = os.path.basename(d)
        state = dname.split('_')[0]
        count = 1
        if state not in big_d.keys():
            big_d[state] = count
        else:
            big_d[state] += 1

    new_states = []
    for st in big_d.keys():
        if st not in current_states:
            new_states.append(st)
    
    print(new_states)



