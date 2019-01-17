from elasticsearch import Elasticsearch
import pandas as pd
from pandas import DataFrame
import requests


es = Elasticsearch()

df = pd.read_csv('C:\\Users\\rlopezlam\\Documents\\2018\\list_search\\base_part_1.csv')
df_docs = df[~df.doc_number.isna()]
df_docs = df_docs[['p_name', 'doc_number', 'resident']]
df_docs.columns = ['name', 'doc', 'country']
dfj = DataFrame()
dfj['json'] = df_docs.apply(lambda x: x.to_json(), axis=1)
sip2 = dfj.iloc[6]['json']

sip = {
    'name': 'Tyson Anderson',
    'doc': 'W894384830',
    'country': 'Not Known',
}

res = es.index(index="test_persons", doc_type='sip', id=181, body=sip2)
print(res['result'])

res = es.get(index="test_persons", doc_type='sip', id=1)
print(res['_source'])

es.indices.refresh(index="test_persons")

res = es.search(index="test_persons", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print(hit)
