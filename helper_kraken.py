#!/usr/bin/python3

""" Descriptive Text Goes Here

"""

# import statements go here

__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"

# kraken --db standard_db/ /scicomp/groups/OID/NCEZID/DFWED/EDLB/share/projects/metagenomics/COAL/assembly/2013RAN-169-M947-14-049-Loopy_contigs4.fasta --threads 16 --fasta-input > 2013RAN-169-M947-14-049-Loopy_contigs4.sequence.kraken
# kraken-translate --db standard_db/ 2013RAN-169-M947-14-049-Loopy_contigs4.sequence.kraken > 2013RAN-169-M947-14-049-Loopy_contigs4.sequence.labels
# TODO add flags --unclassified-out FILENAME and --classified-out FILENAME

# 1826 sequences (5.84 Mbp) processed in 0.598s (183.3 Kseq/m, 585.82 Mbp/m).
#  1665 sequences classified (91.18%)
#  161 sequences unclassified (8.82%)

# 683 | 1826 sequences are classified as Salmonella
