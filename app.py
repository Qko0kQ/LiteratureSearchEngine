from flask import Flask, Response, send_file, request
from Search import Search
from Recommend import Recommend
from GetResult import GetResult
from util import Util
import json
import logging

app = Flask(__name__)
logger = None


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/search/', methods=['GET', 'POST'])
def get_results():
    global Search
    json_data = request.get_data(as_text=True)
    data = json.loads(json_data)
    query = data['query']
    results = Search.getResultDocs(query)
    recommendation = Recommend.getRecommendations(results)

    queryResult = list()
    maxResultCount = int(data['page_count']) * 10
    for i in range(maxResultCount - 10, maxResultCount):
        queryResult.append(GetResult(results[i], query, recommendation[i]))
    response = Response(response=json.dumps(queryResult, default=Util.obj_dict), status=200, mimetype='application/json')
    return response


@app.route('/relevance/', methods=["POST"])
def relevance():
    json_data = request.get_data(as_text=True)
    data = json.loads(json_data)
    # logger.info(json_data)
    with open("Relevance.json", "a") as relevanceJson:
        relevanceJson.write(json_data + "\n")
        relevanceJson.close()
    response = Response(response=json.dumps("OK", default=Util.obj_dict), status=200, mimetype='application/json')
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
