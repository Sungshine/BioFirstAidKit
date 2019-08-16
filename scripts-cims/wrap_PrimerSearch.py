#!/usr/bin/python3

""" Wrapped BioPython.EMBOSS module to handle EMBOSS PrimerSearch.

"""


import os
import subprocess


__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


def primer_search(reference, primersets, outpath):
    """ Wrapper for EMBOSS primersearch program.

    """
    seqall = reference
    infile = primersets
    outfile = '{}/{}.emboss'.format(outpath, os.path.basename(reference))

    ps = subprocess.Popen(['primersearch',
                           '-seqall', seqall,
                           '-infile', infile,
                           '-mismatchpercent', '3',
                           '-outfile', outfile
                           ],
                          )
    return ps


if __name__ == "__main__":

    # variable file paths
    reference = '/home/sim/Projects/CIMS/salmonella/2013RAN-169-M947-14-049-Loopy_contigs4.fasta'
    primersets = '/home/sim/Projects/CIMS/salmonella/summary.table.format'
    emboss_out_path = '/home/sim/Projects/CIMS/salmonella/embossResults/'

    primersearch = primer_search(reference, primersets, emboss_out_path)