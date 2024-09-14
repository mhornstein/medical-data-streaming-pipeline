import sys
from kafka_util import create_consumer, KafkaError
from medical_entity_recognition import extract_diseases

'''
This script sets up a Kafka consumer to read messages from the specified topic and process them.

Important Note: 
Kafka does not provide a built-in mechanism to prevent a consumer from starting if the topic does not exist. 
This script assumes that the topic intended to be consumed from already exists.
'''

BOOTSTARP_SERVERS = 'localhost:9092'
DEST_TOPIC = 'medical-entries'
CONSMER_GROUP_ID = 'medical-entries-group'

def listen_and_print(consumer):
    try:
        for message in consumer:
            data = message.value
            sentence_text = data['sentence_text']
            treatments = data['treatments']
            query_metadata = data['query_metadata']
            validation_data = query_metadata # TODO update protocol
            filtered_diseases = extract_diseases(sentence_text, validation_data)
            print(f"{sentence_text} | {treatments} | {query_metadata} | {filtered_diseases} \n")
    except KafkaError as e:
        print(f"Kafka error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    consumer = create_consumer(BOOTSTARP_SERVERS, CONSMER_GROUP_ID, DEST_TOPIC)
    listen_and_print(consumer)