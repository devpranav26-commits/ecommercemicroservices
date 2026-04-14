from kafka import KafkaConsumer
import json
import logging

# Logging
logging.basicConfig(level=logging.INFO)

# Kafka Consumer
consumer = KafkaConsumer(
    'cart-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='product-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def start_consumer():
    logging.info("🔥 Kafka Consumer Started...")

    for message in consumer:
        event = message.value

        logging.info(f"📥 Event Received: {event}")