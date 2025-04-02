import logging
import csv
import json
import os
import shutil

logger = logging.getLogger(__name__)

def json_to_csv(json_string):

    # Convertir la chaîne JSON en objet Python
    data = json.loads(json_string)

    # Créer un dossier principal pour le CSV et le sous-dossier 'data'
    output_dir = '/tmp/output_folder'
    data_dir = os.path.join(output_dir, 'data')

    # Vérifier si le dossier principal existe, sinon le créer
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Vérifier si le sous-dossier 'data' existe, sinon le créer
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Ouvrir un fichier CSV pour écrire les données
    csv_file_path = os.path.join(output_dir, 'fichier.csv')
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Clef_Document', 'Chemin_Document', 'Contenu_Document', 'Vignette_Document', 'Resume_Document', 'Loc_Appellation', 'Org_Appellation', 'Personne_Appellation']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()  # Écrire les en-têtes

        # Parcourir chaque entrée dans le JSON
        for item in data:
            file_path = item['FilePath']
            summary = item['Summary']

            # On commence par écrire une ligne avec FilePath et Summary
            header_row = {
                'Clef_Document': csv_file_path,
                'Chemin_Document': file_path,
                'Contenu_Document': file_path,
                'Vignette_Document': file_path,
                'Resume_Document': summary,
                'Loc_Appellation': None,
                'Org_Appellation': None,
                'Personne_Appellation': None

            }
            writer.writerow(header_row)  # Écrire la ligne d'en-tête pour cet enregistrement

            # Traiter les éléments NER
            for ner in item['NER']:
                row = {
                    'Clef_Document': csv_file_path,  # Utiliser le même ID pour toutes les lignes liées
                    'Chemin_Document': None,  # Ne pas répéter FilePath et Summary
                    'Contenu_Document': None,  # Ne pas répéter FilePath et Summary
                    'Vignette_Document': None,  # Ne pas répéter FilePath et Summary
                    'Resume_Document': None,
                    'Loc_Appellation': None,
                    'Org_Appellation': None,
                    'Personne_Appellation': None
                }

                # Vérifier le type dans NER et mapper 'Valeur' dans la colonne appropriée
                if ner['Type'] == 'Personne':
                    row['Personne_Appellation'] = ner['Valeur']
                elif ner['Type'] == 'Organisation':
                    row['Org_Appellation'] = ner['Valeur']
                elif ner['Type'] == 'Localisation':
                    row['Loc_Appellation'] = ner['Valeur']

                # Écrire la ligne NER dans le CSV
                writer.writerow(row)

    # Copier les fichiers de 'FilePath' vers le dossier 'data'
    for item in data:
        file_path = item['FilePath']

        # Extraire le nom du fichier (par exemple 'mon_document.txt')
        file_name = os.path.basename(file_path)

        # Définir le chemin de destination dans 'data'
        file_in_data_path = os.path.join(data_dir, file_name)

        # Vérifier si le fichier source existe avant de le copier
        if os.path.exists(file_path):
            # Copier le fichier dans le dossier 'data'
            shutil.copy(file_path, file_in_data_path)
            print(f"Le fichier '{file_name}' a été copié dans '{file_in_data_path}'.")
        else:
            print(f"Le fichier '{file_path}' n'existe pas. Impossible de le copier.")


    return ""