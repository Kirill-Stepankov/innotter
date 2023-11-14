from kafka import KafkaProducer


# env vars
class KafkaProducerWrapper:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers="kafka:9093",
            value_serializer=lambda v: str(v).encode("utf-8"),
        )

    def produce_message(self, topic, message):
        self.producer.send(topic, value=message)


kafka_producer = KafkaProducerWrapper()
