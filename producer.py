from time import sleep
import requests
import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
	value_serializer=lambda x: 
        json.dumps(x).encode('utf-8'))

for y in range(50):
	req = requests.get("http://api.open-notify.org/iss-now")
	response = json.loads(req.content)
	print(response)
	producer.send('iss_location', value=response)
	sleep(10)

