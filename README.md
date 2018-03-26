# Git Collection Rest API

### A simple Flask REST API that imports data from GitHub Search API https://developer.github.com/v3/search/ 

- Python 3
- Flask
- MongoDB

### Free MongoBD up to 500 Mb

    https://mlab.com - register, create, use

### API url to GET data:

    https://api.github.com/search/repositories?q=language:python+stars:%3E=500&order=desc

### Ready Features

Endpoint to see all requested repositories from Github | 0.0.0.0:5000/search
- Filtered by language - Python and sorted by stars rate >= 500. Formatted as json.
- We can choose what fields needed to store in database collection document.
- Open this url to see what we get: http://0.0.0.0:5000/search

Endpoint to fill in the db with collection of github repositories | 0.0.0.0:5000/add
- Filtered by language 'Python' and sorted by stars rate >= 500.
- Fields of documents from GitHub Search API: 
- full_name, html_url, description, stargazers_count, language. 
- Choose your own if needed!
- To fill in the database open terminal and fire next command: curl -H "Content-Type: application/json" -X POST http://0.0.0.0:5000/add 

Endpoint: List of documents, - collection of git db | 0.0.0.0:5000/list?limit=5%offset=0
- Endpoint filled with repositories data fields (name, url, description, count, language).
- Page pagination with limit and offset parameters, total count of records. Added docsrings and comments.
- To list all documents with limit to 5 per page open this url: http://0.0.0.0:5000/list?limit=5%offset=0

Bonus 1
- Sorting by `stars` to an API. +

Bonus 2
- Docker compose encapsulating all the services related to this app. +


### Make Initial Setup:
```
$ git clone https://w-e-ll@bitbucket.org/w-e-ll/coding-challenge-backend.git

$ cd coding-challenge-backend
```
Docker compose encapsulating
```
$ docker build -t well/collection .

$ docker run -p 5000:5000 well/collection
```
Run curl to fill the db
```
$ curl -H "Content-Type: application/json" -X POST http://0.0.0.0:5000/add
```
Run the server
```
$ python collection.py
```
OR Make Initial Setup
```
- virtualenv -p python3 git-collection
- cd git-collection
- activate it (source bin/activate)
- git clone https://w-e-ll@bitbucket.org/w-e-ll/coding-challenge-backend.git
- cd coding-challenge-backend
- cd app
- pip install -r requirements.txt
- python collection.py
```

made by: https://w-e-ll.com
