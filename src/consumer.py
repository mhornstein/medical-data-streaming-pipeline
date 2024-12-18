from kafka_util import create_consumer, create_producer, send_to_kafka, load_schema
from medical_entity_recognition import extract_diseases
import itertools
from util import config

'''
This script sets up a Kafka consumer to read messages from the specified topic and process them.

Important Note: 
Kafka does not provide a built-in mechanism to prevent a consumer from starting if the topic does not exist. 
This script assumes that the topic intended to be consumed from already exists.
'''

def create_message(disease, treatment):
    return {
        'disease': disease,
        'treatment': treatment
    }

def listen_and_process(consumer, producer, dest_topic):
    while True:
        try:
            msg = consumer.poll(timeout=None)

        except Exception as e:
            print(f"Message deserialization failed for {msg}: {e}")
            break

        if msg is None:
            print('Message None')
            continue

        if msg.error():
            print(f"AvroConsumer error: {msg.error}")
            continue

        data = msg.value()
        sentence_text = data['sentence_text']
        treatments = data['treatments']
        query_metadata = data['query_metadata']
        validation_data = query_metadata # TODO update protocol
        filtered_diseases = extract_diseases(sentence_text, validation_data)
        print(f"{sentence_text} | {treatments} | {query_metadata} | {filtered_diseases} \n")
        for disease, treatment in itertools.product(filtered_diseases, treatments):
            message = create_message(disease, treatment)
            send_to_kafka(producer, dest_topic, message)

if __name__ == "__main__":
    bootstrap_servers = config['bootstrap_servers']
    source_topic = config['source_topic']
    dest_topic = config['dest_topic']
    consumer_group_id = config['consumer_group_id']
    schema_registry_url = config['schema_registry_url']
    dest_topic_schemea_path = config['dest_topic_schemea_path']

    consumer = create_consumer(bootstrap_servers, consumer_group_id, source_topic, schema_registry_url)

    dest_value_schema = load_schema(dest_topic_schemea_path)
    producer = create_producer(bootstrap_servers, schema_registry_url, dest_value_schema)

    listen_and_process(consumer, producer, dest_topic)