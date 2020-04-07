import pandas as pd
from json import dumps
import requests as rq
import os

import processing as prcs
import mining as mine




if __name__ == "__main__":

    # API
    url = "http://localhost:3000/api/node/many"

    # PARAMS
    filename = 'data/t-geo-com2019.csv'
    data = pd.read_csv(filename, sep=';', encoding='ISO-8859-1', low_memory=False)
    nbchunks = 100
    h = ['source', 'date_maj']

    # NODES PATTERNS
    reg = {'labels': ['region'], 'props_keys' : ['REG_CODE', 'REG_LIB'] + h} 
    dpt = {'labels':  ['department'], 'props_keys' : ['DPT_CODE', 'DPT_LIB'] + h}
    arr = {'labels': ['district'], 'props_keys' : ['ARR_CODE', 'ARR_LIB'] + h}
    com = {'labels': ['municipality'], 'props_keys' : ['COM_CODE', 'COM_LIB'] + h} 
    
    # RELATIONS PATTERNS
    r1 = {'labels': ['belongs_to'], 'from': ['department'], 'to': ['region'], "props_keys": h}
    r2 = {'labels': ['belongs_to'], 'from': ['district'], 'to': ['department'], "props_keys": h}
    r3 = {'labels': ['belongs_to'], 'from': ['municipality'], 'to': ['district'], "props_keys": h}
    
    # SPLIT DATA IN CHUNKS AND STORE THEM
    chunks = prcs.make_chunks(data, nbchunks)
    res = {}

    for ch in range( len(chunks) ):
        chunks[ch] = mine.prepare(chunks[ch].to_dict('records'), [reg, dpt, arr, com], [r1, r2, r3])
        # SEND IT TO API
        res = rq.post(url, json={'nodes': chunks[ch]['nodes']})
        print("Code : {}, message : {}, response time : {}".format(res.status_code, res.reason, res.elapsed))

    # print(dumps(chunks[0]['nodes'], indent=4))
 