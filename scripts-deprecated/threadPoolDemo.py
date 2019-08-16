#!/usr/bin/python

""" Example of running multiple processes.

https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool
"""


import sys
import time
import random
import subprocess
from multiprocessing import Pool


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.2'


def call_wrapper(command, stdIn=None, stdOut=None, stdErr=None):
    print('calling: ')
    print(command)
    subprocess.call(command, stdin=stdIn, stdout=stdOut, stderr=stdErr)

print('running theading demo...')

with Pool(processes=8) as pool:         # start 4 worker processes

    for x in range(0,5):
        #fileStdIn  = open('qwerty' + str(x) + '.in', 'w+')
        #fileStdErr = open('qwerty' + str(x) + '.err', 'w+')
        #fileStdOut = open('qwerty' + str(x) + '.out', 'w+')
        pool.apply_async(call_wrapper, args=(('ls', '-lha',),))

    pool.close()
    pool.join()

    print('finished processing!')
