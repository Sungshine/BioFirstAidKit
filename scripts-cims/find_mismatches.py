#!/usr/bin/python3

""" Test the target specificity of a set of primer pairs.

Input:  emboss_dir = directory containing results from EMBOSS primersearch
        labels_dir = directory containing taxa translations from kraken-translate
        unclass_dir = directory containing the unclassified contigs from kraken

Output: ## under construction
"""


import os
import sys
# from Bio.Emboss.PrimerSearch import OutputRecord, Amplifier, read


__author__ = "Sung Im"
__email__ = "wla9@cdc.gov"
__version__ = "0.1"


class OutputRecord(object):
    """ Dictionary object to store info from primersearch output.

    Amplifiers is a dictionary where keys are the primer names and
    the values are an Amplifier object whose attributes store the
    output results of each primer pair.
    """
    def __init__(self):
        self.amplifiers = {}


class Amplifier(object):
    """ Store information from a single amplification from primer.

    """
    def __init__(self):
        self.amp_len = 0
        self.contig_id = ""
        self.contig_len = 0
        self.f_primer = ""
        self.f_start = 0
        self.f_mismatch = 0
        self.r_primer = ""
        self.r_start = 0
        self.r_mismatch = 0


def read_primersearch_result(handle):
    """ Parse output from EMBOSS primersearch.

    """
    record = OutputRecord()

    for line in handle:
        if not line.strip():
            continue
        elif line.startswith("Primer name"):
            name = line.split()[-1]
            record.amplifiers[name] = []
        elif line.startswith("Amplimer"):
            amplifier = Amplifier()
            record.amplifiers[name].append(amplifier)
        elif line.startswith("\tSequence: "):
            amplifier.contig_id = line.replace("\tSequence: ", "").rstrip()
        elif line.startswith("\tlength="):
            contig_len = line.replace("\tlength=", "").split()[0]
            amplifier.contig_len = int(contig_len)
        elif "forward strand" in line:
            f_start = line.split(" ")[5]
            f_mismatch = line.split(" ")[7]
            amplifier.f_primer = line.split(" ")[0].lstrip("\t")
            amplifier.f_start = int(f_start)
            amplifier.f_mismatch = int(f_mismatch)
        elif "reverse strand" in line:
            r_start = line.split(" ")[5].strip("[]")
            r_mismatch = line.split(" ")[7]
            amplifier.r_primer = line.split(" ")[0].lstrip("\t")
            amplifier.r_start = int(r_start)
            amplifier.r_mismatch = int(r_mismatch)
        elif line.startswith("\tAmplimer length: "):
            length = line.split()[-2]
            amplifier.amp_len = int(length)
        else:
            continue

    return record


class TaxRecord(object):
    """ Dictionary object to store taxa objects.

    """
    def __init__(self):
        self.taxonomy = {}


def read_kraken_labels(handle):
    """ Parse the taxa labels from kraken-translate.

    """
    record = TaxRecord()
    for line in handle:
        contigId = line.rstrip().split('\t')[0]
        classification = line.rstrip().split('\t')[1].split(';')[-1]
        record.taxonomy[contigId] = classification
    return record


def read_kraken_unclassified(handle):
    """ Parse the kraken output of unclassified contigs.

    """
    unclassifiedContigs = []
    for line in handle:
        if line.startswith('>'):
            contigId = line.split(' ')[0].lstrip('>')
            unclassifiedContigs.append(contigId)
    return unclassifiedContigs


def read_amplicon_info(handle):
    """ Parse Emboss primersearch output and store hit info as hash object.

    Return lists containing primer ids that did not amplify, hit more than one
    target, and hit one target.
    """
    with open(handle, 'r') as infile:

        noHits = []         # primer ids that did not amplify
        contigHits = []     # contig ids where amplification occurred
        multiHits = []      # primer ids that amplified more than one target
        ampLengths = []

        embossRecord = read_primersearch_result(infile)

        for name in embossRecord.amplifiers:
            if len(embossRecord.amplifiers[name]) == 0:
                noHits.append(name)
            elif len(embossRecord.amplifiers[name]) > 1:
                multiHits.append(name)
            for amplifier in embossRecord.amplifiers[name]:
                contigHits.append(amplifier.contig_id)
                ampLengths.append(amplifier.amp_len)

    return noHits, contigHits, multiHits, ampLengths


def read_kraken_translate(kraken_labels, kraken_unclassified):
    """ Parse the kraken-translate and unclassified outputs and return lists.

    """
    with open(kraken_labels, 'r') as labels, \
            open(kraken_unclassified) as unclassified:

        targetContigs = []
        otherContigs = []

        unclassed = read_kraken_unclassified(unclassified)
        krakenRecord = read_kraken_labels(labels)

        for contig, classification in krakenRecord.taxonomy.items():
            if 'Salmonella' in classification:
                targetContigs.append(contig)
            else:
                otherContigs.append(contig)

    return targetContigs, otherContigs, unclassed


if __name__ == "__main__":

    # TODO the input for the directory paths should be command line arguments
    # Paths to files
    emboss_dir = '/mnt/scicomp-groups/OID/NCEZID/DFWED/EDLB/share/projects/CIMS/Salmonella/PrimerSpecificity/embossResults/'                # sys.argv[1]
    labels_dir = '/mnt/scicomp-groups/OID/NCEZID/DFWED/EDLB/share/projects/CIMS/Salmonella/PrimerSpecificity/krakenResults/translations/'   # sys.argv[2]
    unclass_dir = '/mnt/scicomp-groups/OID/NCEZID/DFWED/EDLB/share/projects/CIMS/Salmonella/PrimerSpecificity/krakenResults/unclassified/'  # sys.argv[3]

    emboss_paths = [os.path.join(emboss_dir, fn) for fn in next(os.walk(emboss_dir))[2]]
    labels_paths = [os.path.join(labels_dir, fn) for fn in next(os.walk(labels_dir))[2]]
    unclass_paths = [os.path.join(unclass_dir, fn) for fn in next(os.walk(unclass_dir))[2]]

    # Let's parse the Emboss primer search outputs
    for file in emboss_paths:

        filename = os.path.basename(file)
        with open(file, 'r') as handle:
            record = read_primersearch_result(handle)

            for name in record.amplifiers:
                for amplifier in record.amplifiers[name]:
                    # print(amplifier)
                    # print(amplifier.f_mismatch)
                    # print(amplifier.r_mismatch)
                    if (amplifier.f_mismatch > 0) or (amplifier.r_mismatch > 0):
                        print(name)