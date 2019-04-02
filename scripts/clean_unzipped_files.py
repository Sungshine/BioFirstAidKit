# Remove unzipped fastq files on sneakernet shares

# edlb-sneakernet:/mnt/CalculationEngineReads.test/Salm$ ls *.fastq | wc -l == 217
# edlb-sneakernet:/mnt/CalculationEngineReads.test/STEC$ ls *.fastq | wc -l == 1198
# edlb-sneakernet:/mnt/CalculationEngineReads.test/LMO$ ls *.fastq | wc -l == 4
# edlb-sneakernet:/mnt/CalculationEngineReads.test/Campy$ ls *.fastq | wc -l == 4

# Store list of unzipped files for each organism
# Calculate the amount of diskspace the unzipped files are taking up

# Check that the zipped version of the file exists

# If the zipped copy exists, remove the unzipped file

# Log it
