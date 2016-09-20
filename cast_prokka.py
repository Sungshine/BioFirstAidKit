#!/usr/bin/env python2.7

""" Cast prokka genome annotation program on list of genomes.

"""

import os
import subprocess

__author__  = "Sung Im"
__email__   = "wla9@cdc.gov"

# Load necessary modules.

subprocess.open(["modulecmd", ""])


# input_dir = "/scicomp/groups/OID/NCEZID/DFWED/EDLB/share/out/Calculation_Engine/STEC/PacBio"
#
# paths = [os.path.join(input_dir, fn) for fn in next(os.walk(input_dir))[2]]
#
# for path in paths:
#     if ".fsa" or ".fasta" or ".fna" in os.path.basename(path):
#         # print os.path.basename(path)
#         filename = os.path.basename(path)
#         subprocess.call(["prokka",
#                          "-outdir", filename+".prokka",
#                          "--prefix", filename,
#                          "--force",
#                          "--cpus", "10",
#                          "--compliant"])