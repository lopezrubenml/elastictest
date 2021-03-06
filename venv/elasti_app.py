from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
import pandas as pd
from pandas import DataFrame
from pandas.io.json import json_normalize
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from match_func import match_func_no_counter



es = Elasticsearch()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Match Tester'

@app.route('/form', methods = ['POST','GET'])
def form():
	if request.method == 'POST':
		name = request.form['name']
		doc = request.form['doc']
		country = request.form['country']

		body = {
			"size": 100,
			"query": {
				"bool": {
					"should": [
						{"match": {"name": {"query": name, "fuzziness": "2"}}},
						{"match": {"doc": {"query": doc, "fuzziness": "2"}}}
					]
				}
			}
		}

		res = es.search(index="test_persons", doc_type="sip", body=body)
		potential_matches = json_normalize(res['hits']['hits'])
		if potential_matches.size == 0:
			return ('No Match1')
		potential_matches = potential_matches[['_source.country', '_source.name', '_source.doc']]
		potential_matches.columns = ['list_country', 'list_name', 'list_doc']
		test_user1 = DataFrame({'user_name': name, 'user_doc': doc, 'user_country': country}, index=[0])
		name_param1 = 0.7
		doc_param1 = 0.8
		site_param1 = 0.2
		mid_results = match_func_no_counter(test_user=test_user1,
											list_db=potential_matches,
											name_param=name_param1,
											doc_param=doc_param1,
											site_param=site_param1)
		name_min = 70
		doc_min = 70
		filtered_mid_results = mid_results[(mid_results.name_score > name_min) | (mid_results.doc_score > doc_min)]
		if filtered_mid_results.size > 0:
			final_results = potential_matches.loc[list(filtered_mid_results.index)].to_json(orient='index')
		else:
			final_results = 'No Match2'
		return (final_results)

	return '''<form method="POST"> 
	Name <input type="text" name="name">
	Doc <input type="text" name="doc">
	Country <input type="text" name="country">
	<input type="submit">
	</form>'''

@app.route('/search/<name>/<doc>/<country>', methods=['GET'])
def search(name,doc,country):

	body = {
	"size":100,
	"query":{
		"bool":{
			"should":[
				{"match":{"name":{"query":name, "fuzziness":"2"}}},
				{"match":{"doc":{"query":doc, "fuzziness":"2"}}}
				]
			}
		}
	}


	res = es.search(index="test_persons", doc_type="sip", body=body)
	potential_matches = json_normalize(res['hits']['hits'])
	if potential_matches.size == 0:
		return('No Match')
	potential_matches = potential_matches[['_source.country','_source.name','_source.doc']]
	potential_matches.columns = ['list_country','list_name','list_doc']
	test_user1 = DataFrame({'user_name':name,'user_doc':doc,'user_country':country}, index=[0])
	name_param1 = 0.7
	doc_param1 = 0.8
	site_param1 = 0.2
	mid_results = match_func_no_counter(test_user=test_user1,
										list_db=potential_matches,
										name_param=name_param1,
										doc_param=doc_param1,
										site_param=site_param1)
	name_min = 70
	doc_min = 70
	filtered_mid_results = mid_results[(mid_results.name_score > name_min) | (mid_results.doc_score > doc_min)]
	if filtered_mid_results.size > 0:
		final_results = potential_matches.loc[list(filtered_mid_results.index)].to_json(orient='index')
	else:
		final_results = 'No Match'
	return(final_results)



app.run(debug=True)
