#!/bin/bash
## Embedded Grid Engine commands ##
## Designate correct shell
#$ -S /bin/sh

# The -N option sets the name of the job. This will show up in 'qstat'
#$ -N primersearch_sungshine

# This sets the default directory that the script will use as its home dir
# the CWD standards for "current working diretory"
#$ -cwd

# Specifies the q
#$ -q all.q

# Send an email when the job completes
#$ -m e
##################################################################
source /etc/profile.d/modules.sh

# global variables

EMBOSS_SUMMARY=/scicomp/groups/OID/NCEZID/DFWED/EDLB/share/projects/CIMS/Salmonella/PrimerSpecificity/summary.table.format
EMBOSS_OUT=/scicomp/groups/OID/NCEZID/DFWED/EDLB/share/projects/CIMS/Salmonella/PrimerSpecificity/embossResults

module load EMBOSS/6.5.7

primersearch -mismatchpercent=3 -seqall=$1 -infile=$EMBOSS_SUMMARY -outfile=$EMBOSS_OUT/$(basename $1).emboss

module unload EMBOSS/6.5.7

