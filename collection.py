from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, pymongo
import requests

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'first'
app.config['MONGO_URI'] = 'mongodb://dell:test@ds121089.mlab.com:21089/first'
mongo = PyMongo(app)

LANG = 'python'
SORT = 'stars'
MIN_STARS = 500
ORDER = 'desc'
api = 'https://api.github.com/search/repositories?q=language:{}+{}:%3E={}&order={}'.format(
    LANG, SORT, MIN_STARS, ORDER)


@app.route('/search', methods=['GET'])
def search():
    """
    Endpoint to see all requested repositories from Github.
    """
    data = requests.get(api).json()
    return jsonify({'result': data})


@app.route('/add', methods=['POST'])
def add():
    """
    Endpoint to fill in the db with collection of github repositories.
    """
    data = requests.get(api).json()
    git = mongo.db.git
    for i in data['items']:
        document = {'name': i['full_name'], 'url': i['html_url'],'description': i['description'], 
                    'count': i['stargazers_count'], 'language': i['language']}
        git.insert(document)
    return 'We added data to DB'


@app.route('/list', methods=['GET'])
def list():
    """
    List of documents, - collection of git db.
    """
    git = mongo.db.git
    document_list = []
    for q in git.find({'_id': {'$gte': last_id}}).sort('_id', pymongo.ASCENDING).limit(limit):
        document_list.append({'name': q['name'], 'url': q['url'], 'description': q['description'],
                              'count': q['count'], 'language': q['language']})
    total = git.find().count()
    offset = int(request.args['offset'])
    limit = int(request.args['limit']) 
    first_id = git.find().sort('_id', pymongo.ASCENDING)
    last_id = first_id[offset]['_id']
    link_next = 'http://0.0.0.0:5000/list?limit=' + str(limit) + '&offset=' + str(offset + limit)
    next_url = '<a href="{}">'NEXT'</a>'.format(link_next)
    link_prev = 'http://0.0.0.0:5000/list?limit=' + str(limit) + '&offset=' + str(offset - limit)
    prev_url = '<a href="{}">'PREV'</a>'.format(link_prev)
    return jsonify({'total': total, 'result': document_list, 'prev_url': prev_url, 'next_url': next_url})


@app.errorhandler(404)
def not_found(error=None):
    """
    404 error page
    """
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
