from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, pymongo
import requests

app = Flask(__name__)
# https://mlab.com create Mongo database with 500 Mb FREE
app.config['MONGO_DBNAME'] = 'first'  # name of database
# url to mongo database (if new account, create user and pass to new_db)
app.config['MONGO_URI'] = 'mongodb://dell:test@ds121089.mlab.com:21089/first'
mongo = PyMongo(app)

LANG = 'python'  # choose language to filter
SORT = 'stars'  # sort by star rating
MIN_STARS = 500  # start to collect from 500 stars
ORDER = 'desc'  # chouse order (ascending or descending)
# Github API url to collect data
api = 'https://api.github.com/search/repositories?q=language:{}+{}:%3E={}&order={}'.format(
    LANG, SORT, MIN_STARS, ORDER)  # filter by this variables


@app.route('/search', methods=['GET'])
def search():
    """
    Endpoint to see all requested repositories from Github.
    Filtered by language - Python and stars rate >= 500. Formatted as json.
    Choose what fields you need to store in database collection document.
    """
    data = requests.get(api).json()  # data from api url, converted into json
    return jsonify({'result': data})  # returning json formatted data


@app.route('/add', methods=['POST'])
def add():
    """
    Endpoint to fill in the db with collection of github repositories.
    Filtered by language 'Python' and stars rate >= 500.
    Fields of documents from GitHub Search API: full_name, html_url,
    description, stargazers_count, language. - Choose your own if needed!
    """
    data = requests.get(api).json()  # data from api url, converted into json
    git = mongo.db.git  # initialise collection name in mongo_db
    for i in data['items']:  # iterate thru data.items
        # store data into documents with all requested fields
        document = {'name': i['full_name'],  # all git.doc.full_names
                    'url': i['html_url'],  # all git.doc.html_urls
                    'description': i['description'],  # all git.doc.descriptions
                    'count': i['stargazers_count'],  # all git.doc.stargazers_counts
                    'language': i['language']}  # all git.doc.languages
        git.insert(document)  # adding documents to database
    return 'We added data to DB'  # returning success string


@app.route('/list', methods=['GET'])
def list():
    """
    List of documents, - collection of git db.
    Endpoint filled with repositories data fields (name, url, description, count, language).
    Page pagination with limit and offset parameters, total count of records. Added docsrings and comments.
    To list all documents with limit to 5 per page open this url: http://0.0.0.0:5000/list?limit=5%offset=0
    """
    git = mongo.db.git  # database with which we're working
    total = git.find().count()  # count total documents in db
    offset = int(request.args['offset'])  # if we need to start from 'n_doc' - 'type in number - ex.:offset=0'
    limit = int(request.args['limit'])  # limit to 'n' doc's per page - 'type in number - ex.:limit=5'
    first_id = git.find().sort('_id', pymongo.ASCENDING)  # find all id's, sort them in asc.
    last_id = first_id[offset]['_id']  # get last id: 'first - typed_offset_number'
    document_list = []  # create empty list of documents to store data from db
    # iterate thru db to find, sort, limit and append to list of documents with self.fields.
    for q in git.find({'_id': {'$gte': last_id}}).sort('_id', pymongo.ASCENDING).limit(limit):
        # store all git.documents with self.fields into document_list
        document_list.append({'name': q['name'],  # all git.doc.names
                              'url': q['url'],  # all.git.doc.urls
                              'description': q['description'],  # all.git.doc.descs
                              'count': q['count'],  # all git.doc.counts
                              'language': q['language']})  # all git.doc.langs
    # making pagination: next url. Using url + limit + (offset + limit) parameters.
    link_next = 'http://0.0.0.0:5000/list?limit=' + str(limit) + '&offset=' + str(offset + limit)
    next_text = 'NEXT'
    next_url = '<a href="{}">{}</a>'.format(link_next, next_text)  # hyperlinking next_url
    # making pagination: prev url. Using url + limit + (offset - limit) parameters.
    link_prev = 'http://0.0.0.0:5000/list?limit=' + str(limit) + '&offset=' + str(offset - limit)
    prev_text = 'PREV'
    prev_url = '<a href="{}">{}</a>'.format(link_prev, prev_text)  # hyperlinking prev_url
    # returning json object as result: document list, count total documents, pagination urls
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
