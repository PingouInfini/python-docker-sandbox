# Utiliser une image Python officielle
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt depuis la racine du projet dans le répertoire de travail du conteneur
COPY ../requirements.txt /app/

# Installer les dépendances
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copier le dossier src depuis la racine du projet dans le répertoire de travail du conteneur
COPY ../src /app/src

# Commande pour démarrer l'application
CMD ["python", "src/main.py"]
# CMD ["tail", "-f", "/dev/null"]
