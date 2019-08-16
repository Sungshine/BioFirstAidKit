#!/bin/bash
## Embedded Grid Engine commands ##
## Designate correct shell
#$ -S /bin/sh

# The -N option sets the name of the job. This will show up in 'qstat'
#$ -N spades_sungshine

# This sets the default directory that the script will use as its home dir
# the CWD standards for "current working diretory"
#$ -cwd

# Specifies the q
#$ -q all.q

# Send an email when the job completes
#$ -m e
##################################################################
source /etc/profile.d/modules.sh

# globals
SPADES_OUT=/scicomp/groups/OID/NCEZID/DFWED/EDLB/share/projects/Other_Analyses/Heidelberg/Pattern22/assemblies

module load SPAdes/3.9.0

# requires interleaved read pairs
spades.py --careful --12 "$1" -o $SPADES_OUT/$(basename $1).spades
