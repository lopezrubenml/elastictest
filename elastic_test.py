from elasticsearch import Elasticsearch

es = Elasticsearch()

sip = {
    'name': 'Boris Gromov',
    'doc': '100109456',
    'country': 'Russia',
}

res = es.index(index="test_person", doc_type='sip', id=1, body=sip)
print(res['result'])

res = es.get(index="test_persons", doc_type='sip', id=1)
print(res['_source'])

es.indices.refresh(index="test_persons")

res = es.search(index="test_persons", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print(hit)
