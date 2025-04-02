import os
import json
import logging
from datetime import datetime

class JsonMerger:
    def __init__(self, producer):
        self.producer = producer
        self.cache = {}

    def merge_json(self, uuid, new_data):
        """ Fusionne les JSON lorsque les deux parties sont reçues et les enregistre """
        # Si le message existe déjà dans le cache, on fusionne les données
        print(f"UUID reçu par merge_json : {uuid}")
        if uuid in self.cache:
            print("UUID trouvé dans le cache : il va le merger")
            existing_data = self.cache[uuid]

            # Fusionner les deux messages sans écraser
            existing_data.update(new_data)
            merged_data = existing_data
            print("Merge terminé")

            logging.info(f"Fusion réussie pour UUID {uuid}: {merged_data}")

            # Sauvegarder dans un fichier
            self.save_json_to_file(merged_data)

            # Envoyer le message fusionné à Kafka
            self.producer.send_message(json.dumps(merged_data))

            # Supprimer le message du cache
            del self.cache[uuid]
        else:
            # Si le message n'est pas dans le cache, on l'ajoute en attendant la seconde moitié
            self.cache[uuid] = new_data
            logging.info(f"Message ajouté au cache pour UUID {uuid}: {new_data}")

    def save_json_to_file(self, merged_data):
        """ Sauvegarde le JSON fusionné dans un fichier """
        try:
            # Récupère la valeur de 'FilePath' depuis merged_data
            file_path = merged_data.get("FilePath", "")
            if not file_path:
                logging.warning("Impossible de générer un fichier : FilePath manquant.")
                return

            # Extraire le nom du fichier à partir du 'FilePath' (en supprimant le chemin et l'extension)
            filename_without_extension = os.path.basename(file_path).rsplit('.', 1)[0]

            # Créer un timestamp au format mmjj_hhmm
            timestamp = datetime.now().strftime("%m%d_%H%M")

            # Construire le nom final du fichier
            output_filename = f"{timestamp}_{filename_without_extension}.json"

            # Utiliser OUTPUT_DIR pour définir le chemin de sauvegarde
            output_filepath = os.path.join("/home/aderemet/workspace/merged-files", output_filename)

            # Sauvegarder le fichier dans OUTPUT_DIR
            with open(output_filepath, "w", encoding="utf-8") as f:
                json.dump(merged_data, f, indent=4, ensure_ascii=False)

            logging.info(f"JSON fusionné sauvegardé dans {output_filepath}")
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde du fichier JSON : {e}")