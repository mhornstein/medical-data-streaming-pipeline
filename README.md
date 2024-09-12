# Kafka Medical Data Pipeline Project

## Project Overview

This project simulates a real-time data pipeline using Apache Kafka, Python, and MongoDB. It simulates a scenario where medical entries about patients are generated, processed to extract key information (illness and medicine), and then stored in MongoDB. The pipeline is designed to run locally on Windows and can be later extended to run on Google Cloud.

## Architecture

The architecture consists of the following components:

1. **Data Generation (Producer)**: A Python script reads medical entries from a CSV file and publishes them to a Kafka topic.
2. **Data Processing (Consumer)**: A Kafka consumer listens to the topic, applies heuristic-based logic to extract illness and medicine information from the medical entry, and publishes the processed data to another Kafka topic.
3. **Data Storage (MongoDB)**: The processed data is consumed by a MongoDB sink connector and stored in a MongoDB collection.
4. **Monitoring & Error Handling**: The pipeline includes logging and error handling through a dead letter queue (DLQ) for failed messages.

## Features

- **Local Deployment**: Run Kafka and MongoDB locally on Windows using Python scripts.
- **Heuristic-Based Processing**: Extract illness and medicine from medical entries using rule-based heuristics.
- **Kafka to MongoDB Integration**: Use Kafka Connect to seamlessly load processed data into MongoDB.
- **Cloud Integration**: The project can be extended to run on Google Cloud with Kafka or Google Pub/Sub, and MongoDB Atlas.

## Prerequisites

- **Python 3.8+**
- **Kafka & ZooKeeper** (Installed locally or using Docker)
- **MongoDB** (Local instance or MongoDB Atlas for cloud)
- **Python Packages**:
  - `kafka-python`
  - `confluent-kafka`
  - `pymongo`
  - `schema-registry-client` (for Kafka message schemas)

### Installing Kafka (Local)

If you're running this locally on Windows, you can install Kafka and ZooKeeper using the following steps:

1. Download Kafka from the official [Apache Kafka](https://kafka.apache.org/downloads) website.
2. Start ZooKeeper:
   ```bash
   bin\windows\zookeeper-server-start.bat config\zookeeper.properties
   ```
3. Start Kafka:
   ```bash
   bin\windows\kafka-server-start.bat config\server.properties
   ```

Alternatively, you can use Docker to run both Kafka and ZooKeeper in containers.

## Running the Project Locally

### Step 1: Set up Kafka Topics

1. Create a topic for the raw medical entries:
   ```bash
   bin\windows\kafka-topics.bat --create --topic medical-entries --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

2. Create a topic for the processed data (illness and medicine):
   ```bash
   bin\windows\kafka-topics.bat --create --topic processed-entries --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

### Step 2: Producer - Generate and Push Medical Entries

1. Write a Python script to read a CSV file containing medical data and publish the entries to Kafka.
   
   Example CSV format:
   ```csv
   patient_id,medical_entry,timestamp
   1,"Patient shows signs of flu. Prescribed ibuprofen.",2024-01-01 12:00
   ```

   Example Producer Code:
   ```python
   from kafka import KafkaProducer
   import csv

   producer = KafkaProducer(bootstrap_servers='localhost:9092')

   with open('medical_data.csv', 'r') as file:
       reader = csv.reader(file)
       for row in reader:
           producer.send('medical-entries', value=','.join(row).encode('utf-8'))
   ```

### Step 3: Consumer - Extract Illness and Medicine

1. Write a Python consumer that applies heuristics to extract illness and medicine information from the Kafka topic.

   Example Consumer Code:
   ```python
   from kafka import KafkaConsumer, KafkaProducer
   import re

   consumer = KafkaConsumer('medical-entries', bootstrap_servers='localhost:9092')
   producer = KafkaProducer(bootstrap_servers='localhost:9092')

   for message in consumer:
       medical_entry = message.value.decode('utf-8')
       illness = re.search(r'signs of (\w+)', medical_entry).group(1)
       medicine = re.search(r'Prescribed (\w+)', medical_entry).group(1)
       processed_entry = f"Illness: {illness}, Medicine: {medicine}"
       producer.send('processed-entries', value=processed_entry.encode('utf-8'))
   ```

### Step 4: Load Processed Data into MongoDB

1. Set up **Kafka Connect** with the **MongoDB Sink Connector** to automatically consume the `processed-entries` Kafka topic and insert the records into a MongoDB collection.
   
   MongoDB Sink Configuration Example:
   ```json
   {
     "name": "mongo-sink-connector",
     "config": {
       "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
       "tasks.max": "1",
       "topics": "processed-entries",
       "connection.uri": "mongodb://localhost:27017",
       "database": "medical",
       "collection": "processed_entries",
       "key.converter": "org.apache.kafka.connect.storage.StringConverter",
       "value.converter": "org.apache.kafka.connect.storage.StringConverter"
     }
   }
   ```

### Step 5: Error Handling and Logging

- Set up a **Dead Letter Queue (DLQ)** to capture any failed messages. You can create another Kafka topic (`dlq-topic`) to route failed messages.
- Implement logging using Python’s `logging` module to track the status of producer/consumer operations.

### Running the Project on Google Cloud

1. **Kafka Alternative**: Deploy Kafka on **Google Kubernetes Engine (GKE)** or use **Google Cloud Pub/Sub** as an alternative to Kafka.
2. **MongoDB on Cloud**: Use **MongoDB Atlas** for cloud MongoDB hosting.
3. **Monitoring**: Integrate **Google Cloud Monitoring** for real-time insights on your pipeline’s performance and health.
4. **Scaling**: Utilize **autoscaling** in GKE for scaling your pipeline based on demand.

## Future Enhancements

- **Schema Management**: Use Avro or Protobuf for message serialization and schema enforcement.
- **Natural Language Processing (NLP)**: Improve illness and medicine extraction with more advanced NLP techniques or use pre-trained models.
- **Batch Processing**: Incorporate batch processing using Apache Spark or Google Dataproc for larger datasets.
- **Cloud Storage**: Store raw medical entries in **Google Cloud Storage** for backup and further batch analysis.

## Conclusion

This project is designed to demonstrate key data engineering concepts, including real-time streaming with Kafka, heuristic-based data processing, and integration with MongoDB. By running this both locally and on Google Cloud, you will gain experience in building scalable, cloud-ready data pipelines.
