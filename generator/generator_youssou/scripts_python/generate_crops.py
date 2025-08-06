# ===============================================
# Script : Génération de données sur les types de cultures agricoles
# Objectif : Créer un fichier JSON listant différents types de cultures,
# leurs saisons de culture et leurs rendements moyens par hectare.
# ===============================================

import json
import random

# Liste des cultures agricoles simulées
crops = ["Mil", "Maïs", "Sorgho", "Riz", "Arachide", "Oignon", "Tomate"]

# Saisons possibles de culture
seasons = ["Hivernage", "Contre-saison", "Saison sèche"]

# Génération des données
data = [
    {
        "crop_id": i + 1,  # Identifiant unique pour chaque culture
        "name": crop,  # Nom de la culture
        "season": random.choice(seasons),  # Saison de culture associée (choisie aléatoirement)
        "avg_yield_kg_per_hectare": round(random.uniform(1000, 8000), 2)  
        # Rendement moyen en kilogrammes par hectare, valeur aléatoire entre 1000 et 8000 kg/ha
    }
    for i, crop in enumerate(crops)
]

# Écriture des données dans un fichier JSON avec indentation lisible et encodage UTF-8
with open("stockage_data/stockage_youssou/data_json/crops.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("crops.json généré avec succès !")
