# ============================================================
# Script : insert_postgres.py
# Objectif : Insérer les données agricoles dans PostgreSQL
# Source : Fichier CSV généré précédemment
# Auteur : Aminata (avec assistance ChatGPT)
# ============================================================

import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# -------------------------------
# Charger les variables d'environnement
# -------------------------------
load_dotenv(dotenv_path="../.env")  # chemin vers le fichier .env

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# -------------------------------
# Connexion à PostgreSQL
# -------------------------------
try:
    conn = psycopg2.connect(
        host="localhost",
        port="5445",
        dbname="post_db_collect",
        user="admin",
        password="admin"
    )
    print("✅ Connexion à PostgreSQL réussie.")
except Exception as e:
    print(f"❌ Erreur de connexion à PostgreSQL : {e}")
    exit()

cursor = conn.cursor()

# -------------------------------
# Création de la table si elle n'existe pas
# -------------------------------
create_table_query = """
CREATE TABLE IF NOT EXISTS donnees_agricoles (
    id SERIAL PRIMARY KEY,
    date DATE,
    region VARCHAR(100),
    produit VARCHAR(100),
    prix_fcfa_kg NUMERIC,
    volume_kg INTEGER,
    marche VARCHAR(100),
    devise VARCHAR(10),
    source VARCHAR(50)
);
"""
cursor.execute(create_table_query)
conn.commit()

# -------------------------------
# Lecture du fichier CSV
# -------------------------------
try:
    today = pd.Timestamp.today().strftime('%Y-%m-%d')
    csv_path = f"/stockage_data/stock_data_amina/csv/scraped_agri_dat"
    df = pd.read_csv(csv_path)
    print(f"✅ Lecture du fichier : {csv_path}")
except Exception as e:
    print(f"❌ Erreur lecture fichier : {e}")
    exit()

# Nettoyage des colonnes (si nécessaire)
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# -------------------------------
# Insertion ligne par ligne
# -------------------------------
insert_query = """
INSERT INTO donnees_agricoles (
    date, region, produit, prix_fcfa_kg, volume_kg, marche, devise, source
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    try:
        values = (
            row.get("date"),
            row.get("region"),
            row.get("produit"),
            row.get("prix_fcfa_kg"),
            row.get("volume_kg"),
            row.get("marche", "N/A"),
            row.get("devise", "FCFA"),
            row.get("source", "api")
        )
        cursor.execute(insert_query, values)
    except Exception as e:
        print(f"⚠️ Erreur insertion ligne : {e}")
        continue

conn.commit()
cursor.close()
conn.close()
print("✅ Données insérées avec succès dans PostgreSQL.")
