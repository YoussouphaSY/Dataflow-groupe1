import random
import csv 
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from faker import Faker
import os

fake = Faker()

# Initialisation des données
prenoms_femmes = [
    "Aissatou", "Fatou", "Aminata", "Mariama", "Ndeye", "Adama", "Bineta", "Seynabou", "Khady", "Coumba","Rokhaya","helene","Maty"]

prenoms_hommes = [
    "Mamadou", "Ibrahima", "Cheikh", "Pape", "Ousmane", "Moussa", "El Hadji", "Abdoulaye", "Babacar", "Modou", "Sidy", "Lamine", "Mamadou Lamine", "Mamadou Boubacar", "Mamadou Diop", "Mamadou Ndiaye", "Mamadou Sow", "Mamadou Faye", "Mamadou Sarr"
]

noms_famille = [
    "Ndiaye", "Diop", "Fall", "Faye", "Sarr", "Ba", "Diallo", "Sow", "Sy", "Ndoye", "Thiam", "Gueye", "Camara", "Barry", "Kouyaté", "Toure", "Dieng", "Cissé", "Diagne", "Senghor", "Diakhate", "Gassama", "Kane", "Sall", "Balde", "Diallo", "Diouf", "Koulibaly", "Sow", "Fofana", "Traoré", "Keita", "Bamba", "Camara", "Dabo"
]

regions_senegal = [
    "Dakar", "Thiès", "Saint-Louis", "Kaolack", "Ziguinchor", "Tambacounda", "Kolda", "Louga", "Matam", "Fatick", "Sédhiou", "Diourbel", "Tivaouane", "Mbour"
]

cultures = ["mil","mais","arachide","sésame","haricot","coton","riz","manioc","igname","patate douce","légumes","fruits","autres"]

qualites = ["Excellente", "Bonne", "Moyenne", "Mauvaise"]

# Création des dossiers dans stock_data_mariama
def create_directories():
    base_path = "stock_data_mariama"
    directories = [
        os.path.join(base_path, "databug_csv"), 
        os.path.join(base_path, "databug_json"), 
        os.path.join(base_path, "databug_xml")
    ]
    
    # Créer le dossier principal s'il n'existe pas
    os.makedirs(base_path, exist_ok=True)
    
    # Créer les sous-dossiers
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print(f"Dossiers créés dans {base_path}/: databug_csv, databug_json, databug_xml")

def generate_recolte(id, nb_producteurs):
    return {
        'id': id,
        'producteur_id': random.randint(1, nb_producteurs),
        'culture': random.choice(cultures),
        'date_recolte': fake.date_between(start_date='-1y', end_date='today').isoformat(),
        'quantité_kg': round(random.uniform(200, 3000), 1),
        'prix_unitaire_fcfa': random.choice([125, 150, 175, 200, 225, 250]),
        'qualité': random.choice(qualites)
    }

def generate_producteur(id):
    sexe = random.choice(['M', 'F'])
    
    if sexe == 'M':
        prenom = random.choice(prenoms_hommes)
    else:
        prenom = random.choice(prenoms_femmes)

    nom_famille = random.choice(noms_famille)
    nom_complet = f"{prenom} {nom_famille}"
    
    return {
        'id': id,
        'nom': nom_complet,
        'sexe': sexe,
        'région': random.choice(regions_senegal),
        'âge': random.randint(18, 65),
        'culture': random.choice(cultures)
    }

def generate_cooperative(id):
    types_structures = ['GIE', 'Coopérative', 'Groupement']
    suffixes = ['And Défar', 'Jappo', 'Deggo', 'Naatangué', 'Moom Sa Bopp', 'Siggil Jigeen']

    type_structure = random.choice(types_structures)
    region = random.choice(regions_senegal)
    suffix = random.choice(suffixes)
    
    nom = f"{type_structure} {suffix} {region}"

    return {
        'id': id,
        'nom': nom,
        'région': region,
        'type_structure': type_structure,
        'date_creation': fake.date_between(start_date='-10y', end_date='today').isoformat(),
        'nb_membres': random.randint(5, 50)
    }

# Export CSV
def export_csv(data, filename, fieldnames):
    filepath = os.path.join("stock_data_mariama", "databug_csv", filename)
    with open(filepath, mode='w', newline='', encoding='utf-8') as fichier:
        writer = csv.DictWriter(fichier, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    print(f"CSV exporté → {filepath}")

# Export JSON
def export_json(data, filename):
    filepath = os.path.join("stock_data_mariama", "databug_json", filename)
    with open(filepath, mode='w', encoding='utf-8') as fichier:
        json.dump(data, fichier, ensure_ascii=False, indent=2)
    print(f"JSON exporté → {filepath}")

# Export XML
def export_xml(data, filename, root_name, item_name):
    filepath = os.path.join("stock_data_mariama", "databug_xml", filename)
    
    root = ET.Element(root_name)
    
    for item in data:
        item_element = ET.SubElement(root, item_name)
        for key, value in item.items():
            field = ET.SubElement(item_element, key)
            field.text = str(value)
    
    tree = ET.ElementTree(root)
    tree.write(filepath, encoding='utf-8', xml_declaration=True)
    print(f"XML exporté → {filepath}")

# Génération et export des producteurs (CSV uniquement)
def export_producteurs(nb_producteurs=50):
    print(f"Génération de {nb_producteurs} producteurs en format CSV...")
    producteurs = []
    
    for i in range(1, nb_producteurs + 1):
        producteur = generate_producteur(i)
        producteurs.append(producteur)
    
    # Export en CSV uniquement
    fieldnames = ['id', 'nom', 'sexe', 'région', 'âge', 'culture']
    export_csv(producteurs, "producteurs.csv", fieldnames)

# Génération et export des récoltes (JSON uniquement)
def export_recoltes(nb_recoltes=100, nb_producteurs=50):
    print(f"Génération de {nb_recoltes} récoltes en format JSON...")
    recoltes = []
    
    for i in range(1, nb_recoltes + 1):
        recolte = generate_recolte(i, nb_producteurs)
        recoltes.append(recolte)
    
    # Export en JSON uniquement
    export_json(recoltes, "recoltes.json")

# Génération et export des coopératives (XML uniquement)
def export_cooperatives(nb_coops=20):
    print(f"Génération de {nb_coops} coopératives en format XML...")
    cooperatives = []
    
    for i in range(1, nb_coops + 1):
        coop = generate_cooperative(i)
        cooperatives.append(coop)
    
    # Export en XML uniquement
    export_xml(cooperatives, "cooperatives.xml", "cooperatives", "cooperative")

# Fonction principale
def main():
    print("=== Générateur de données agricoles multi-format ===")
    print()
    
    # Création des dossiers
    create_directories()
    print()
    
    # Génération des données
    nb_producteurs = 5000
    nb_recoltes = 5000
    nb_coops = 5000
    
    export_producteurs(nb_producteurs)
    print()
    
    export_recoltes(nb_recoltes, nb_producteurs)
    print()
    
    export_cooperatives(nb_coops)
    print()
    
    print("=== Génération terminée ===")
    print(f"Données générées dans stock_data_mariama/:")
    print(f"- Producteurs en CSV: stock_data_mariama/databug_csv/producteurs.csv")
    print(f"- Récoltes en JSON: stock_data_mariama/databug_json/recoltes.json")
    print(f"- Coopératives en XML: stock_data_mariama/databug_xml/cooperatives.xml")

# Lancer la génération
if __name__ == '__main__':
    main()