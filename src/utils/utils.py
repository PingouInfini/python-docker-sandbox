import logging

logger = logging.getLogger(__name__)

def uppercase_vowels(text):
    vowels = "aeiou"
    logger.debug(f"Transformation des voyelles pour le texte: {text}")
    return ''.join([char.upper() if char in vowels else char for char in text])
