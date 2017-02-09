#!/usr/bin/env python2.7

""" Replace IUPAC alphabet letters with N.

"""


__author__ = 'Sung Im'
__email__ = 'sungbin401@gmail.com'


if __name__ == '__main__':


    string = input('Enter your sequence string: ')
    print('Length of input sequence: {}'.format(len(string)))

    nucleotides = ['A', 'T', 'C', 'G']
    newstring = []

    for char in string:
        if char not in nucleotides:
            print('{} found. Replacing with N.'.format(char))
            char = 'N'
            newstring.append(char)
        else:
            newstring.append(char)

    print(''.join(newstring))
    print('Length of new string: {}'.format(len(''.join(newstring))))