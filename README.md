# key-value
simple key-value service

### Config parameters
## below config parameters are for Mongo db to store key value
```
MONGO_HOST
MONGO_PORT
MONGO_DB
```
## below config parameters are to send email notifications to subscribers
```
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "chitenderkumar.16@gmail.com"
SMTP_PASSWORD = "test123"
```

### building docker image
```
sudo docker build .
```
## run docker image
```
sudo docker run --env MONGO_HOST=192.168.29.59 --env MONGO_PORT=27017 --env MONGO_DB=data --env SMTP_HOST="smtp.gmail.com" --env SENDER_EMAIL="chitenderkumar.16@gmail.com" --env SMTP_PASSWORD="XXXXXX" --env SMTP_PORT="465" BUILD_DOCKER_IMAGE_ID
```
### List last 50 key values
```
curl http://localhost:80/list
```

### Create new key value 
```
curl -X POST 'http://localhost:80/create' -H "Content-Type: application/json" --data '{"key": "employee", "value": "chitender", "subscribers": "chitenderkumar.16@gmail.com"}'
```
### Update existing key value
```
curl -X PUT 'http://localhost:80/update' -H "Content-Type: application/json" --data '{"key": "employee", "value": "chitender6", "subscribers": "chitenderkumar.16@gmail.com"}'
```