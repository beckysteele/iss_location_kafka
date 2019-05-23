## Streaming ISS Geolocation Data to MongoDB with Apache Kafka & Python

# Package & Installation Requirements:
- Apache Kafka & Zookeeper
- Python packages: `pymongo`, `json`, `requests`, `time`

# What Producer.py does:
- Creates an instance of `KafkaProducer` using `localhost:9092`
- Serializes data for `utf-8` encoding using a lambda function (to ensure there are no encoding errors in the future).
- The app requests a payload from `http://api.open-notify.org/iss-now`, loads that response into a digestible format by the consumer, and sends that response to the Kafka server. It prints a message to the screen each time, and waits 10 seconds before doing the same thing again, for a total of 50 requests.

# What Consumer.py does:
- Creates an instance of `KafkaConsumer` using `localhost:9092`
- Serializes data for `utf-8` encoding using a lambda function (to ensure there are no encoding errors in the future).
- Creates an instance of `MongoClient` at `localhost:27017`
- Creates a new collection at `client.iss.iss_location`, with `iss` being the database and `iss_location` being the name of the new collection.
- For every message on the Kafka stream, the consumer ingests that message's `.value` property, dumps it to a `dict` type, inserts that new document into the `iss_location` collection, and prints a message to the screen with the object id and message of the inserted document.

# How to Start Apache Kafka & Zookeeper Servers:
1. In Terminal, navigate to your Kafka directory locally (mine is at root).

2. Start the Zookeeper server: `sh bin/zookeeper-server-start.sh config/zookeeper.properties`

3. In a new terminal window (at the Kafka directory), start the Kafka server: `sh bin/kafka-server-start.sh config/server.properties`

4. In a new terminal window, run the MongoDB Daemon `mongod`

# How to Run Producer & Consumer (and expected behaviors):
1. In another terminal window, once you verify that Kafka & Zookeeper servers are running, run Producer.py: `python producer.py`. Expected behavior: a message with the ISS Location API payload should print to the console, and is served to the Kafka stream.

2. In another terminal window, run Consumer.py: `python consumer.py`. Expected behavior: a message should print to the console with confirmation that a document containing the messages consumed from Kafka stream has been inserted to a MongoDB named `iss` in the `iss_location` collection.

3. Prove that the documents exist in your MongoDB by launching the Mongo client in another terminal: `mongo`, and then `use iss` and `db.iss_location.count()`. Every 10 seconds, you should see that count go up by 1 as the consumer inserts new documents from the Kafka stream.

# What Needs Done:
[ ] Feed data to PostgreSQL
[ ] Testing and better error checking
[ ] Continuous integration/automation tooling (i.e. Bamboo, Jenkins)
