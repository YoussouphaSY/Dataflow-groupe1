import csv
import time
import random
from datetime import datetime

#Donnees de personnalisation
prenoms_noms = [
    "Mamadou Diop", "Aminata Ndoye", "Fatou Sarr", "Cheikh Fall", "Khadija Ba",
    "Abdoulaye Diallo", "Adama Cissé", "Oumar Thiam", "Coumba Gueye", "Ibrahima Lo",
    "Aissatou Sow", "Seydou Seck", "Ndeye Toure", "Alioune Faye", "Mariama Ly",
    "Boubacar Diagne", "Mamadou Sarr", "Aminata Ba", "Fatou Diallo", "Cheikh Cissé",
    "Fallilou Ndiaye", "Fatoumata Diallo", "Mamadou Sow", "Aminata Sarr", "Modou Faye"
]

liste_regions = ["Thiès", "Kaolack", "Saint-Louis", "Kolda"]

cultures_par_region = {
    "Kaolack": ["Mil", "Maïs", "Arachide"],
    "Saint-Louis": ["Riz", "Tomate", "Oignon"],
    "Kolda": ["Pastèque", "Riz", "Niébé"],
    "Ziguinchor": ["Riz", "Manioc", "Banane"],
    "Thiès": ["Arachide", "Légumes", "Sorgho"]
}

marches_par_region = {
    "Thiès": ["Marché Thiès", "Marché Mbour", "Marché Tivaouane"],
    "Kaolack": ["Marché Central", "Médina Mbaba", "Marché Ndoffane", "Marché Guinguinéo", "Marché Kahone"],
    "Saint-Louis": ["Marché Sor", "Marché Ndar", "Marché Richard Toll"],
    "Ziguinchor": ["Marché Boucotte", "Marché Ziguinchor", "Marché Bignona", "Marché Oussouye"],
    "Kolda": ["Marché Diaobé", "Marché Sédhiou", "Marché Goudomp"]
}

def generate_sale_data():
    #Le nom aleatoirement  en fonction de la liste des nom-prenoms
    nom = random.choice(prenoms_noms)
    region = random.choice(liste_regions)
    #Le produit aleatoirement  en fonction de la region choisie
    recolte = random.choice(cultures_par_region[region])
    marché = random.choice(marches_par_region[region])
    #Parametre du numero
    prefixe = random.choice(["77", "70", "75", "78" , "76"])
    numero = f"+221 {prefixe} {random.randint(100,999)} {random.randint(10,99)} {random.randint(10,99)}"

#Dictionnaire de donnée generé
    return {
        "Nom": nom,
        "Region": region,
        "Culture": recolte,
        "Quantité_kg": random.randint(100, 10000),
        "Prix_kg": round(random.uniform(100, 1000), 2),
        "Lieu_vente": marché,
        "Telephone": numero,
        "Timestamp": datetime.now().isoformat()
    }

#Ecriture et enregistrement dans un csv
def append_to_csv(data_list, filename="ventes.csv"):
    if not data_list:
        return
    
    #Recuperer les clé du premier dictionnaire pour les colonne (header)
    header = data_list[0].keys()
    
    #variable booleen pour verifier si le fichier existe deja
    si_fichier_exists = False
    
    #Ouvrir le fichier en mode lecture s'il existe
    try:
        with open(filename, 'r'):
            #Si le fichier s'ouvre on change la variable a True
            si_fichier_exists = True
    except FileNotFoundError:
        pass

    #Ouvrir le fichier en format ajout "a"
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        
        #Si le fichier n'existe pas
        if not si_fichier_exists:
            #Ecrire les colonne
            writer.writeheader()
            
        #Ecrire tous les donnees en format ligne
        writer.writerows(data_list)

while True:
    echantillon = [generate_sale_data() for _ in range(5)]   
    append_to_csv(echantillon)
    print(f"{len(echantillon)} données ajoutées à {datetime.now().strftime('%H:%M:%S')}")
    time.sleep(10)  
