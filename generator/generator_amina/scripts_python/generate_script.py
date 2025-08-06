# SCRIPT# ============================================
# Script : generate_agri_data.py
# Objectif : Générer des données agricoles sénégalaises simulées
# Formats : CSV, JSON, Excel, XML, YAML
# Dossier de sortie : ../stockage_data/YYYY-MM-DD/
# ============================================

import os
import random
import pandas as pd
from faker import Faker
from datetime import datetime
import yaml
import json
import xmltodict

# ----------------------------
# Initialisation du Faker
# ----------------------------
fake = Faker('fr_FR')  # Langue française

# ----------------------------
# Paramètres de simulation
# ----------------------------
NB_ENTREES = 100  # Nombre de lignes de données à générer

# Listes personnalisées pour le contexte agricole sénégalais
regions = ["Dakar", "Thiès", "Kaolack", "Fatick", "Saint-Louis", "Ziguinchor", "Tambacounda", "Kolda"]
produits = ["Arachide", "Mil", "Maïs", "Riz", "Sorgho", "Niébé", "Oignon", "Tomate", "Bissap"]
marches = ["Marché Sandaga", "Marché Kaolack", "Marché Tilène", "Marché Saloum", "Marché Castors"]
sources = ["simulation"]
devise = "FCFA"

# ----------------------------
# Création des données simulées
# ----------------------------
donnees = []

for _ in range(NB_ENTREES):
    entree = {
        "date": fake.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
        "region": random.choice(regions),
        "produit": random.choice(produits),
        "prix_fcfa_kg": round(random.uniform(100, 800), 2),  # prix entre 100 et 800 FCFA/kg
        "volume_kg": random.randint(100, 2000),  # entre 100 et 2000 kg
        "marche": random.choice(marches),
        "devise": devise,
        "source": random.choice(sources)
    }
    donnees.append(entree)

# Conversion en DataFrame pour exploitation avec pandas
df = pd.DataFrame(donnees)

# ----------------------------
# Création du dossier de sortie
# ----------------------------
date_str = datetime.today().strftime('%Y-%m-%d')
output_dir = f"stockage_data/stock_data_amina/"
os.makedirs(output_dir, exist_ok=True)

# ----------------------------

# ----------------------------
# Sauvegarde en JSON
# ----------------------------
with open(os.path.join(output_dir, "json/agri_data.json"), "w", encoding='utf-8') as f:
    json.dump(donnees, f, ensure_ascii=False, indent=4)


# ----------------------------
# Message de succès
# ----------------------------
print(f"✅ Données générées avec succès dans : {output_dir}")
