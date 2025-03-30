from confluent_kafka import Producer
import logging

class KafkaProducer:
    def __init__(self, host: str, port: int, topic: str):
        # Configuration du producteur Kafka
        self.logger = logging.getLogger(__name__)
        self.producer = Producer({
            'bootstrap.servers': f'{host}:{port}'
        })
        self.topic = topic
        self.logger.debug(f"KafkaProducer initialisé pour le topic {self.topic} sur {host}:{port}")

    def delivery_report(self, err, msg):
        """ Callback appelé à la livraison du message """
        if err is not None:
            self.logger.error(f"Échec de la livraison du message: {err}")
        else:
            self.logger.debug(f"Message livré à {msg.topic()} [{msg.partition()}]")

    def send_message(self, message: str):
        """ Méthode pour envoyer un message à Kafka """
        self.producer.produce(self.topic, message, callback=self.delivery_report)
        self.producer.flush()  # S'assure que le message est envoyé
