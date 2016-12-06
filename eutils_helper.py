#!/usr/bin/env python

""" SRR Id retrieval
"""


import requests
from xml.etree import ElementTree

__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.1'

# payload = {'db': 'biosample', 'query': 'PNUSAL000100'}
response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=biosample&term=PNUSAL000100")
root = ElementTree.fromstring(response.content)

# print(root)
# for child in root:
#     print(child.tag)

print(root[0].text)