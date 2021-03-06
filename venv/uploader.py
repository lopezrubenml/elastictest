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


# uploader function
for i in list(dfj.index):
    sip3 = dfj.loc[i]['json']
    res = es.index(index="test_persons", doc_type='sip', id=i, body=sip3)

# refresh
es.indices.refresh(index="test_persons")

# check upload
res = es.search(index="test_persons", body={"query": {"match_all": {}}})

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print(hit)
