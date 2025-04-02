import logging
import os
import sys
import json
import time

from dotenv import load_dotenv
from json_merger import JsonMerger
from mock_data import generate_mock_messages
from kafka.kafka_producer import KafkaProducer
from kafka.kafka_consumer import  KafkaConsumer

# === Chargement des variables d'environnement ===
load_dotenv()

KAFKA_HOST = os.environ.get('KAFKA_HOST')
KAFKA_PORT = os.environ.get('KAFKA_PORT')
KAFKA_CONSUMER_TOPIC_SUMMARIZE = os.environ.get('KAFKA_CONSUMER_TOPIC_SUMMARIZE')
KAFKA_CONSUMER_TOPIC_GAZETTEER = os.environ.get('KAFKA_CONSUMER_TOPIC_GAZETTEER')
KAFKA_PRODUCER_TOPIC = os.environ.get('KAFKA_PRODUCER_TOPIC')
KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID', 'my-consumer-group')
KAFKA_AUTO_OFFSET_RESET = os.environ.get('KAFKA_AUTO_OFFSET_RESET', 'earliest')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
OUTPUT_DIR = os.environ.get('OUTPUT_DIR')

# === Vérification des variables ===
if not all([KAFKA_HOST, KAFKA_PORT, KAFKA_CONSUMER_TOPIC_SUMMARIZE, KAFKA_CONSUMER_TOPIC_GAZETTEER, KAFKA_PRODUCER_TOPIC]):
    print("Erreur : Une ou plusieurs variables d'environnement sont manquantes.")
    sys.exit(1)

# === Configuration des logs ===
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=LOG_LEVEL,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# === Initialisation des Kafka Consumer/Producer ===
consumer_gazetteer = KafkaConsumer(KAFKA_HOST, KAFKA_PORT, KAFKA_GROUP_ID, KAFKA_AUTO_OFFSET_RESET, KAFKA_CONSUMER_TOPIC_GAZETTEER)
consumer_summarize = KafkaConsumer(KAFKA_HOST, KAFKA_PORT, KAFKA_GROUP_ID, KAFKA_AUTO_OFFSET_RESET, KAFKA_CONSUMER_TOPIC_SUMMARIZE)
producer = KafkaProducer(KAFKA_HOST, KAFKA_PORT, KAFKA_PRODUCER_TOPIC)


# === Envoi des messages mockés pour simuler les topics d'entrée ===
def send_mock_messages():
    """Envoi des messages simulés aux topics Kafka pour tester la fusion."""
    logger.info("Envoi des messages mockés aux topics Kafka.")

    msg_gazetteer, msg_summarize = generate_mock_messages()

    # Envoi des messages aux topics appropriés
    consumer_gazetteer.send_message(json.dumps(msg_gazetteer))  # Pour le topic Gazetteer
    consumer_summarize.send_message(json.dumps(msg_summarize))  # Pour le topic Summarize

    logger.info(f"Message Gazetteer envoyé : {msg_gazetteer}")
    logger.info(f"Message Summarize envoyé : {msg_summarize}")

# === Push les messages mockés dans le producer Kafka ===
def push_mock_messages(producer: KafkaProducer):
    """Push les messages mockés dans le topic producer Kafka """
    logger.info("Envoi des messages mockés au topic Kafka.")
    for message in generate_mock_messages():
        producer.send_message(json.dumps(message))

# === Démarrer le consumer Kafka qui va consommer les messages ===
def start_consumer():
    """Démarre le consommateur Kafka qui va fusionner les JSON et les envoyer dans un autre topic"""
    logger.info("Démarrage de la consommation des messages - envoi au JSON Merger...")
    merger = JsonMerger(KAFKA_HOST, KAFKA_PORT, producer)  # Passer le producer au merger
    merger.start()

# === Test de merge - peut être appelé seul depuis l'exe pour tester ===
def start_merge_test():
    """Teste la fusion des JSON et exporte le fichier fusionné"""
    logger.info("Test du JSON Merger...")

    msg_gazetteer, msg_summarize = generate_mock_messages()

    merger = JsonMerger(consumer_gazetteer, producer)

    # Fusionner les messages des deux listes
    for g_msg, s_msg in zip(msg_gazetteer, msg_summarize):
        # Fusionner les données de Gazetteer
        merger.merge_json(g_msg["uuid"], g_msg)

        # Fusionner les données de Summarize
        merger.merge_json(s_msg["uuid"], s_msg)

# === Exécution du programme ===
if __name__ == "__main__":
    start_merge_test()  # Pour tester la fusion
    # send_mock_messages()  # Pour envoyer les messages aux topics Kafka
    # start_consumer()  # Lancer le consommateur
