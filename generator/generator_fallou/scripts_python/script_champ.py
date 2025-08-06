# SCRIPT
import json
import random
from datetime import datetime, timedelta

liste_regions = ["Thiès", "Kaolack", "Saint-Louis", "Kolda"]

cultures_par_region = {
    "Kaolack": ["Mil", "Maïs", "Arachide"],
    "Saint-Louis": ["Riz", "Tomate", "Oignon"],
    "Kolda": ["Pastèque", "Riz", "Niébé"],
    "Thiès": ["Arachide", "Légumes", "Sorgho"]
}

etat_sanitaire_possibles = ["bon", "moyen", "critique"]

def generate_parcelle():
    region = random.choice(liste_regions)
    culture = random.choice(cultures_par_region[region])
    superficie = round(random.uniform(0.5, 5.0), 2)
    date_semis = datetime.now() - timedelta(days=random.randint(1, 60))
    prevision_recolte = date_semis + timedelta(days=random.randint(60, 100))
    latitude = round(random.uniform(12.0, 16.5), 5)
    longitude = round(random.uniform(-17.5, -12.0), 5)
    etat = random.choice(etat_sanitaire_possibles)
    irrigue = random.choice([True, False])
    
    return {
        "region": region,
        "culture": culture,
        "superficie_ha": superficie,
        "date_semis": date_semis.date().isoformat(),
        "previsions_recolte": prevision_recolte.date().isoformat(),
        "localisation": {
            "latitude": latitude,
            "longitude": longitude
        },
        "etat_sanitaire": etat,
        "irrigue": irrigue,
        "timestamp": datetime.now().isoformat()
    }
def append_to_json(data_list, filename="stockage_data/stock_data_fallou/parcelles.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except FileNotFoundError:
        donnees = []

    full_data = donnees + data_list

    with open(filename, "w", encoding="utf-8") as f:
        print("Enregistrement dans :", filename)
        json.dump(full_data, f, indent=4, ensure_ascii=False)
        

#Génération unique (pour Airflow)
if __name__ == "__main__":
    echantillon = [generate_parcelle() for _ in range(10)]
    append_to_json(echantillon)
    print(f"{len(echantillon)} parcelles ajoutées à {datetime.now().strftime('%H:%M:%S')}")
