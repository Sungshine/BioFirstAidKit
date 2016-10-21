#!/bin/bash

for file in $1/*
do qsub -M $2 /scicomp/home/wla9/krakenSingle.sh "$file"
done
