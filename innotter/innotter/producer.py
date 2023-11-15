import json

from kafka import KafkaProducer

from .settings import env


class KafkaProducerWrapper:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=env("KAFKA_BOOTSTRAP_SERVERS"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def produce_message(self, topic, message):
        self.producer.send(topic, value=message)


kafka_producer = None
if not int(env("TESTING")):
    kafka_producer = KafkaProducerWrapper()
