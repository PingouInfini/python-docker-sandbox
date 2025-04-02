import unittest

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
# model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")
camembert_ner = pipeline("ner", model=model, aggregation_strategy='simple', tokenizer=tokenizer)


# example = "A l’issue des discussions en Arabie saoudite, le président ukrainien Zelensky a dit que « l’Ukraine est prête pour la paix » et que Washington doit désormais « convaincre la Russie » d’accepter cette proposition. Les Etats-Unis ont également acté le retour de leur aide « en matière de sécurité » et de renseignements à Kiev."

def ner_on_text(text: str):
    ner = camembert_ner(text)

    ner_doubleless = {}
    for entity in ner:
        # Change le nom des attributs
        entity['position'] = entity.pop('start')
        entity['valeur'] = entity.pop('word')
        entity['type'] = entity.pop('entity_group')
        entity['score'] = float(entity.pop('score'))
        del entity['end']

        # Dédoublonnage
        if not entity['valeur'] in ner_doubleless:
            ner_doubleless[entity['valeur']] = entity
            ner_doubleless[entity['valeur']]["position"] = [entity["position"]]
            ner_doubleless[entity['valeur']]["score"] = [entity["score"]]
        else:
            ner_doubleless[entity['valeur']]["position"].append(entity['position'])
            ner_doubleless[entity['valeur']]["score"].append(entity['score'])

    return [v for k, v in ner_doubleless.items()]


class Test(unittest.TestCase):
    def test(self):
        file = open("article_test_ner.txt", "r")
        article = file.read()
        file.close()
        ner = ner_on_text(article)
        self.assertEqual(ner, [])

    def test_(self):
        ner = ner_on_text("Le 12 à 29r Planquette, Vitry-sur-Seine")
        self.assertEqual(ner, [])

    def test_2(self):
        ner = ner_on_text("Alice est au Pays des Merveilles")
        self.assertEqual(ner, [])
