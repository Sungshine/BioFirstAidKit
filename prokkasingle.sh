#!/bin/sh

## Embedded Grid Engine commands ##

## Designate correct shell
#$ -S /bin/sh

# The -N option sets the name of the job. This will show up in 'qstat'
#$ -N Prokka_Sungshine

# This sets the default directory that the script will use as its home dir
# the CWD standards for "current working diretory"
#$ -cwd

# Specifies the q
#$ -q all.q

# Send an email when the job completes
#$ -m e
##################################################################
## Now we do work ...
## From Jo's old cluster account - necessary to run.
source /etc/profile.d/modules.sh

module load prokka/1.8
module unload tbl2asn/22.4
module load tbl2asn/25
module unload hmmer/2.3.2
module load hmmer/3.1b1

prokka "$1" --outdir "$(basename $1)" --prefix "$(basename $1)"

module unload prokka/1.8
module unload tbl2asn/25
module unload hmmer/3.1b1
