#!/usr/bin/env python2.7

""" Execute STing detection with varying k-mer lengths.

Script should be executed from inside 'reads' directory.
No other files should be in directory.

"""


import os
import csv
import errno
import argparse
import subprocess


__author__ = 'Sung Im'
__email__ = 'sungbin401@gmail.com'


def wranglePairedEnds(path):
    """ Match paired-end read files.

    """
    pair_hash = {}
    for file in path:
        newfile = ""
        if '_R1' in file:
            newfile = file.replace('_R1', '_R*')
        elif '_R2' in file:
            newfile = file.replace('_R2', '_R*')
        if newfile not in pair_hash:
            pair_hash[newfile] = [file]
        else:
            pair_hash[newfile].append(file)
    return pair_hash


def check_for_directory(path):
    """ Create output directory if it does not exist.

    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


if __name__ == '__main__':


    # Command line arguments.
    opt_parse = argparse.ArgumentParser(description='Launch STing Utilities on a directory of reads.')
    opt_parse.add_argument('-i', '--input-directory', dest='indir', required=True, help='Path to directory containing paired read files.')
    opt_parse.add_argument('-d', '--database', dest='db', required=True, help='Path to database + prefix.')
    opt_parse.add_argument('-o', '--outdir', dest='outdir', required=True, help='Path to results directory.')
    opt_parse.add_argument('-x', '--x-range', dest='x', required=True, help='Starting kmer size.')
    opt_parse.add_argument('-y', '--y-range', dest='y', required=True, help='Ending kmer size')
    args = opt_parse.parse_args()

    # Designate pointers to absolute paths.
    read_paths = [os.path.join(args.indir, fn) for fn in next(os.walk(args.indir))[2]]
    reads_hash = wranglePairedEnds(read_paths)

    # Path to database
    database = args.db

    for k in range(int(args.x), int(args.y)):
        kmer = str(k)
        out_directory = '{}/k{}_results'.format(args.outdir, kmer)
        check_for_directory(out_directory)

        # agg_results = '{}/k{}_aggresults.csv'.format(args.outdir, kmer)
        # agg_handle = open(agg_results, 'wa')
        # agg_writer = csv.writer(agg_handle, delimiter=',')
        # agg_writer.writerow('this is where the header will go.')

        for key in reads_hash:
            r1 = reads_hash.get(key)[0]
            r2 = reads_hash.get(key)[1]
            outname = os.path.basename(key).split('_')[0]

            outfile = '{}/{}.csv'.format(out_directory, outname)
            out_handle = open(outfile, 'w')

            print('###### Processing {}\n'.format(outname))

            ps = subprocess.Popen(('detector', '-l', '-x', database, '-k', kmer, '-1', r1, '-2', r2),
                                  stderr=subprocess.STDOUT,
                                  stdout=subprocess.PIPE,
                                  )

            # columns = ps.stderr
            # output = ps.communicate()[0]
            # captured_output = ps.stdout
            out, err = ps.communicate()

            out_handle.write(str(err))
            out_handle.write(str(out))
            out_handle.close()

            # for line in captured_output:
            #     agg_writer.writerow(line.strip())

            # writer = csv.writer(out_handle, delimiter=',')
            # write header
            # for line in columns:
            #     writer.writerow(line)

            # for line in repr(output):
            #     writer.writerow(line.strip())

            # writer.writerow(output)


        # agg_handle.close()


