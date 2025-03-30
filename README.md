# python-docker-sandbox

Ce projet implémente un producteur et un consommateur Kafka en Python, avec transformation de messages. Le producteur envoie des messages mockés dans un premier topic Kafka, le consommateur lit ces messages, applique une transformation sur les voyelles et envoie le résultat dans un autre topic.

## Table des matières

1. [Pré-requis](#pré-requis)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Structure du Projet](#structure-du-projet)
6. [Démarrage du Projet](#démarrage-du-projet)
7. [Fonctionnalités](#fonctionnalités)

---

## Pré-requis

Avant de commencer, assurez-vous d'avoir installé :

- Docker et Docker Compose
- Python 3.12+ et ```pip```
- Kafka (via Docker)
- Zookeeper (via Docker)

## Installation

1. Clonez le projet depuis GitHub :

   ```
   git clone https://github.com/PingouInfini/python-docker-sandbox.git
   cd python-docker-sandbox
   ```

2. Créez et démarrez la stack Kafka/Zookeeper avec Docker :

   ```
   docker-compose up -d
   ```

3. Installez les dépendances Python dans un environnement virtuel :

   ```
   python3 -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Configuration

Les configurations du projet sont gérées via des variables d'environnement. Les principales variables sont :

- `KAFKA_HOST`: L'adresse IP ou le nom d'hôte de Kafka (par défaut : `192.168.100.100`)
- `KAFKA_PORT`: Le port Kafka (par défaut : `9093`)
- `KAFKA_CONSUMER_TOPIC`: Le topic où le consommateur lit les messages (par défaut : `docsToText`)
- `KAFKA_PRODUCER_TOPIC`: Le topic où le producteur envoie les messages transformés (par défaut : `TextToNer`)
- `KAFKA_GROUP_ID`: L'identifiant du groupe Kafka pour le consommateur (par défaut : `my-consumer-group`)
- `KAFKA_AUTO_OFFSET_RESET`: Le paramètre d'offset automatique pour Kafka (par défaut : `earliest`)
- `LOG_LEVEL`: Le niveau de log (par défaut : `INFO`, mais peut être `DEBUG`, `WARNING`, etc.)

Vous pouvez définir ces variables directement dans votre shell ou en utilisant un fichier `.env`.

### Exemple de fichier `.env`

```
KAFKA_HOST=192.168.100.100
KAFKA_PORT=9093
KAFKA_CONSUMER_TOPIC=docsToText
KAFKA_PRODUCER_TOPIC=TextToNer
KAFKA_GROUP_ID=my-consumer-group
KAFKA_AUTO_OFFSET_RESET=earliest
LOG_LEVEL=DEBUG
```

## Usage

### 1. Pousser des messages mockés dans Kafka

L'étape 1 envoie des messages mockés au topic Kafka spécifié par `KAFKA_CONSUMER_TOPIC`.

### 2. Lire les messages, les transformer, et les renvoyer

Le consommateur lit les messages du topic `KAFKA_CONSUMER_TOPIC`, transforme les voyelles en majuscules, puis envoie le résultat enrichi dans le topic `KAFKA_PRODUCER_TOPIC`.

### Commande de lancement

Lancez le programme avec la commande suivante :

```
python3 main.py
```

## Structure du Projet

```
python-docker-sandbox
│
├── docker/                        # Contient les fichiers de configuration Docker
│   ├── docker-compose.yml          # Configuration Docker Compose pour Kafka et Zookeeper
│   └── Dockerfile                  # Dockerfile pour la création de l'image Docker personnalisée
│
├── .env                            # Fichier de configuration des variables d'environnement
├── .gitignore                      # Fichier pour ignorer les fichiers/dossiers non désirés dans le repo
├── README.md                       # Documentation du projet
├── requirements.txt                # Fichier des dépendances Python
│
└── src/                            # Contient le code source du projet
    ├── kafka/                      # Dossier contenant les classes KafkaProducer et KafkaConsumer
    │   ├── kafka_consumer.py       # Classe pour la consommation des messages Kafka
    │   └── kafka_producer.py       # Classe pour la production des messages Kafka
    │
    ├── main.py                     # Point d'entrée principal du programme
    └── utils/                       # Dossier contenant des utilitaires partagés
        └── utils.py                # Fonctions utilitaires diverses
```

## Démarrage du Projet

1. Configurez les variables d'environnement dans un fichier `.env` (ou directement dans votre terminal).
2. Démarrez Kafka et Zookeeper via Docker Compose :

   ```
   docker-compose up -d
   ```

3. Lancez le script principal `main.py` :

   ```
   python3 main.py
   ```

## Fonctionnalités

- **KafkaProducer** : Envoi de messages à un topic Kafka.
- **KafkaConsumer** : Lecture de messages depuis un topic Kafka.
- **Transformation** : Transformation des voyelles des messages reçus en majuscules.
- **Logs** : Configuration des logs en fonction du niveau (INFO, DEBUG, etc.) défini dans les variables d'environnement.
