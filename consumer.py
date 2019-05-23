from kafka import KafkaConsumer
from pymongo import MongoClient
import json

consumer = KafkaConsumer(
	'iss_location',
	bootstrap_servers=['localhost:9092'],
	auto_offset_reset='earliest',
	enable_auto_commit=True,
	group_id='my-group',
	value_deserializer=lambda x: json.loads(x.decode('utf-8')))

client = MongoClient('localhost:27017')
collection = client.iss.iss_location

for message in consumer:
    message = message.value
    document = json.dumps(message)
    collection.insert_one(message)
    print('{} added to {}'.format(message, collection))
