from kafka import KafkaProducer
import json
import sys
from kafka.errors import KafkaError
from kafka import KafkaConsumer

def create_consumer(bootstrap_servers, consumer_group_id, source_topic):
    try:
        consumer = KafkaConsumer(
            source_topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest', # Start from the earliest message
            enable_auto_commit=True,
            group_id=consumer_group_id, # unique identifier that allows multiple consumers to work together to read from the same Kafka topic, while ensuring that each partition of the topic is consumed by only one consumer in the group.
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        print("Kafka consumer created successfully.")
        return consumer
    except KafkaError as e:
        print(f"Failed to connect to Kafka server: {e}")
        sys.exit(1)

def create_producer(bootstrap_servers):
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Kafka producer created successfully.")
        return producer
    except KafkaError as e:
        print(f"Failed to create Kafka producer: {e}")
        sys.exit(1)

def send_to_kafka(producer, topic, message):
    try:
        producer.send(topic, message)
        producer.flush()
        print(f"Sent: {message}")
    except KafkaError as e:
        print(f"Failed to send message to Kafka: {e}")
        sys.exit(1)