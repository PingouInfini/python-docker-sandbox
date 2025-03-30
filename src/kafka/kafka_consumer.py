from confluent_kafka import Consumer, KafkaException, KafkaError
import logging

class KafkaConsumer:
    def __init__(self, host: str, port: int, group_id: str, auto_offset_reset: str, topic: str):
        # Configuration du consommateur Kafka
        self.logger = logging.getLogger(__name__)
        self.consumer = Consumer({
            'bootstrap.servers': f'{host}:{port}',
            'group.id': group_id,
            'auto.offset.reset': auto_offset_reset
        })
        self.topic = topic
        self.consumer.subscribe([self.topic])
        self.logger.debug(f"KafkaConsumer initialisé pour le topic {self.topic} sur {host}:{port} avec le group-id {group_id}")

    def read_message(self, timeout: float = 1.0):
        """ Méthode pour lire un message depuis Kafka """
        try:
            msg = self.consumer.poll(timeout)
            if msg is None:
                self.logger.debug("Aucun message reçu dans le délai imparti.")
                return None
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    self.logger.warning(f"Fin de la partition : {msg.topic()} [{msg.partition()}] : {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                self.logger.info(f"Message reçu depuis {self.topic} : {msg.value().decode('utf-8')}")
                return msg.value().decode('utf-8')
        except KafkaException as e:
            self.logger.error(f"Erreur lors de la lecture du message : {e}")
            return None

    def close(self):
        """ Ferme le consommateur """
        self.logger.info("Fermeture du KafkaConsumer.")
        self.consumer.close()