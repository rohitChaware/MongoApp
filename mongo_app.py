from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import Response
from flask_pymongo import PyMongo
import os
import logging

logging.basicConfig(filename='mongo_app.log',level=logging.DEBUG)

app = Flask(__name__)


MONGO_DBNAME = 'demo'
app.config['MONGO_DBNAME'] = MONGO_DBNAME
MONGO_URL = os.environ['MONGO_URL']
app.config['MONGO_URI'] = 'mongodb://' + MONGO_URL + '/' + MONGO_DBNAME

mongo = PyMongo(app)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/add')
def new_entry():
  return render_template('entry_form.html')

@app.route('/test', methods=['GET'])
def test():
  result = mongo.db.command('ping')
  url_info = {'/': 'Book Reviews home page', '/all': 'To get all records', '/add': 'To add a json record'}
  output = {'MongoDB_ping_status':result, 'url_info': url_info  }
  return jsonify(output)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
  return Response("{'app_status':'success'}", status=200, mimetype='application/json')

@app.route('/all', methods=['GET'])
def get_all():
  reviews = mongo.db.reviews
  output = []
  for s in reviews.find():
    output.append({'book' : s['book'], 'author' : s['author'], 'review': s['review']})
  return render_template('json_table.html',  posts=output)

@app.route('/book/<name>', methods=['GET'])
def get_book_review(name):
  reviews = mongo.db.reviews
  review_list = reviews.find({'book' : name})
  if review_list:
    output = []
    for s in review_list:
     output.append({'book' : s['book'], 'author' : s['author'], 'review': s['review']})
    return render_template('json_table.html',  posts=output)
  else:
    output = "No such book."
    return jsonify({'result' : output})

@app.route('/add', methods=['POST'])
def add_book_review():
  reviews = mongo.db.reviews
  book = request.form['book']
  author = request.form['author']
  review = request.form['review']
  review_id = reviews.insert({'book': book, 'author': author, 'review':  review})
  #new_review = reviews.find_one({'_id': review_id })
  #output = [{'book' : new_review['book'], 'author' : new_review['author'], 'review': new_review['review']}]
  reviews = mongo.db.reviews
  output = []
  for s in reviews.find():
    output.append({'book' : s['book'], 'author' : s['author'], 'review': s['review']})
  return render_template('json_table.html',  posts=output)

@app.route('/http_host', methods=['GET'])
def http_host():
  http_host = os.uname()[1]
  output = {'Http Request Served from host':http_host }
  return jsonify(output)

@app.route('/https_host', methods=['GET'])
def https_host():
  https_host = os.uname()[1]
  output = {'Https Request Served from host':https_host }
  return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
