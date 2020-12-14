# mongo.py

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask import abort
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import os

app = Flask(__name__)
try:
    # Python 3.x
    from urllib.parse import quote_plus
except ImportError:
    # Python 2.x
    from urllib import quote_plus

app.config['MONGO_DBNAME'] = 'data'
app.config['MONGO_URI'] = "mongodb://%s:%s/%s" % (
  os.environ['MONGO_HOST'], os.environ['MONGO_PORT'], os.environ['MONGO_DB']
)
SMTP_HOST = os.environ['SMTP_HOST']
SMTP_PORT = os.environ['SMTP_PORT']
SENDER_EMAIL = os.environ['SENDER_EMAIL']
SMTP_PASSWORD = os.environ['SMTP_PASSWORD']
print (SMTP_PORT)
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

@app.route('/update', methods=['PUT'])
def update_report():
  stats = mongo.db.object
  key = request.json['key']
  newValue = request.json['value']
  newSubscribers = request.json['subscribers']
  documents = stats.find_one({'key': key},{"key":1, "value":1, "subscribers":1,"_id": False})
  presentValue = documents['value']
  presentSubscribers = documents['subscribers']
  update = stats.find_one_and_update(
    {"key": key},
    {"$set":
        {"value": newValue, "subscribers": newSubscribers}
    },upsert=True
  )
  ######## Mailing
  port = SMTP_PORT  # For SSL
  smtp_server = SMTP_HOST
  sender_email = SENDER_EMAIL  # Enter your address
  receiver_email = presentSubscribers  # Enter receiver address
  password = SMTP_PASSWORD
  message = """Subject: key {key} has been updated

  value for {key} has been updated to {newValue}"""

  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, message.format(key=key, newValue=newValue))
  response = {
        'key': key,
        'value': newValue,
        'subscribers': newSubscribers,
        'Description': "update success"
    }
  return jsonify({'response': response}), 201  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='80')
