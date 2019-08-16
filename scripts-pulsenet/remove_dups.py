#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


""" Create histogram of files downloaded from PulseNet FTP and BaseSpace.

    Counts samples and bins them by month/year.

"""


# Makes matplotlib library work on monolith1
import matplotlib
matplotlib.use('Agg')

import sqlite3
import argparse
import calendar
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


def get_args():
    """ Get command line arguments. """
    parser = argparse.ArgumentParser(
        description='Search NCBI for SRA and BioProject accessions.'
    )
    parser.add_argument(
        '-d', '--database',
        dest='db',
        required=True,
        help='Path to SQLite database file.'
    )
    parser.add_argument(
        '-o', '--output-directory',
        dest='outdir',
        required=True,
        help='Path to desired output directory.'
    )
    return parser.parse_args()


def dict_factory(cursor, row):
    """ Create dictionary object of SQL query elements. """
    d = {}
    for index, column in enumerate(cursor.description):
        d[column[0]] = row[index]
    return d


def plot_samples(df, color, todays_date, total):
    """ Create historgram of total number of samples. """
    plt.figure(figsize=(25, 20))
    ax = (df.groupby([df.dt.year, df.dt.month]).count()/2).plot(kind='bar', color=color, ylim=(0, 5000))

    # X-tick labels
    new_labs = []
    for i in ax.get_xticklabels():
        year = str(i).split("u'(")[1].split(', ')[0]
        month = str(i).split("u'(")[1].split(', ')[1].rstrip(")')")
        month_name = calendar.month_abbr[int(month)]
        new_labs.append('{}_{}'.format(year, month_name))
    ax.set_xticklabels(new_labs)

    # Bar height labels
    for p in ax.patches:
        ax.annotate(np.round(p.get_height(), decimals=0).astype(int),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 23),
                    textcoords='offset points', rotation=90)
    # X-axis label
    ax.set_xlabel('Date by Month/Year')
    # Y-axis label
    ax.set_ylabel('Sample Count')
    # Bar chart title
    ax.set_title('Total Samples Download from BaseSpace & PulseNet FTP (Total Samples = {})'.format(total))

    # Save figure
    plt.savefig('{}/{}test.bymonth.png'.format(args.outdir, todays_date), dpi=300)


if __name__ == '__main__':

    args = get_args()

    todays_date = datetime.today().isoformat(sep='T').split('T')[0]

    # Globals
    myD = {}
    ids = []
    ids2 = []

    # Query Files table and store unique entries & most recent submission date into dictionary
    conn = sqlite3.connect(args.db)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select Name, dateCreated from Files where date(dateCreated) >= date('2018-05-25')")
    # c.execute("select Name, dateCreated from Files")

    for i in c.fetchall():
        id = i['Name']
        date = i['DateCreated'].split('T')[0]
        if id not in myD.keys():
            myD[id] = date
        else:
            if datetime.strptime(myD[id], '%Y-%m-%d') < datetime.strptime(date, '%Y-%m-%d'):
                myD[id] = date
            else:
                continue
        ids.append(id)

    # Query ftpFiles table and add to dictionary of non-duplicate files
    c.execute("select Name, Date from ftpFiles where date(date) >= date('2018-05-25')")
    # c.execute("select Name, Date from ftpFiles")

    for i in c.fetchall():
        id = i['Name']
        date = i['Date'].split('T')[0]
        if id not in myD.keys():
            myD[id] = date
        else:
            if datetime.strptime(myD[id], '%Y-%m-%d') < datetime.strptime(date, '%Y-%m-%d'):
                myD[id] = date
            else:
                continue
        ids2.append(id)

    sample_total = len(myD.keys())

    # Store dates from query into list, format to datetime objects
    data = myD.values()
    dates = [datetime.strptime(i, '%Y-%m-%d') for i in data]

    # Plot
    df = pd.Series(dates)
    cols = '#99ffcc' #'#d65861'
    plot_samples(df, cols, todays_date, sample_total)
