#/usr/bin/env python3
# How many files does each lab have?
# {GA: {SALM: []}}


import shutil
import os
import csv


topdir = '/Users/sim/Projects/stateFTP'
salm_fsizes = []



bigD = dict()
root = [os.path.join(topdir, f) for f in next(os.walk(topdir))[1]]

for stateDir in root:
    # print('====== {}'.format(os.path.basename(stateDir)))
    stateId = os.path.basename(stateDir)
	
    stateDirs = [os.path.join(stateDir, f) for f in next(os.walk(stateDir))[1]]
    for bactDir in stateDirs:
        # print('==== {}'.format(os.path.basename(bactDir)))
        bactId = os.path.basename(bactDir)

        sampleDirs = [os.path.join(bactDir, f) for f in next(os.walk(bactDir))[1]]
        for sample in sampleDirs:
            # print('== {}'.format(os.path.basename(sample)))
            sampleId = os.path.basename(sample)
            
            totalSampleSize = 0

            files = [os.path.join(sample, f) for f in next(os.walk(sample))[2]]
            for zipFile in files:
                if os.path.basename(zipFile) != 'AnalysesAvailableLog.json':
                    # print('{}'.format(os.path.basename(zipFile)))
                    singleFile = os.path.basename(zipFile)                
                    newFileSize = int(os.stat(zipFile).st_size)
                    totalSampleSize += newFileSize
        
            if stateId not in bigD.keys():
                bigD[stateId] = {}
                if bactId not in bigD[stateId].keys():
                    bigD[stateId][bactId] = [totalSampleSize]
                else:
                    bigD[stateId][bactId].append(totalSampleSize)
            else:
                if bactId not in bigD[stateId].keys():
                    bigD[stateId][bactId] = [totalSampleSize]
                else:
                    bigD[stateId][bactId].append(totalSampleSize)

for k, v in bigD.items():
    # print(k, v)
    for bact in v:
        # print(bact, v[bact])
        print('{}\t{}\t{} B\t{} MB'.format(
            k, bact, sum(v[bact])/len(v[bact]), (sum(v[bact])/len(v[bact]))/1000000)
            )
