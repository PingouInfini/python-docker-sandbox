import json
import logging
import os
import sys

from dotenv import load_dotenv  # Import de load_dotenv

from kafka.kafka_consumer import KafkaConsumer
from kafka.kafka_producer import KafkaProducer
from summarization.summarizeWithNltk  import *
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

texte1 = """Bella, une lycéenne de dix-sept ans, décide de quitter sa mère et la ville de Phoenix pour vivre à Forks, un village de l'État de Washington où vit son père. Elle n'est pas proche de ce dernier, qu'elle ne voit habituellement que deux semaines par an, et hait la ville de Forks, mais souhaite laisser sa mère vivre seule avec son nouveau compagnon, Phil[T 1]. Ce dernier est joueur de baseball professionnel et voyage donc beaucoup : Bella tient à la laisser le suivre sans obstacle[T 2]. Des le lendemain de son arrivée, elle se rend dans le lycée de la ville[T 3]. Le midi, à la cantine, elle rencontre la famille Cullen, elle est fascinée par leur pâleur, leurs yeux sombres et leurs cernes marqués[T 4]. En cours de biologie, elle s'assoit à côté d'Edward, ce dernier la traite avec hostilité et colère, refusant de lui adresser la parole[T 5]. Après une semaine d'absence, il revient cependant, se montrant très poli et faisant comme si cette première rencontre n'avait pas eu lieu[T 6].

Un jour de neige, elle a un accident sur le parking du lycée : un étudiant, Tyler, perd le contrôle de son fourgon et lui fonce dessus. Edward, qui se tient à quatre voitures d'elle, se retrouve soudain à ses côtés et arrête l'impact de la voiture à mains nues[T 7]. Un bal du printemps est ensuite organisé : elle refuse trois invitations sous prétexte d'une visite à Jacksonville prévue. Edward propose alors de l'y emmener et elle accepte[T 8]. Lors d'une visite à la plage de la réserve quileute de La Push, Bella rencontre Jacob Black et Sam, un jeune homme qui laisse entendre que les Cullen ne sont pas les bienvenus à la réserve[T 9]. Bella demande des détails à Jacob, qui lui parle des légendes quileutes et mentionne en particulier les Sang-froid. Il raconte que l'arrière-grand-père de Jacob Black aurait lui-même négocié l'accord bannissant les vampires, ou Sang-froid, des terres quileutes. Ces vampires ne s'attaquent pas aux humains : l'aïeul Black conclut donc un traité avec eux, s'engageant à ne pas les chasser tant qu'ils ne s'aventurent pas sur les terres de la réserve. Jacob révèle alors que ces vampires sont la famille Cullen, et en particulier que Carlisle n'a pas changé depuis cette époque[T 10].

Bella fait alors des recherches sur Internet sur le thème des vampires, et se convainc qu'Edward pourrait en être un[T 11]. Jessica, Angela et Lauren comptent acheter leurs robes de bal à Port Angeles et invitent Bella à les rejoindre, bien qu'elle n'ait pas l'intention de se rendre à la soirée[T 12]. Angela lui révèle alors que la famille Cullen ne se rend jamais au lycée les jours de soleil : « au premier rayon de soleil, ils partent en randonnée[T 13] ». Bella se sépare alors des autres filles pour chercher une librairie où elle peut se renseigner sur les vampires, mais ne trouve aucun magasin satisfaisant. Elle se perd alors en ville, se retrouvant dans une rue désaffectée où quatre hommes commencent à la harceler[T 14]. Edward arrive soudain à la rescousse, la prenant dans sa voiture et la conduisant à l'abri[T 15]. Après avoir rassuré ses amies, il l'emmène dîner au restaurant La Bella Italia[T 16]. Elle lui annonce alors qu'elle pense qu'il lit dans les pensées, ce qu'il lui confirme[T 17]. Il lui confirme ensuite que les Cullen sont des vampires[T 18]. Le soir, de retour chez son père, Bella résume la situation :

    « J'étais à peu près certaine de trois choses. Un, Edward était un vampire ; deux, une part de lui - dont j'ignorais la puissance - désirait s'abreuver de mon sang ; et trois, j'étais follement et irrévocablement amoureuse de lui. »

— Fascination, chapitre 9.[T 19]

Bella découvre alors que seule Alice Cullen soutient Edward, tandis que tous les autres enfants Cullen s'opposent à son attirance pour une humaine, estimant que la relation est dangereuse et qu'il nuirait trop à la famille s'il devait céder à ses instincts et la tuer[T 20]. Carlisle se range finalement du côté d'Edward, tandis qu'Esmé refuse de prendre parti[T 21]. Bella annule ensuite sa journée prévue à Seattle, à la demande d'Edward qui veut lui montrer ce que le soleil fait réellement aux vampires[T 22]. Elle découvre alors que la peau des vampires brille au soleil, et Edward lui déclare ses sentiments[T 23]. Edward invite ensuite Bella à rencontrer sa famille au domicile des Cullen[T 24]. Or, Alice a une vision d’un groupe de vampires nomades en voyage, passant par Forks : Edward veut alors absolument protéger Bella[T 25].

Pendant sa visite au domicile des Cullen, Bella est invitée à les rejoindre à un match de base-ball familial, Alice ayant prévu une tempête : les matches ne peuvent s'organiser que s'il y a du tonnerre pour couvrir le bruit du jeu[T 26]. Le clan de vampire nomades arrive cependant plus tôt que prévu, pendant la partie. Il est composé de trois personnes, James, Victoria et Laurent. Le chef est James, un vampire aux traits quelconques et aux cheveux châtains ; Victoria est sa compagne et Laurent les a rejoints récemment. Laurent s'intéresse au mode de vie végétarien et est cordial envers les Cullen ; or, un coup de vent trahit la nature de Bella et attire l'attention de James, qui décide de la traquer pour la dévorer[T 27].

Les Cullen se préparent immédiatement à faire fuir Bella : elle quitte son père en l'insultant pour qu'il ne tente pas de la suivre, puis s'enfuit à Phoenix, près de chez sa mère qui est en déplacement en Floride avec Phil[T 28]. Elle est accompagnée d'Alice et Jasper. James appelle Bella, lui faisant croire qu'il tient sa mère en otage, et lui ordonne de le rejoindre dans un studio de danse de son enfance[T 29]. Bella parvient à fuir Alice et Jasper à l'aéroport où ils attendent l'arrivée Edward et se rend immédiatement au studio de danse où James lui a donné rendez-vous [T 30]. Elle découvre alors que James ne tient pas sa mère otage : il a juste fouillé la maison et pris une vidéo d'enfance où elle appelait Bella d'un ton inquiet[T 31].

James lui raconte alors la transformation d'Alice, puis lui casse la jambe et elle perd connaissance[T 32]. Edward et ses frères arrivent à temps pour tuer James, mais se rendent compte que Bella a été mordue à la main. Carlisle ordonne alors à Edward d'aspirer le sang de Bella jusqu'à en retirer tout le venin, ce qu'il parvient à faire[T 33].

Elle se réveille à l'hôpital plusieurs jours plus tard, aux côtés de sa mère et d'Edward. Les Cullen font croire à Renée qu'elle est tombée dans l'escalier de l'hôtel[T 34]. Renée lui annonce alors que Phil a été engagé à Jacksonville à long terme, et qu'ils ont acheté une maison dans laquelle Bella pourra avoir sa chambre, mais cette dernière annonce vouloir revenir à Forks. Edward et Bella discutent ensuite de la transformation en vampire : elle lui reproche de l'avoir sauvée, tandis qu'il refuse catégoriquement de la transformer[T 35].

Dans l'épilogue, Bella et Edward se rendent au bal de fin d'année. Bella est très en colère : elle avait refusé de s'y rendre et, tenue dans l'ignorance par les Cullen, croyait à une cérémonie de transformation en vampire[T 36]. Au bal, Jacob Black lui envoie un avertissement de la part de son père : Billy Black lui fait dire de quitter Edward, et que les Quileutes ne relâcheront pas leur garde. Bella ignore l'avertissement[T 37]. """

