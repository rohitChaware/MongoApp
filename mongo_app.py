from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

MONGO_DBNAME = 'test'
app.config['MONGO_DBNAME'] = MONGO_DBNAME
MONGO_URL = os.environ['MONGO_URL']
app.config['MONGO_URI'] = 'mongodb://' + MONGO_URL + '/' + MONGO_DBNAME

mongo = PyMongo(app)

@app.route('/all', methods=['GET'])
def get_all():
  zips = mongo.db.zips
  output = []
  for s in zips.find():
    output.append({'city' : s['city'], 'location' : s['loc'], 'state': s['state']})
  return render_template('json_table.html',  posts=output)

@app.route('/zip/<name>', methods=['GET'])
def get_one_zip(name):
  zips = mongo.db.zips
  s = zips.find_one({'city' : name})
  if s:
    output = {'city' : s['city'], 'location' : s['loc'], 'state': s['state']}
  else:
    output = "No such city."
  return jsonify({'result' : output})

@app.route('/zip', methods=['POST'])
def add_zip():
  zips = mongo.db.zips
  city = request.json['city']
  loc = request.json['loc']
  state = request.json['state']
  zip_id = zips.insert({'city': city, 'loc': loc, 'state':  state})
  new_zip = zips.find_one({'_id': zip_id })
  output = {'name' : new_zip['city'], 'location' : new_zip['loc'], 'state': new_zip['state']}
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(port=80)
