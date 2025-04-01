# Utiliser une image Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt depuis la racine du projet dans le répertoire de travail du conteneur
COPY ../requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

# Copier le dossier src depuis la racine du projet dans le répertoire de travail du conteneur
COPY ../src /app/src

# Commande pour démarrer l'application
CMD ["python", "src/main.py"]
# CMD ["tail", "-f", "/dev/null"]
