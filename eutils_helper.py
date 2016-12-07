#!/usr/bin/env python

""" SRR Id retrieval
"""

import csv
import requests
from xml.etree import ElementTree

__author__ = 'Sung Im'
__email__ = 'wla9@cdc.gov'
__version__ = '0.1'


# globals
esearch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
elink_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
efetch_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

# Read in csv file containing PulseNet WGS_Ids
# with open('/home/sim/Projects/PulseNetThings/Listeria_SRA_lookup_20160926.csv', 'rb') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     next(reader, None)  # skips the header
#     for row in reader:
#         id = row[0]

# testlist = ['FDA00007715', 'CFSAN003732']
testlist = ['FDA00007715']
# testlist = ['PNUSAL000100']
for id in testlist:
    esearch_resp = requests.get(esearch_base
                                +'?retmode=xml&db=biosample&term={}&usehistory=y'
                                .format(id))
    # print(esearch_resp.content)
    s_tree = ElementTree.fromstring(esearch_resp.content)
    for s_node in s_tree.iter('IdList'):
        try:
            s_id = s_node[0].text
            # print(s_id)
        except IndexError, KeyError:
            print(id, "WGS Id not found.")

        elink_resp = requests.get(elink_base + '?retmode=xml&dbfrom=biosample&db=sra&id={}'.format(s_id))
        # print(elink_resp.content)

        e_tree = ElementTree.fromstring(elink_resp.content)
        for e_node in e_tree.findall('LinkSet'):

            link = e_node.find('LinkSetDb')
            # If no links exist, move on to next id
            if link is None:
                print(id, 'No links exist.')
                continue
            else:
                link = link.find('Link')
                e_id = link[0].text

                efetch_resp = requests.get(efetch_base + '?db=sra&id={}'.format(e_id))


        # for e_node in e_tree.iter('Link'):
        #     if e_node == '':
        #         print(id, "No links out.")
            # try:
            #     e_id = e_node[0].text
            #     print(e_node[0].text)
            # except IndexError, KeyError:
            #     print(id, 'No out links exist.')
            # if not e_id:
            #     print('No e_id.')

            # efetch_resp = requests.get(efetch_base + '?db=sra&id={}'.format(e_id))
            # # print(efetch_resp.content)
            # f_tree = ElementTree.fromstring(efetch_resp.content)
            # for node in f_tree.iter('IDENTIFIERS'):
            #     # print(node[0].text)
            #     try:
            #         primary_id = node[0].text
            #     except IndexError, KeyError:
            #         print(id, 'No SRR id exists')
            #     if not primary_id:
            #         print('No primary_id.')
            #     if 'SRR' in primary_id:
            #         print(primary_id)
            #     else:
            #         print(id, 'No SRR Id exists.')
            #         continue


    # try:
    #     id = esearch_resp['esearchresult']['idlist'][0]
    #     webenv = esearch_resp['esearchresult']['webenv']
    #     querykey = esearch_resp['esearchresult']['querykey']
    # except IndexError:
    #     print(id, " PNUSA Id not found.")
    #     continue
    #     # pass

    # elink_resp = requests.get(elink_base +
    #                           '?retmode=json&dbfrom=biosample&db=sra&query_key={}&WebEnv={}'
    #                           .format(querykey, webenv, id)).json()
    # print(elink_resp)
    # try:
    #     link = elink_resp['linksets'][0]['linksetdbs'][0]['links'][0]
    #     print(link)
    # except IndexError, KeyError:
    #     print(id, " No links out.")
    #     continue
    #     # pass

    # efetch_resp = requests.get(efetch_base + '?db=sra&id={}'.format(link))
    #
    # tree = ElementTree.fromstring(efetch_resp.content)
    #
    # for node in tree.iter('IDENTIFIERS'):
    #     primary_id = node[0].text
    #     if 'SRR' in primary_id:
    #         print(primary_id)
    #     else:
    #         continue
    #         # pass