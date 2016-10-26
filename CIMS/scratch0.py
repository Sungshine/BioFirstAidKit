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


def Read(handle):
    """ Parse output from EMBOSS primersearch.

    """
    record = OutputRecord()

    for line in handle:
        if not line.strip():
            continue
            #TODO We want to capture the primer sets that have no hits
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


if __name__ == "__main__":

    emboss_outfile = '/home/sim/Projects/CIMS/salmonella/embossResults/2013RAN-169-M947-14-049-Loopy_contigs4.fasta.emboss'
    with open(emboss_outfile, 'r') as emboss_infile:

        my_dict = Read(emboss_infile)

        no_hits = []        # lists primer ids
        contigHits = []

        for name in my_dict.amplifiers:
            # create list of primer pairs that did not amplify
            if len(my_dict.amplifiers[name]) == 0:
                no_hits.append(name)
            for amplifier in my_dict.amplifiers[name]:
                # print(amplifier.contig_id)
                contigHits.append(amplifier.contig_id)

        uniq_contig_hits = set(contigHits)  # stores the final list of contigs that targets where amplified from

        # print('nohits = {}'.format(len(no_hits)))
        # print('hits = {}'.format(len(contigHits)))
        # print('uniq_hits = {}'.format(len(uniq_contig_hits)))
