import nltk
from nltk.tokenize import sent_tokenize

def summarize(texte, max_chars=4000):
    phrases = sent_tokenize(texte)
    resume = []
    total_chars = 0

    for phrase in phrases:
        if total_chars + len(phrase) > max_chars:
            break
        resume.append(phrase)
        total_chars += len(phrase)

    return " ".join(resume)
