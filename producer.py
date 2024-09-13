import os
import pandas as pd
import random
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import sys

'''
This Python script will:

1. Load the data from the CSV files into memory.
2. Randomly pick one line from a random CSV file every 10 seconds.
3. Send the sentence_text along with the source_id (the filename) to the Kafka topic.
'''

DATA_DIR = './data/'
BOOTSTARP_SERVERS = 'localhost:9092'
DEST_TOPIC = 'medical-entries'

def create_producer(bootstrap_servers):
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Kafka producer created successfully.")
        return producer
    except  KafkaError as e:
        print(f"Failed to create Kafka producer: {e}")
        sys.exit(1)

def load_data(data_dir):
    data = {}
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(data_dir, filename)
            file_identifier = filename.split('.')[0] # use only file name as the identifier
            try:
                df = pd.read_csv(filepath, usecols=['sentence_text']) # Use 'usecols' to grab only the relevant column
                data[file_identifier] = df
            except ValueError:
                print(f"Failed to read the last column from {filename}. Check the file and its format.")
                sys.exit(1)
    return data

def send_to_kafka(producer, topic, message):
    try:
        producer.send(topic, message)
        producer.flush()
        print(f"Sent: {message}")
    except KafkaError as e:
        print(f"Failed to send message to Kafka: {e}")
        sys.exit(1)

def simulate_data_production(producer, topic, data):
    while True:
        file_identifier = random.choice(list(data.keys()))
        entry = data[file_identifier].sample()

        message = {
            'source_id': file_identifier,
            'sentence_text': entry['sentence_text'].values[0]
        }

        send_to_kafka(producer, topic, message)

        time.sleep(10) # Wait for 10 seconds before sending the next entry as part of the simulation

if __name__ == "__main__":
    data = load_data(DATA_DIR)
    producer = create_producer(BOOTSTARP_SERVERS)
    simulate_data_production(producer, DEST_TOPIC, data)
