# mongo.py

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask import abort

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'data'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/data'

mongo = PyMongo(app)

@app.route('/list', methods=['GET'])
def get_all_report():
  stats = mongo.db.object
  documents = stats.find().limit(50)
  print (documents)
  output = []
  for document in documents:
    output.append({'key': document['key'], 'value': document['value'], 'subscribers': document['subscribers']})
  return jsonify({'key-value lists': {'result' : output}})

@app.route('/create', methods=['POST'])
def add_report():
  if not request.json or not 'key' in request.json:
      abort(400)
  stats = mongo.db.object
  key = request.json['key']
  # print (key)
  value = request.json['value']
  # print (value)
  subscribers = request.json['subscribers']
  # print (subscribers)
  record = stats.insert({'key': key, 'value': value , 'subscribers': subscribers })
  print (record)
  # return jsonify({'Response': {'result' : record}})
  # if len(record) == 0:
  #     abort(404)
  response = {
        # 'id': tasks[-1]['id'] + 1,
        'key': request.json['key'],
        'value': request.json['value'],
        'subscribers': request.json['subscribers']
    }
  
  return jsonify({'response': response}), 201
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='80')