# Messages mockés à envoyer
mocked_messages = [
    {"uuid": "f1953fb1-c80c-46d4-af44-e5512967436f",
     "poids": 37250,"text": texte1}
]



def push_mocked_messages(producer: KafkaProducer):
    """ Envoie des messages mockés dans le topic Kafka """
    logger.info("Envoi des messages mockés au topic Kafka.")
    for message in mocked_messages:
        producer.send_message(json.dumps(message))


def consume_and_transform(consumer: KafkaConsumer, producer: KafkaProducer):
    """ Consomme les messages, les transforme et les renvoie dans un autre topic """
    logger.info("Démarrage de la consommation des messages et de la transformation.")
    try:
        while True:
            message = consumer.read_message()
            if message:
                message_json = json.loads(message)
                transformed_message = summarize(message_json.get("text", "erreur lors de la génération du résumé"), max_chars=4000)
                enriched_message = {"uuid": message_json.get("uuid", ""), "FilePath": message_json.get("FilePath",""),"summary": transformed_message}
                producer.send_message(json.dumps(enriched_message))  # Envoie du message transformé dans le topic TextToNer
                logger.info("Message envoyé :" + str(enriched_message))
    except KeyboardInterrupt:
        logger.info("Surveillance du consumer arrêtée par l'utilisateur.")
    finally:
        consumer.close()


if __name__ == "__main__":
    # Initialisation des producteurs et consommateurs Kafka
    #producer_for_mocked = KafkaProducer(KAFKA_HOST, KAFKA_PORT, KAFKA_CONSUMER_TOPIC)
    producer_for_transformed = KafkaProducer(KAFKA_HOST, KAFKA_PORT, KAFKA_PRODUCER_TOPIC)
    consumer = KafkaConsumer(KAFKA_HOST, KAFKA_PORT, KAFKA_GROUP_ID, KAFKA_AUTO_OFFSET_RESET, KAFKA_CONSUMER_TOPIC)

    # Étape 1 : Pousser des messages mockés dans KAFKA_CONSUMER_TOPIC
    #push_mocked_messages(producer_for_mocked)

    # Étape 2 : Consommer les messages du topic KAFKA_CONSUMER_TOPIC, transformer et renvoyer
    consume_and_transform(consumer, producer_for_transformed)
