import json
import logging
import os
import sys

from dotenv import load_dotenv  # Import de load_dotenv

from kafka.kafka_consumer import KafkaConsumer
from kafka.kafka_producer import KafkaProducer
from utils.utils import json_to_csv

load_dotenv()  # Charge les variables d'environnement depuis le fichier .env

# Variables d'environnement
KAFKA_HOST = os.environ.get('KAFKA_HOST')
KAFKA_PORT = os.environ.get('KAFKA_PORT')
KAFKA_CONSUMER_TOPIC = os.environ.get('KAFKA_CONSUMER_TOPIC')
KAFKA_PRODUCER_TOPIC = os.environ.get('KAFKA_PRODUCER_TOPIC')
KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID', 'my-consumer-group')
KAFKA_AUTO_OFFSET_RESET = os.environ.get('KAFKA_AUTO_OFFSET_RESET', 'earliest')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

# Vérification si toutes les variables sont définies
if not all([KAFKA_HOST, KAFKA_PORT, KAFKA_CONSUMER_TOPIC, KAFKA_PRODUCER_TOPIC]):
    print("Erreur : Une ou plusieurs variables d'environnement sont manquantes.")
    print("Assurez-vous que les variables suivantes soient définies :")
    print("KAFKA_HOST, KAFKA_PORT, KAFKA_CONSUMER_TOPIC, KAFKA_PRODUCER_TOPIC")
    sys.exit(1)  # Arrêt du programme avec code d'erreur

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=LOG_LEVEL,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Messages mockés à envoyer
mocked_message = '''
    {"FilePath":"/home/lgaulier/Documents/test.txt",
    "Summary":"resume",
    "NER":[
            {
            "Type":"Personne",
            "Valeur":"toto",
            "Position":[7,52,27]
            },
            {
            "Type":"Personne",
            "Valeur":"toto",
            "Position":[7,52,27],
            "MGRS":"4QFJ 12345 67890"
            }
        ]
}'''


def push_mocked_messages(producer: KafkaProducer):
    """ Envoie des messages mockés dans le topic Kafka """
    logger.info("Envoi des messages mockés au topic Kafka.")
    producer.send_message(mocked_message)


def consume_and_transform(consumer: KafkaConsumer, producer: KafkaProducer):
    """ Consomme les messages, les transforme et les renvoie dans un autre topic """
    logger.info("Démarrage de la consommation des messages et de la transformation.")
    try:
        while True:
            message = consumer.read_message()
            if message:
                json_to_csv(message)
                logger.info(f"csv créé")
    except KeyboardInterrupt:
        logger.info("Surveillance du consumer arrêtée par l'utilisateur.")
    finally:
        consumer.close()


if __name__ == "__main__":
    # Initialisation des producteurs et consommateurs Kafka
    producer_for_mocked = KafkaProducer(KAFKA_HOST, KAFKA_PORT, KAFKA_CONSUMER_TOPIC)
    producer_for_transformed = KafkaProducer(KAFKA_HOST, KAFKA_PORT, KAFKA_PRODUCER_TOPIC)
    consumer = KafkaConsumer(KAFKA_HOST, KAFKA_PORT, KAFKA_GROUP_ID, KAFKA_AUTO_OFFSET_RESET, KAFKA_CONSUMER_TOPIC)

    # Étape 1 : Pousser des messages mockés dans KAFKA_CONSUMER_TOPIC
    #push_mocked_messages(producer_for_mocked)

    # Étape 2 : Consommer les messages du topic KAFKA_CONSUMER_TOPIC, transformer et renvoyer
    consume_and_transform(consumer, producer_for_transformed)
