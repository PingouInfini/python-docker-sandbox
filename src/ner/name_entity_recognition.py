import logging
import unittest

import spacy
from langdetect import detect
from spacy import Language


# Texte d'article pour tester
# article = open("article_test_ner.txt", "r").read()


def get_model_for_language(text: str) -> Language:
    """"Récupère le modèle adapté à la langue du texte"""
    # Détecter la langue
    language = detect(text)
    logging.info(f"Langue détectée : {language}")

    # Charger le modèle en fonction de la langue détectée
    if language == "fr":
        nlp = spacy.load("fr_core_news_lg")
    elif language == "en":
        nlp = spacy.load("en_core_web_sm")
    else:
        # nlp = spacy.load("en_core_web_sm")
        nlp = spacy.load("fr_core_news_lg")
        logging.warning("Langue non reconnue. Utilisation de la langue par défaut (fr)")
        # raise ValueError("Langue non prise en charge : uniquement le français (fr) et l'anglais (en)")
    return nlp


def ner_on_text(text: str, nlp: Language):
    # Traiter le texte avec le modèle
    doc = nlp(text)

    # Affiche les entités trouvées
    ner = {}
    for ent in doc.ents:
        logging.debug("Entitée détectée : %s | %s | %s", ent.text, ent.label_, ent.start_char)
        if not ent.text in ner:
            ner[ent.text] = {"name": ent.text, "type": ent.label_, "position": [ent.start_char]}
        else:
            ner[ent.text]["position"].append(ent.start_char)

    logging.debug("Entitées trouvées :", ner)
    return ner


class Test(unittest.TestCase):
    def test_ner(self):
        text = "Isabelle a les yeux bleus"
        nlp = spacy.load("fr_core_news_md")
        result = ner_on_text(text, nlp)
        expected_result = {"Isabelle": {"name": "Isabelle", "type": "PER", "position": [0]}}
        self.assertEqual(expected_result, result)

    def detect_language(self, text: str, language_module: str):
        nlp = spacy.load(language_module)
        nlp_test = get_model_for_language(text)
        self.assertEqual(nlp.lang, nlp_test.lang)

    def test_detect_french(self):
        text = "Salut la Team! Vous m'avez manqué!"
        module = "fr_core_news_md"
        self.detect_language(text, module)

    def test_detect_english(self):
        text = "Hello world"
        module = "en_core_web_sm"
        self.detect_language(text, module)
