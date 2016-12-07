#!/usr/bin/env python

""" SRR Id retrieval
"""


import requests
from xml.etree import ElementTree

__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.1'


esearch_resp = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?retmode=json&db=biosample&term=PNUSAL000100&usehistory=y").json()

id = esearch_resp['esearchresult']['idlist'][0]     #2347439
webenv = esearch_resp['esearchresult']['webenv']
querykey = esearch_resp['esearchresult']['querykey']

elink_resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?retmode=json&dbfrom=biosample&db=sra&query_key={}&WebEnv={}'.format(querykey, webenv, id)).json()

link = elink_resp['linksets'][0]['linksetdbs'][0]['links'][0]   #491766

efetch_resp = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id={}'.format(link))

# print(efetch_resp.content)
tree = ElementTree.fromstring(efetch_resp.content)
# for child in tree.iter('PRIMARY_ID'):
#     print(child[1])

for i in tree.findall('EXPERIMENT'):
    print(i)








# payload = {'db': 'biosample', 'query': 'PNUSAL000100'}

# root = ElementTree.fromstring(response.content)
# print(root)
# for child in root:
#     print(child.tag)

# for child in root:
#     print(child, child.attrib)

# for elem in root.iter(tag='Count'):
#     print(elem)

