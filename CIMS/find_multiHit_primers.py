#!/usr/bin/python3

""" Find the primer sets that amplify multiple targets.

Input:  emboss_dir = directory containing results from EMBOSS primersearch
        labels_dir = directory containing taxa translations from kraken-translate
        unclass_dir = directory containing the unclassified contigs from kraken

Output: > Reference assembly <
        - Primer Set -
        Hit information
"""


import os
import sys
from Bio.Emboss.PrimerSearch import OutputRecord, Amplifier, read


__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


if __name__ == "__main__":

    # TODO the input for the directory paths should be command line arguments
    # Paths to files
    emboss_dir = '/mnt/scicomp-groups/OID/NCEZID/DFWED/EDLB/share/projects/CIMS/Salmonella/PrimerSpecificity/embossResults/'  # sys.argv[1]
    labels_dir = '/mnt/scicomp-groups/OID/NCEZID/DFWED/EDLB/share/projects/CIMS/Salmonella/PrimerSpecificity/krakenResults/translations/'  # sys.argv[2]
    unclass_dir = '/mnt/scicomp-groups/OID/NCEZID/DFWED/EDLB/share/projects/CIMS/Salmonella/PrimerSpecificity/krakenResults/unclassified/'  # sys.argv[3]

    emboss_paths = [os.path.join(emboss_dir, fn) for fn in next(os.walk(emboss_dir))[2]]
    labels_paths = [os.path.join(labels_dir, fn) for fn in next(os.walk(labels_dir))[2]]
    unclass_paths = [os.path.join(unclass_dir, fn) for fn in next(os.walk(unclass_dir))[2]]

    # Let's parse the Emboss primer search outputs
    for file in emboss_paths:

        filename = os.path.basename(file)

        # Print the primers that hit more than one target and the hit info for those amplicons
        print('\n')
        print('>>>>>>>>>>>>_____{}_____<<<<<<<<<<<<'.format(filename))
        with open(file, 'r') as handle:

            record = read(handle)

            for name in record.amplifiers:

                if len(record.amplifiers[name]) > 1:
                    print('-----{}-----'.format(name))
                    for amplifier in record.amplifiers[name]:
                        print(amplifier.length)
                        print(amplifier.hit_info)
                        print('\n')