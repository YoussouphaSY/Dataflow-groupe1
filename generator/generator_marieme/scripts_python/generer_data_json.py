import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('fr_FR')

# Valeurs possibles
regions = ["Dakar", "Thiès", "Fatick", "Kaolack", "Saint-Louis", "Tambacounda"]
types_cultures = ["Mil", "Maïs", "Arachide", "Riz", "Sorgho", "Niébé"]
types_sols = ["Sableux", "Argileux", "Limonneux", "Humifère"]
nutriments_possibles = ["Azote", "Phosphore", "Potassium", "Calcium", "Magnésium"]
niveaux_etudes = ["Aucun", "Primaire", "Secondaire", "Supérieur"]

def generer_ligne(id_parcelle, id_producteur):
    region = random.choice(regions)
    departement = f"{region}-Dept-{random.randint(1, 3)}"
    superficie = round(random.uniform(0.5, 10), 2)
    type_culture = random.choice(types_cultures)
    rendement = round(random.uniform(800, 4000), 2)

    date_semi = fake.date_between(start_date='-1y', end_date='-6mois')
    date_recolte = date_semi + timedelta(days=random.randint(90, 180))
    quantite_recoltee = round(superficie * rendement, 2)

    temperature = round(random.uniform(20, 40), 1)
    precipitations = round(random.uniform(0, 300), 1)
    humidite = round(random.uniform(10, 90), 1)
    vent = round(random.uniform(0, 50), 1)
    type_sol = random.choice(types_sols)
    ph_sol = round(random.uniform(5.5, 8.5), 2)
    nutriments = random.sample(nutriments_possibles, random.randint(1, 3))

    engrais_utilise = random.choice(["Oui", "Non"])
    quantite_engrais = round(random.uniform(0, 100), 2) if engrais_utilise == "Oui" else 0
    pesticide_utilise = random.choice(["Oui", "Non"])
    irrigation = random.choice(["Oui", "Non"])
    nbre_travaux_sol = random.randint(1, 5)

    nom_producteur = fake.name()
    sexe = random.choice(["Homme", "Femme"])
    age = random.randint(18, 65)
    niveau_etude = random.choice(niveaux_etudes)
    telephone = fake.phone_number()

    cout_total = round(random.uniform(50000, 500000), 2)
    prix_vente_kg = round(random.uniform(100, 500), 2)
    revenu_vente = round(quantite_recoltee * prix_vente_kg, 2)

    return {
        "id_parcelle": id_parcelle,
        "region": region,
        "departement": departement,
        "superficie_ha": superficie,
        "type_culture": type_culture,
        "rendement_kg_ha": rendement,
        "date_semi": date_semi.isoformat(),
        "date_recolte": date_recolte.isoformat(),
        "quantite_recoltee_kg": quantite_recoltee,
        "temperature_c": temperature,
        "precipitations_mm": precipitations,
        "humidite_%": humidite,
        "vent_kmh": vent,
        "type_sol": type_sol,
        "ph_sol": ph_sol,
        "nutriments": nutriments,
        "engrais_utilise": engrais_utilise,
        "quantite_engrais_kg": quantite_engrais,
        "pesticide_utilise": pesticide_utilise,
        "irrigation": irrigation,
        "nbre_travaux_sol": nbre_travaux_sol,
        "id_producteur": id_producteur,
        "nom_producteur": nom_producteur,
        "sexe": sexe,
        "age": age,
        "niveau_etude": niveau_etude,
        "telephone": telephone,
        "cout_total_production": cout_total,
        "revenu_vente": revenu_vente,
        "prix_vente_kg": prix_vente_kg
    }

# Génération du fichier JSON
def generer_json(n=100, nom_fichier="donnees_agricoles.json"):
    donnees = []
    for i in range(n):
        ligne = generer_ligne(id_parcelle=i+1, id_producteur=1000+i)
        donnees.append(ligne)

    with open("stockage_data/stock_data_marieme/data_json/donnees_agricultures.json", "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=4)

    print(f"Fichier JSON '{'donnees_agriculture.json'}' généré avec succès.")

# Appel de la fonction
generer_json(100)
