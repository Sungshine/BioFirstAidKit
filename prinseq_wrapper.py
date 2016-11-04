#!/usr/bin/python

""" Run PrinSeq program on multiple threads.

Example of using Python's multiprocess library.
"""


import os
import sys
import subprocess
from multiprocessing import Pool


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.2'


paths = [os.path.join(inputDirectory, fn) for fn in next(os.walk(inputDirectory))[2]]


def call_wrapper(command, stdIn=None, stdOut=None, stdErr=None):
    """ Helper script to call PrinSeq.

    """
    print("calling: ")
    print(command)
    subprocess.call(command, stdin=stdIn, stdout=stdOut, stderr=stdErr)

# start 4 worker processes
with Pool(processes=8) as pool:
    for file in paths:
        pool.apply_async(call_wrapper, args=(('prinseq-lite',
                                              '-verbose',
                                              '-fastq',
                                              file,
                                              '-out_format',
                                              '3',
                                              ),
                                             )
                         )
    pool.close()
    pool.join()
    print("finished processing!")