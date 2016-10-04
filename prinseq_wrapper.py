__author__ = 'sim'

#!/usr/bin/python
#Prinseq

import os
import sys
import subprocess
from multiprocessing import Pool;
#inputDirectory = "/home/sungshine/prinseq";
paths = [os.path.join(inputDirectory,fn) for fn in next(os.walk(inputDirectory))[2]]
# print("processing these files: ");
# print(paths);

def call_wrapper(command, stdIn=None, stdOut=None, stdErr=None):
    print("calling: ");
    print(command);
    subprocess.call(command,stdin=stdIn, stdout=stdOut, stderr=stdErr);

with Pool(processes=8) as pool:         # start 4 worker processes

    for file in paths:

        #fileStdOut = file+".trimmed";
        pool.apply_async(call_wrapper, args=(("prinseq-lite","-verbose","-fastq",file,"-out_format","3",),)) ;

    pool.close();
    pool.join();

    print("finished processing!")