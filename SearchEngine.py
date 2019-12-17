from flask import Flask, jsonify, Response, send_file, request
#from flask_cors import CORS
from Search import Search
from SearchResult import SearchResult
from CommonUtilities import CommonUtilities
from logging import Formatter, FileHandler
import json
import logging

app = Flask(__name__)
#CORS(app)
logger = None

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/search/', methods=['GET', 'POST'])
def get_results():
    global search
    json_data = request.get_data(as_text=True)
    data = json.loads(json_data)
    print(data)
    query = data['query']
    results = Search.getResultDocs(query)
    queryResult = list()
    maxResultCount = int(data['page_count']) * 10
    for result in results[maxResultCount - 10 : maxResultCount]:
        queryResult.append(SearchResult(result, query))
    response = Response(response=json.dumps(queryResult, default=CommonUtilities.obj_dict), status=200, mimetype='application/json')
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/relevance/', methods=["POST"])
def relevance():
    json_data = request.get_data(as_text=True)
    data = json.loads(json_data)
    # logger.info(json_data)
    with open("Relevance.json", "a") as relevanceJson:
        relevanceJson.write(json_data + "\n")
        relevanceJson.close()
    response = Response(response=json.dumps("OK", default=CommonUtilities.obj_dict), status=200, mimetype='application/json')
    return response

def setLogger():
    global logger
    logger = logging.getLogger('relevance')
    logger.setLevel(logging.INFO)
    ch = logging.FileHandler('Relevance.json')
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

if __name__ == '__main__':
    search = Search()
    setLogger()
    app.run(debug=True)
