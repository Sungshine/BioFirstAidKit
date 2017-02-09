#!/usr/bin/env python2.7

""" Parse multifasta file into header specific mulitfasta files.

Last file created will be missing a newline.
Suggest that you open the file and add a newline to end of file.
"""


import argparse


__author__ = 'Sung Im'
__email__ = 'sungbin401@gmail.com'


if __name__ == '__main__':


    # Command line arguments.
    opt_parse = argparse.ArgumentParser(description='Split multifasta file into header specific multifasta files.')
    opt_parse.add_argument('-i', '--input-file', dest='infile', required=True, help='Path to file.')
    opt_parse.add_argument('-o', '--outdir', dest='outdir', required=True, help='Path to output directory.')
    args = opt_parse.parse_args()


    with open(args.infile, 'rb') as infsa:

        filename = False

        for line in infsa.readlines():
            if not filename:
                if line.startswith('>'):
                    filename = line.split(':')[0].lstrip('>')
                    outfile = '{}/{}.fa'.format(args.outdir, filename)
                    out = open(outfile, 'wa')
                    out.write(line)
                else:
                    if line != '':
                        out.write(line)
                    else:
                        continue
            else:
                if line.startswith('>'):
                    if filename == line.split(':')[0].lstrip('>'):
                        out.write(line)
                    else:
                        out.close()
                        filename = line.split(':')[0].lstrip('>')
                        outfile = '{}/{}.fa'.format(args.outdir, filename)
                        out = open(outfile, 'wa')
                        out.write(line)
                        continue
                else:
                    if line != '':
                        out.write(line)
                    else:
                        continue
