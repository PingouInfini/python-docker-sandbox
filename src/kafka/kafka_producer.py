from confluent_kafka import Producer
import logging
import json
import os

# Activer/Désactiver le mock
MOCK_KAFKA = os.getenv("MOCK_KAFKA", "True").lower() == "false"

class KafkaProducer:
    def __init__(self, host: str, port: int, topic: str):
        self.logger = logging.getLogger(__name__)
        self.topic = topic

        if MOCK_KAFKA:
            self.logger.warning(f"Mode MOCK activé : KafkaProducer va afficher les messages au lieu de les envoyer !")
        else:
            self.producer = Producer({'bootstrap.servers': f'{host}:{port}'})
            self.logger.debug(f"KafkaProducer initialisé pour le topic {self.topic} sur {host}:{port}")

    def delivery_report(self, err, msg):
        """ Callback appelée à la livraison du message """
        if err is not None:
            self.logger.error(f"Échec de la livraison du message: {err}")
        else:
            self.logger.debug(f"Message livré à {msg.topic()} [{msg.partition()}]")

    def send_message(self, message: str):
        """ Méthode pour envoyer un message à Kafka """
        if MOCK_KAFKA:
            print(f"[MOCK PRODUCER] Message envoyé sur {self.topic}: {json.dumps(message, indent=2)}")
        else:
            self.producer.produce(self.topic, json.dumps(message), callback=self.delivery_report)
            self.producer.flush()  # S'assure que le message est envoyé
