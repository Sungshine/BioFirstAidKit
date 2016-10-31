#!/usr/bin/python3

""" Modified classes and methods from BioPython.Emboss.Applications module.

"""

# import statements go here

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


def parse_amplicon_info():
    """ Parse resulting primersearch results.

    Return lists containing primer ids that did not amplify, hit more than one target, and hit one target.
    """
    emboss_results = file

    noHits = []     # primer ids that did not amplify
    contigHits = [] # contig ids where amplification occurred
    multiHits = []  # primer ids that amplified more than one target

    with open(emboss_results, 'r') as infile:

        embossRecord = read_primersearch_result(infile)
        for name in embossRecord.amplifiers:
            if len(embossRecord.amplifiers[name]) == 0:
                noHits.append(name)
            elif len(embossRecord.amplifiers[name]) > 1:
                multiHits.append(name)
            for amplifier in embossRecord.amplifiers[name]:
                contigHits.append(amplifier.contig_id)

    return noHits, contigHits, multiHits



if __name__ == "__main__":

    ## Let's parse the Emboss primer search output for an isolate/assembly
    primersearch_result_file = '/home/sim/Projects/CIMS/salmonella/embossResults/2013RAN-169-M947-14-049-Loopy_contigs4.fasta.emboss'
    with open(primersearch_result_file, 'r') as emboss_infile:

        embossRecord = read_primersearch_result(emboss_infile)

        noHits = []         # primer ids that did not amplify
        contigHits = []     # contig ids where amplification occurred

        for name in embossRecord.amplifiers:
            # create list of primer pairs that did not amplify
            if len(embossRecord.amplifiers[name]) == 0:
                noHits.append(name)
            # check to see if any primers hit multiple places
            # if len(embossRecord.amplifiers[name]) > 1:
            #     print("AHHHHHHHH")
            for amplifier in embossRecord.amplifiers[name]:
                # print(amplifier.contig_id)
                contigHits.append(amplifier.contig_id)

        print('nohits = {}'.format(len(noHits)))
        print('hits = {}'.format(len(contigHits)))
        print('uniq_hits = {}'.format(len(set(contigHits))

        ## Let's parse the kraken-translate output for the same file
        kraken_labels = '/home/sim/Projects/CIMS/salmonella/2013RAN-169-M947-14-049-Loopy_contigs4.sequence.labels'
        kraken_unclassified = '/home/sim/Projects/CIMS/salmonella/2013RAN-169-M947-14-049-Loopy_contigs4.fasta.unclassified'
        with open(kraken_labels, 'r') as labels, open(kraken_unclassified, 'r') as unclassified:

            targetContigs = []
            otherContigs = []
            unclassed = read_kraken_unclassified(unclassified)

            krakenRecord = read_kraken_labels(labels)

            for contig, classification in krakenRecord.taxonomy.items():
                if 'Salmonella' in classification:
                    targetContigs.append(contig)
                else:
                    otherContigs.append(contig)

        print("kraken targetContigs = {}".format(len(targetContigs)))
        print("kraken otherContigs = {}".format(len(otherContigs)))
        print("kraken unclassed = {}".format(len(unclassed)))

    # for contigId in uniqContigHits:
    #     print(set(contigHits).intersection(targetContigs))
        print(len(set(contigHits).intersection(targetContigs)))
        print(set(contigHits).intersection(otherContigs))
        print(set(contigHits).intersection(unclassed))

        # print(contigHits)
        # print(len(set(targetContigs).union(otherContigs).union(unclassed)))
        # for i in noHits:
        #     print(i)
