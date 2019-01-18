from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
import pandas as pd
from pandas import DataFrame



es = Elasticsearch()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Match Tester'


@app.route('/search/<name>/<doc>', methods=['GET'])
def search(name,doc):
#    name = request.args.get['name']
#    doc = request.args.get['doc']

    body={
	"query":{
		"bool":{
			"should":[
				{"match":{"name":name}},
				{"match":{"doc":doc}}
				]
		    }
	    }
    }

    res = es.search(index="test_persons", doc_type="sip", body=body)
    return jsonify(res['hits']['hits'])


app.run(debug=True)