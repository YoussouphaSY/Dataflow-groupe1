# ===============================================
# Script : scrape_marche_agricole.py
# Objectif : Scraper les données agricoles économiques depuis marcheagricole.sn
# Auteur : Aminata (avec assistance ChatGPT)
# ===============================================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

# ----------------------------
# URL cible à scraper
# ----------------------------
url = "https://marcheagricole.sn/donnees-des-marches/"

# ----------------------------
# Requête HTTP pour récupérer le contenu HTML de la page
# ----------------------------
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Lève une exception si statut != 200
except requests.exceptions.RequestException as e:
    print(f"❌ Erreur lors de l'accès au site : {e}")
    exit()

# ----------------------------
# Analyse HTML avec BeautifulSoup
# ----------------------------
soup = BeautifulSoup(response.content, "html.parser")

# ----------------------------
# Extraction des données — ⚠️ À adapter selon le vrai HTML
# ----------------------------
# Exemple générique : récupération de lignes dans un tableau
table = soup.find("table")  # Cherche le premier tableau de la page
if not table:
    print("❌ Aucun tableau trouvé sur la page.")
    exit()

# Extraction des lignes du tableau
rows = table.find_all("tr")

# Initialisation de la liste des données
data = []

# Extraction ligne par ligne
for row in rows[1:]:  # on saute l'en-tête
    cols = row.find_all("td")
    if len(cols) < 5:  # Vérifie que la ligne est bien structurée
        continue
    data.append({
        "date": cols[0].text.strip(),
        "produit": cols[1].text.strip(),
        "region": cols[2].text.strip(),
        "prix_fcfa_kg": cols[3].text.strip(),
        "volume_kg": cols[4].text.strip()
    })

# ----------------------------
# Conversion en DataFrame
# ----------------------------
df = pd.DataFrame(data)

# ----------------------------
# Création du dossier de sortie
# ----------------------------
date_str = datetime.today().strftime('%Y-%m-%d')
output_dir = f"stockage_data/stock_data_amina/"
os.makedirs(output_dir, exist_ok=True)

# ----------------------------
# Sauvegarde en CSV
# ----------------------------
csv_path = os.path.join(output_dir, "csv/scraped_agri_data.csv")
df.to_csv(csv_path, index=False)

print(f"✅ Données scrappées avec succès : {csv_path}")
