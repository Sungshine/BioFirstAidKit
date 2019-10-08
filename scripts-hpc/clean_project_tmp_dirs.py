#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Remove external user (states) temp files with modified dates before a specified date.

    Usage:  python2.7 /path/to/rm_dirs.py -d /path/to/target_dir -c 2019-03-27
    Help:   python2.7 /path/to/rm_dirs.py -h 

"""


import os
import sys
import time
import shutil
import argparse

from datetime import datetime


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Clear external partner temp directories where modified dates before desired date.'
    )
    parser.add_argument(
        '-d', '--root-dir',
        dest='rootdir',
        required=True,
        help='Path to target directory: [ /data/ceroot/execute, /data/shared ]'
    )
    parser.add_argument(
        '-c', '--cutoff-date',
        dest='cutoff',
        required=True,
        help='Desired cutoff date: [ YYYY-MM-DD ]'
    )
    return parser.parse_args()


if __name__ == '__main__':
    
    # args object holds the arguments passed into the command line
    args = get_args()

    root_dir = args.rootdir # /data/shared
    cutoff_date = datetime.strptime('{} 00:00:00.00000'.format(args.cutoff), '%Y-%m-%d %H:%M:%S.%f')

    # store all subdirectories in rootdir into list object
    all_dirs = [os.path.join(root_dir, f) for f in next(os.walk(root_dir))[1]]
    print('Master List == {}'.format(len(all_dirs)))
    
    # remove static shared directories
    exclude = ['CDC_EDLB_Salm_v3', 'CDC_EDLB_Ecoli_v4']
    for dpath in all_dirs:
        if os.path.basename(dpath) in exclude:
            print('Excluding from master list: {}'.format(dpath))
            all_dirs.remove(dpath)
    print('Trimmed Master List == {}'.format(len(all_dirs)))

    for d in all_dirs:
        p = '{}/temp'.format(d)
        if not os.path.exists(p):
            print('{} directory !exist, moving on to next project'.format(p))
            continue
        else:
            dl = [os.path.join(p, f) for f in next(os.walk(p))[1]]
            rm_dirs = [dir for dir in dl if datetime.fromtimestamp(os.stat(dir).st_mtime) < cutoff_date]
            for dirpath in rm_dirs:
                try:
                    # TODO print the counts of temp files for each state-organism project!
                    print('{}\t{}'.format(dirpath, len(rm_dirs)))
                    # print('Removing: {}'.format(dirpath))
                    # shutil.rmtree(dirpath)
                except Exception as e:
                    print('Error removing {}'.format(dirpath))
                    print('{}'.format(e))
