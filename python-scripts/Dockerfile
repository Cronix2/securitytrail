FROM python:3.9

# Installation de libmariadb-dev
RUN apt-get update && apt-get install -y libmariadb-dev && rm -rf /var/lib/apt/lists/*

# Définition du dossier de travail
WORKDIR /app

# Copie des fichiers de l'application
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie des scripts Python
COPY . .

# Commande par défaut
CMD ["python", "main.py", "-a"]
