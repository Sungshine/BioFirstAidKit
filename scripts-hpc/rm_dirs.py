#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Remove directories with modified dates before a specified date.

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
        description='Remove directories where modified dates before desired date.'
    )
    parser.add_argument(
        '-d', '--root-dir',
        dest='rootdir',
        required=True,
        help='Path to target directory: [ /data/ceroot/execute, /data/shared/CDC_EDLB_RefId_v1/temp ]'
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

    rootdir = args.rootdir
    cutoff_date = datetime.strptime('{} 00:00:00.00000'.format(args.cutoff), '%Y-%m-%d %H:%M:%S.%f')

    # store all subdirectories in rootdir into list object
    all_dirs = [os.path.join(args.rootdir, f) for f in next(os.walk(args.rootdir))[1]]
    
    # store subdirectories before cut-off date into list object
    rm_dirs = [dir for dir in all_dirs if datetime.fromtimestamp(os.stat(dir).st_mtime) < cutoff_date]

    print('=(^.^)=')
    print('Searching inside: {}'.format(args.rootdir))
    print('Found: {}/{} directories with modified dates earlier than: {}'.format(len(rm_dirs), len(all_dirs), args.cutoff))
    
    # Ask user to confirm delete operation
    confirm = raw_input('Are you sure you want to remove {} directories? [Y/N] :'.format(len(rm_dirs)))

    if confirm == 'N' or confirm == 'n':
        print('User aborted. Bye meow.')
        exit()

    if confirm == 'Y' or confirm == 'y':
        print('Proceed to remove {} directories'.format(len(rm_dirs)))

        for dirpath in rm_dirs:
            try:
                print('Removing:: {}'.format(dirpath))
                shutil.rmtree(dirpath)
            except Exception as e:
                print('Error removing {}'.format(dirpath))
                print('{}'.format(e))
