# ===============================================
# Script : Génération de données d'exploitations agricoles
# Objectif : Créer un fichier CSV simulant 100 exploitations agricoles
# Les données générées incluent un identifiant unique, le nom du propriétaire,
# la région, la superficie en hectares, le type d'exploitation, et la date de création.
# ===============================================

import pandas as pd
from faker import Faker
import random

fake = Faker()

def generate_farms(n=100):
    """
    Génère un jeu de données simulées pour des exploitations agricoles.

    Paramètre :
    - n (int) : nombre de fermes à générer (par défaut 100)

    Chaque ferme contient les colonnes suivantes :
    - farm_id : Identifiant unique de la ferme (UUID)
    - owner : Nom du propriétaire de la ferme (nom complet aléatoire)
    - region : Région géographique où se trouve la ferme (nom d'État généré par Faker)
    - area_hectares : Superficie de la ferme en hectares (entre 1 et 500 ha)
    - type : Type d'exploitation (choisi parmi "Céréales", "Maraîchage", "Élevage", "Mixte")
    - created_at : Date de création de la ferme (aléatoire sur les 5 dernières années)
    """

    data = []
    for _ in range(n):
        data.append({
            "farm_id": fake.uuid4(),  # Identifiant unique de la ferme
            "owner": fake.name(),  # Nom complet du propriétaire
            "region": fake.state(),  # Région ou état simulé
            "area_hectares": round(random.uniform(1, 500), 2),  # Superficie en hectares
            "type": random.choice(["Céréales", "Maraîchage", "Élevage", "Mixte"]),  # Type d'activité agricole
            "created_at": fake.date_between(start_date='-5y', end_date='today')  # Date de création
        })

    # Création du DataFrame
    df = pd.DataFrame(data)

    # Enregistrement au format CSV
    df.to_csv("stockage_data/stock_data_youssou/data_json/farms.csv", index=False)
    print("farms.csv généré avec succès !")

if __name__ == "__main__":
    generate_farms()
