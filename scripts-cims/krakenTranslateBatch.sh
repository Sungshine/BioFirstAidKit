#!/bin/sh

## Usage: run this script directly passing it your target directory
## as the first argument, and it will iterate over the files in the
## target folder and pass them as a parameter to krakenTranslate.sh

for file in $1/*.sequence.kraken
do qsub -M $2 /scicomp/home/wla9/Projects/CIMS/scripts/krakenTranslate.sh "$file"
done