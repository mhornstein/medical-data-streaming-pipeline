import json
import sys
from kafka import KafkaConsumer
from kafka.errors import KafkaError

'''
This script sets up a Kafka consumer to read messages from the specified topic and process them.

Important Note: 
Kafka does not provide a built-in mechanism to prevent a consumer from starting if the topic does not exist. 
This script assumes that the topic intended to be consumed from already exists.
'''

BOOTSTARP_SERVERS = 'localhost:9092'
DEST_TOPIC = 'medical-entries'
CONSMER_GROUP_ID = 'medical-entries-group'

def create_consumer():
    try:
        consumer = KafkaConsumer(
            DEST_TOPIC,
            bootstrap_servers=BOOTSTARP_SERVERS,
            auto_offset_reset='earliest', # Start from the earliest message
            enable_auto_commit=True,
            group_id=CONSMER_GROUP_ID, # unique identifier that allows multiple consumers to work together to read from the same Kafka topic, while ensuring that each partition of the topic is consumed by only one consumer in the group.
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        print("Kafka consumer created successfully.")
        return consumer
    except KafkaError as e:
        print(f"Failed to connect to Kafka server: {e}")
        sys.exit(1)

def listen_and_print(consumer):
    try:
        for message in consumer:
            data = message.value
            sentence_text = data['sentence_text']
            treatments = data['treatments']
            query_metadata = data['query_metadata']
            print(f"{sentence_text} | {treatments} | {query_metadata}\n")
    except KafkaError as e:
        print(f"Kafka error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    consumer = create_consumer()
    listen_and_print(consumer)