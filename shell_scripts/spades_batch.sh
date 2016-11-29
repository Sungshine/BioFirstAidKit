#!/bin/sh

## Usage: run this script directly passing it your target directory
## as the first argument, and it will iterate over the files in the
## target folder and pass them as a parameter to spades_single.sh

for file in $1/*.fastq.gz
do qsub -M $2 /scicomp/home/wla9/Projects/interGene/scripts/spades_single.sh "$file"
done