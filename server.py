# mongo.py

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

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
    output.append({'key': document['key'], 'value': document['value'], 'subscribers': document['subcriber']})
  return jsonify({'Metrics for ssh log-in attempts': {'result' : output}})

@app.route('/create', methods=['PUT'])
def add_report():
  stats = mongo.db.object
  key = request.args.PUT('key')
  value = request.args.PUT('value')
  subscribers = request.args.put('subscribers')
  record = stats.insert({'key': key, 'value': value , 'subscribers': subscribers })
  print (record.inserted_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='80')
