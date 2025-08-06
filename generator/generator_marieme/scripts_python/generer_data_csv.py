import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('fr_FR')

# Valeurs possibles pour certaines colonnes
regions = ["Dakar", "Thies", "Kaolack", "Fatick", "Saint-Louis", "Tambacounda"]
types_cultures = ["Mil", "Maïs", "Arachide", "Riz", "Sorgho", "Niébé"]
types_sols = ["Sableux", "Argileux", "Limonneux", "Humifère"]
nutriments_possibles = ["Azote", "Phosphore", "Potassium", "Calcium", "Magnésium"]
niveaux_etudes = ["Aucun", "Primaire", "Secondaire", "Supérieur"]

def generer_ligne(id_parcelle, id_producteur):
    region = random.choice(regions)
    departement = f"{region}-dept-{random.randint(1, 5)}"
    superficie_ha = round(random.uniform(0.5, 10.0), 2)
    type_culture = random.choice(types_cultures)
    rendement = round(random.uniform(500, 4000), 2)
    
    date_semi = fake.date_between(start_date='-1y', end_date='-6mois')
    date_recolte = date_semi + timedelta(days=random.randint(90, 180))
    quantite_recoltee = round(superficie_ha * rendement, 2)
    
    temperature = round(random.uniform(20.0, 40.0), 1)
    precipitations = round(random.uniform(0.0, 300.0), 1)
    humidite = round(random.uniform(10.0, 90.0), 1)
    vent = round(random.uniform(0.0, 50.0), 1)
    type_sol = random.choice(types_sols)
    ph_sol = round(random.uniform(5.5, 8.5), 2)
    nutriments = random.sample(nutriments_possibles, k=random.randint(1, 3))
    
    engrais_utilise = random.choice(["Oui", "Non"])
    quantite_engrais = round(random.uniform(0.0, 100.0), 2) if engrais_utilise == "Oui" else 0.0
    pesticide_utilise = random.choice(["Oui", "Non"])
    irrigation = random.choice(["Oui", "Non"])
    nbre_travaux_sol = random.randint(1, 5)
    
    nom_producteur = fake.name()
    sexe = random.choice(["Homme", "Femme"])
    age = random.randint(18, 70)
    niveau_etude = random.choice(niveaux_etudes)
    telephone = fake.phone_number()
    
    cout_total_production = round(random.uniform(50000, 1000000), 2)
    prix_vente_kg = round(random.uniform(100, 500), 2)
    revenu_vente = round(quantite_recoltee * prix_vente_kg, 2)
    
    return {
        "id_parcelle": id_parcelle,
        "region": region,
        "departement": departement,
        "superficie_ha": superficie_ha,
        "type_culture": type_culture,
        "rendement_kg_ha": rendement,
        "date_semi": date_semi,
        "date_recolte": date_recolte,
        "quantite_recoltee_kg": quantite_recoltee,
        "temperature_c": temperature,
        "precipitations_mm": precipitations,
        "humidite_%": humidite,
        "vent_kmh": vent,
        "type_sol": type_sol,
        "ph_sol": ph_sol,
        "nutriments": ", ".join(nutriments),
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
        "cout_total_production": cout_total_production,
        "revenu_vente": revenu_vente,
        "prix_vente_kg": prix_vente_kg
    }

# Générer les données
def generer_donnees(nb_lignes=100):
    data = []
    for i in range(1, nb_lignes + 1):
        ligne = generer_ligne(i, 1000 + i)
        data.append(ligne)
    return pd.DataFrame(data)

# Génération et sauvegarde en CSV
df = generer_donnees(100)
df.to_csv("stockage_data/stock_data_marieme/data_csv/donnees_agriculture.csv", index=False, encoding="utf-8")

print("Fichier 'donnees_agriculture.csv' généré avec succès.")
