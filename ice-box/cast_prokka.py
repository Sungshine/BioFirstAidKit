#!/usr/bin/env python2.7

""" Cast prokka genome annotation program on list of genomes.

Working example of how to invoke system modules within a Python script.

"""


import os
import subprocess


__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.2'


# Load environment modules.
execfile('/usr/share/Modules/init/python.py')
module('load', 'prokka')
module('unload', 'tbl2asn/22.4')
module('load', 'tbl2asn/25')
module('unload', 'hmmer/2.3.2')
module('load', 'hmmer/3.1b1')
module('load', 'hmmer/3.1b1')
module('list')


# global variables
input_dir = '/scicomp/groups/OID/NCEZID/DFWED/EDLB/share/out/Calculation_Engine/STEC/PacBio'
out_dir = '/scicomp/groups/OID/NCEZID/DFWED/EDLB/share/projects/CIMS/Escherichia/prokka/tmp/'
paths = [os.path.join(input_dir, fn) for fn in next(os.walk(input_dir))[2]]

for filepath in paths:
    if '.fsa' or '.fasta' or '.fna' in os.path.basename(filepath):
        print('Now processing {}.'.format(os.path.basename(filepath)))
        filename = os.path.basename(filepath)
        subprocess.call(['prokka',
                         '-outdir', out_dir + filename + '.prokka',
                         '--prefix', filename,
                         '--force',
                         '--cpus', '10',
                         '--compliant',
                         filepath,
                         ])

print('Job complete. Purging modules.')
module('purge')