#!/bin/bash
## Embedded Grid Engine commands ##
## Designate correct shell
#$ -S /bin/sh

# The -N option sets the name of the job. This will show up in 'qstat'
#$ -N kraken_sungshine

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
KRAKEN_DB=$HOME/Projects/CIMS/salmonella/kraken/standard_db
KRAKEN_OUT=$HOME/Projects/CIMS/salmonella/kraken/results
#READS = $@;

module load kraken/0.10.5

kraken --fasta-input --threads=16 --db=$KRAKEN_DB --output=$KRAKEN_OUT/$(basename $1).sequence.kraken "$1"

module unload kraken/0.10.5
