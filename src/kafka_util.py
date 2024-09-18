from confluent_kafka.avro import AvroProducer, AvroConsumer
import sys
from confluent_kafka import avro

def create_consumer(bootstrap_servers, consumer_group_id, source_topic, schema_registry_url):
    try:
        consumer = AvroConsumer(
            {
                'bootstrap.servers': bootstrap_servers,
                'group.id': consumer_group_id,
                'auto.offset.reset': 'earliest',
                'schema.registry.url': schema_registry_url
            },
        )

        consumer.subscribe([source_topic])

        print("Consumer created successfully.")
        return consumer
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        sys.exit(1)

def create_producer(bootstrap_servers, schema_registry_url, value_schema, key_schema=None):
    try:
        producer = AvroProducer(
            {'bootstrap.servers': bootstrap_servers,
            'schema.registry.url': schema_registry_url},
            default_value_schema=value_schema,
            default_key_schema=key_schema
        )
        print("Producer created successfully.")
        return producer
    except Exception as e:
        print(f"Failed to create producer: {e}")
        sys.exit(1)

def send_to_kafka(producer, topic, message, timeout=10):
    try:
        producer.produce(topic=topic, value=message)
        producer.flush(timeout=timeout)
        print(f"Sent: {message}")
    except Exception as e:
        print(f"Failed to send message to Kafka:\nMessage: {message}, Topic: {topic}, error: {e}")
        sys.exit(1)

def load_schema(schema_path):
    try:
        schema = avro.load(schema_path)
        return schema
    except Exception as e:
        print(f"Failed to load schema: {e}")
        sys.exit(1)