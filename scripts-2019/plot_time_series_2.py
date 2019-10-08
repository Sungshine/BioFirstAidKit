#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


""" Create histogram of submission to start times on the CE.

"""


import csv
import time
import datetime
import calendar
import argparse

import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Make time series of HPC accounting file'
    )
    parser.add_argument(
        '-i', '--input-file',
        dest='infile',
        required=True,
        help='Path to HPC accounting file'
    )
    parser.add_argument(
        '-o', '--output-dir',
        dest='outdir',
        required=True,
        help='Path to desired output dir'
    )
    return parser.parse_args()


def distill_input(f):
    """ Clean HPC acct file, return dict. """

    def map_job_name(jobname):
        jobname = str(jobname)
        if jobname.startswith('A_download_job_for_'):
            job_name = 'Downloader'
        elif jobname.startswith('Create_'):
            job_name = 'DbBackupProcess'
        elif jobname == 'Doing_a_denovo_assembly':
            job_name = 'Assembly'
        elif jobname.startswith('Doing_a_reference_mapping_against_'):
            job_name = 'RefMapper'
        elif jobname == 'Finding_alleles':
            job_name = 'AF_AlleleCaller'
        elif jobname == 'Performing_ANI-based_speciation':
            job_name = 'ANI'
        elif jobname == 'Performing_BLAST':
            job_name = 'AB_AlleleCaller'
        elif jobname == 'Performing_contamination_detection':
            job_name = 'Contamination'
        elif jobname == 'Performing_genotyping':
            job_name = 'Genotyper'
        elif jobname == 'Submitting_data_from_BaseSpace_to_NCBI':
            job_name = 'DataFetcher'
        elif jobname.startswith('Step'):
            job_name = 'InternalProcess'
        elif jobname == 'CheckInstall':
            job_name = 'InternalProcess'
        elif jobname == 'simple':
            job_name = 'InternalProcess'
        elif jobname.startswith('arrayjob'):
            job_name = 'InternalProcess'
        else:
            job_name = 'UnknownProcess'
        return job_name

    big_dict = {}
    with open(f, 'r') as fh:
        r = csv.reader(fh, delimiter='\t')
        next(r, None)
        for row in r:
            jobid = row[5]
            jobname = map_job_name(str(row[4]))
            subtime = datetime.datetime.fromtimestamp(int(row[8]))
            starttime = datetime.datetime.fromtimestamp(int(row[9]))
            endtime = datetime.datetime.fromtimestamp(int(row[10]))
            failed = int(row[11])
            exitstat = int(row[12])
            
            # Remove entries with failed exit status
            if failed != 0 or exitstat != 0:
                continue
            # Remove entries where submission-time > start-time
            elif subtime > starttime:
                continue
            # Remove duplicate jobids
            elif jobid in big_dict.keys():
                big_dict.pop(jobid)
                #print('Duplicate key found, removing both = {}'.format(jobid))
                continue
            else:
                big_dict[jobid] = [subtime, starttime, endtime, jobname]
                # big_dict[jobid] = {'sub': subtime, 'start': starttime, 'end': endtime, 'jobname': jobname}
    
    return big_dict


def grab_col_names(f):
    with open(f, 'r') as fh:
        r = csv.reader(fh, delimiter='\t')
        col_names = next(r, None)

    return col_names


def to_tuple(list):
    return (*list, )


def plot_sub_to_start(d, outdir, todays_date):
    ''' Plot time series of wait times after job sumbission '''
    job_times = []
    for k, v in d.items():
        sub = v[0]
        start = v[1]
        end = v[2]
        sub2start = start - sub
        job_times.append([sub, sub2start])

    sorted_job_times = sorted(job_times, key=lambda x: x[0])

    job_submit_times = []   # store submission-times only (datetime obj)
    times_to_start = []     # store sub2start-times only (timedelta obj)
    for i in sorted_job_times:
        job_submit_times.append(i[0])
        times_to_start.append(i[1])
    
    dates = mdates.date2num(job_submit_times)
    # Convert values (ns) to minutes
    in_minutes = []
    for t in times_to_start:
        a = np.timedelta64(t, 'ms')
        in_minutes.append(int(str(a.astype('timedelta64[m]')).split(' ')[0]))

    # Plot action
    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(70, 15))
    ax.plot(dates, in_minutes)
    
    myfmt = mdates.DateFormatter('%A (%m/%d)')
    ax.xaxis.set_major_formatter(myfmt)
    
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(np.arange(min(dates), max(dates), 1.0))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(4)

        # Add horizontal line
        plt.axhline(y=120, color='#1C6A5B', linestyle='--', linewidth=1)

    plt.savefig('{}/{}.sub2start.png'.format(outdir, todays_date))
    # plt.savefig('{}/{}.sub2start.png'.format(outdir, todays_date), dpi=500)


if __name__ == '__main__':

    args = get_args()
    outdir = args.outdir
    todays_date = datetime.datetime.today().isoformat(sep='T').split('T')[0]
    # f = '/Users/sim/Dropbox/EDLB/CalculationEngine/HPC/08-19-2019/accounting.txt'


    d = distill_input(args.infile)

    plot_sub_to_start(d, outdir, todays_date)