import random
from faker import Faker
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

fake = Faker('fr_FR')

regions = ["Dakar", "Thiès", "Kaolack", "Fatick", "Saint-Louis", "Tambacounda"]
cultures = ["Mil", "Maïs", "Arachide", "Riz", "Sorgho", "Niébé"]
sols = ["Sableux", "Argileux", "Limonneux", "Humifère"]
nutriments_list = ["Azote", "Phosphore", "Potassium", "Calcium", "Magnésium"]
niveaux = ["Aucun", "Primaire", "Secondaire", "Supérieur"]

def generer_donnee(id_parcelle, id_producteur):
    region = random.choice(regions)
    departement = f"{region}-Dept-{random.randint(1, 3)}"
    superficie = round(random.uniform(0.5, 10.0), 2)
    type_culture = random.choice(cultures)
    rendement = round(random.uniform(800, 4000), 2)

    date_semi = fake.date_between(start_date="-1y", end_date="-6mois")
    date_recolte = date_semi + timedelta(days=random.randint(90, 180))
    quantite = round(superficie * rendement, 2)

    temperature = round(random.uniform(20, 40), 1)
    precipitation = round(random.uniform(0, 300), 1)
    humidite = round(random.uniform(10, 90), 1)
    vent = round(random.uniform(0, 50), 1)

    type_sol = random.choice(sols)
    ph = round(random.uniform(5.5, 8.5), 2)
    nutriments = random.sample(nutriments_list, random.randint(1, 3))

    engrais = random.choice(["Oui", "Non"])
    q_engrais = round(random.uniform(0, 100), 2) if engrais == "Oui" else 0
    pesticide = random.choice(["Oui", "Non"])
    irrigation = random.choice(["Oui", "Non"])
    travaux_sol = random.randint(1, 5)

    nom = fake.name()
    sexe = random.choice(["Homme", "Femme"])
    age = random.randint(18, 70)
    niveau = random.choice(niveaux)
    telephone = fake.phone_number()

    cout = round(random.uniform(50000, 500000), 2)
    prix_kg = round(random.uniform(100, 500), 2)
    revenu = round(quantite * prix_kg, 2)

    return {
        "id_parcelle": id_parcelle,
        "region": region,
        "departement": departement,
        "superficie_ha": superficie,
        "type_culture": type_culture,
        "rendement_kg_ha": rendement,
        "date_semi": date_semi.isoformat(),
        "date_recolte": date_recolte.isoformat(),
        "quantite_recoltee_kg": quantite,
        "temperature_c": temperature,
        "precipitations_mm": precipitation,
        "humidite_%": humidite,
        "vent_kmh": vent,
        "type_sol": type_sol,
        "ph_sol": ph,
        "nutriments": ", ".join(nutriments),
        "engrais_utilise": engrais,
        "quantite_engrais_kg": q_engrais,
        "pesticide_utilise": pesticide,
        "irrigation": irrigation,
        "nbre_travaux_sol": travaux_sol,
        "id_producteur": id_producteur,
        "nom_producteur": nom,
        "sexe": sexe,
        "age": age,
        "niveau_etude": niveau,
        "telephone": telephone,
        "cout_total_production": cout,
        "revenu_vente": revenu,
        "prix_vente_kg": prix_kg
    }

# Création XML
def generer_xml(nb=100, nom_fichier="donnees_agricoles.xml"):
    root = ET.Element("donnees_agricoles")

    for i in range(nb):
        data = generer_donnee(i+1, 1000+i)
        parcelle_elem = ET.SubElement(root, "parcelle")

        for cle, valeur in data.items():
            elem = ET.SubElement(parcelle_elem, cle)
            elem.text = str(valeur)

    # Création de l’arbre XML
    tree = ET.ElementTree(root)
    tree.write("stockage_data/stock_data_marieme/data_json/api.json", encoding="utf-8", xml_declaration=True)
    print(f"Fichier XML '{'donnees_agricultures.xml'}' généré avec succès.")

# Appel
generer_xml(100)
