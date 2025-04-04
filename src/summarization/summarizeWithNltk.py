import logging

import nltk
from nltk.tokenize import sent_tokenize

logger = logging.getLogger(__name__)
def summarize(texte, max_chars=4000):
    resume = []
    try:
        phrases = sent_tokenize(texte)
        total_chars = 0

        for phrase in phrases:
            if total_chars + len(phrase) > max_chars:
                break
            resume.append(phrase)
            total_chars += len(phrase)
    except Exception as e:
        logger.error("erreur lors du summarize :", exec_info=True)
        result = "erreur lors de la génération du résumé"
    return " ".join(resume)
