import os
import csv
import sqlite3
import requests
import datetime


def fetch_api_ids(pnusaid):

    myD = {}

    db = '/scicomp/home/edlb-sneakernet/bin/PulsenetDataRescue/db/basespace.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()

    sql = "SELECT Id, SampleId, DateCreated FROM Samples WHERE Name LIKE '%{}%'".format(
        pnusaid
    )
    c.execute(sql)
    result = c.fetchall()
    if len(result) == 0:
        return pnusaid
    else:
        for i in result:
            fid = i[0]
            fname = i[1]
            date = i[2].replace('T', ' ').rstrip('.0000000')
            if fname not in myD.keys():
                myD[fname] = [fid, date]
            else:
                old = myD[fname][1]
                f = '%Y-%m-%d %H:%M:%S'
                if datetime.datetime.strptime(old, f) < datetime.datetime.strptime(date, f):
                    myD[fname] = [fid, date]
                else:
                    continue
        conn.close()

        for k, v in myD.iteritems():
            return(k, v[0], v[1])


def read_input_ids(f):
    d = {}
    with open(f, 'rU') as fh:
        r = csv.reader(fh, delimiter='\t')
        for row in r:
            pnusaid = row[0]
            outbreak = row[1]
            if pnusaid not in d.keys():
                d[pnusaid] = outbreak
            else:
                break
    return d

if __name__ == '__main__':

    # final = {}
    #
    # f = '/scicomp/home/edlb-sneakernet/tmp/sung/quabity_assuance/run_list.txt'
    # my_ids = read_input_ids(f)
    #
    # for k, v in my_ids.iteritems():
    #     h = fetch_api_ids(k)
    #     print(k, v, h)
        # print('{}\t{}\t{}\t{}\t{}\t'.format(k, h))

    # d = fetch_api_ids()
    #
    # # API
    url = 'https://api.basespace.illumina.com/v1pre3/samples/{}'
    access_token = '45d41295ac594eb18cc9a347af4af638'
    headers = {'x-access-token': access_token}
    params = {'Limit': '1024', 'SortDir': 'Desc', 'SortBy': 'DateCreated'}
    # for k, v in d.iteritems():
    #     pnusa = k
    #     sid = v[0]
    #     date = v[1]
    #     r = requests.get(url.format('81490435'), headers=headers, params=params).json()
    #     print(r['Response']['Properties']['Items'][0]['Items'][0]['HrefBaseSpaceUI'])

    pnusa = 'PNUSAE014367'
    sid = '135376242'
    date = '2018-05-29 15:20:13'
    r = requests.get(url.format('81490435'), headers=headers, params=params).json()
    x = r['Response']['Properties']['Items'][0]['Items'][0]['HrefBaseSpaceUI']
    strx = str(x)
    url = '{}/files'.format(strx)
    r2 = requests.get(url, headers=headers, params=params)
    print(r2)

    # print(r['Response']['Properties']['Items'][0]['Items'][0]['HrefBaseSpaceUI'])