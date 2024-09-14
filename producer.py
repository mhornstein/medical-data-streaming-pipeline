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
METADATA_FILE = './metadata/query_metadata.csv'
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
                df = pd.read_csv(filepath, usecols=['sentence_id', 'sentence_text', 'treatment']) # Use 'usecols' to grab only the relevant column
                df = df.set_index('sentence_id')
                data[file_identifier] = df
            except ValueError:
                print(f"Failed to read the last column from {filename}. Check the file and its format.")
                sys.exit(1)
    return data

def load_query_metadata(metadata_file):
    query_metadata = pd.read_csv(metadata_file, dtype={'query_index': str}).set_index('query_index')
    query_metadata_dict = query_metadata.T.to_dict()
    return query_metadata_dict

def send_to_kafka(producer, topic, message):
    try:
        producer.send(topic, message)
        producer.flush()
        print(f"Sent: {message}")
    except KafkaError as e:
        print(f"Failed to send message to Kafka: {e}")
        sys.exit(1)


def create_message(entry, query_metadata):
    sentence_text = entry['sentence_text'].iloc[0]
    treatments = entry['treatment'].tolist()

    message = {
        'sentence_text': sentence_text,
        'treatments': treatments,
        'query_metadata': query_metadata
    }

    return message

def sample_entry(data, file_identifier):
    df = data[file_identifier]
    sampled_index = df.sample().index[0]
    entry = df.loc[[sampled_index]]
    return entry


def simulate_data_production(producer, topic, metadata_dict, data):
    while True:
        file_identifier = random.choice(list(data.keys()))
        entry = sample_entry(data, file_identifier)
        query_metadata = metadata_dict[file_identifier]

        message = create_message(entry, query_metadata)
        
        send_to_kafka(producer, topic, message)

        time.sleep(10) # Wait for 10 seconds before sending the next entry as part of the simulation

if __name__ == "__main__":
    data = load_data(DATA_DIR)
    metadata_dict = load_query_metadata(METADATA_FILE)
    producer = create_producer(BOOTSTARP_SERVERS)
    simulate_data_production(producer, DEST_TOPIC, metadata_dict, data)
