# FROM python:3.11-slim

# # Dossier de travaille dans le container
# WORKDIR /app

# # On copy tout dans le repertoire
# COPY . .

# RUN pip install -r requirements.txt

# CMD [ "python", "data-lake/stock_datalake_youssou/datalake_mongo/script_mongo.py" ]

FROM python:3.11-slim

WORKDIR /app
COPY . .

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "data-lake/stock_datalake_youssou/datalake_mongo/script_mongo.py" ]
