#!/usr/bin/python env

input = open("/Users/sungshine/Downloads/2012K-1420_LargeContigs.fna.primersearch", "r")

prime_dict = dict()

for line in input:
    if not line.strip():    # ignore lines with only white space
        continue
    elif line.startswith("Primer name"):
        name = line.split()[-1]
        # print(name)
        dict[name] = []
    elif line.startswith("Amplimer"):

# def read(handle):
# 52      """Get output from primersearch into a PrimerSearchOutputRecord
# 53      """
# 54      record = OutputRecord()
# 55
# 56      for line in handle:
# 57          if not line.strip():
# 58              continue
# 59          elif line.startswith("Primer name"):
# 60              name = line.split()[-1]
# 61              record.amplifiers[name] = []
# 62          elif line.startswith("Amplimer"):
# 63              amplifier = Amplifier()
# 64              record.amplifiers[name].append(amplifier)
# 65          elif line.startswith("\tSequence: "):
# 66              amplifier.hit_info = line.replace("\tSequence: ", "")
# 67          elif line.startswith("\tAmplimer length: "):
# 68              length = line.split()[-2]
# 69              amplifier.length = int(length)
# 70          else:
# 71              amplifier.hit_info += line
# 72
# 73      for name in record.amplifiers:
# 74          for amplifier in record.amplifiers[name]:
# 75              amplifier.hit_info = amplifier.hit_info.rstrip()
# 76
# 77      return record