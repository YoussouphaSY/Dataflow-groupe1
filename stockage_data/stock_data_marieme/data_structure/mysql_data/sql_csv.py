import csv
from pymysql import connect
conn = connect(
    host="localhost",
    user="root",
    password="admin",
    database="mysql_db_collecte",
    port=3310
)
# Connexion à MySQL

cursor = conn.cursor()

# Créer la table si elle n'existe pas encore
cursor.execute("""
CREATE TABLE IF NOT EXISTS donnees_agricoles (
    id_parcelle INT,
    region VARCHAR(100),
    departement VARCHAR(100),
    superficie_ha FLOAT,
    type_culture VARCHAR(100),
    rendement_kg_ha FLOAT,
    date_semi DATE,
    date_recolte DATE,
    quantite_recoltee_kg FLOAT,
    temperature_c FLOAT,
    precipitations_mm FLOAT,
    humidite_percent FLOAT,
    vent_kmh FLOAT,
    type_sol VARCHAR(100),
    ph_sol FLOAT,
    nutriments TEXT,
    engrais_utilise VARCHAR(100),
    quantite_engrais_kg FLOAT,
    pesticide_utilise VARCHAR(100),
    irrigation VARCHAR(50),
    nbre_travaux_sol INT,
    id_producteur INT,
    nom_producteur VARCHAR(100),
    sexe VARCHAR(10),
    age INT,
    niveau_etude VARCHAR(100),
    telephone VARCHAR(20),
    cout_total_production FLOAT,
    revenu_vente FLOAT,
    prix_vente_kg FLOAT
);
""")

# Lecture du fichier CSV et insertion
with open('/home/mariam/Documents/nouveau_data_flow/Dataflow-groupe1/stockage_data/stock_data_marieme/data_csv/donnees_agriculture.csv', newline='', encoding='utf-8') as fichier_csv:
    reader = csv.reader(fichier_csv)
    next(reader)  # sauter l'en-tête

    for ligne in reader:
        cursor.execute("""
        INSERT INTO donnees_agricoles VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ligne)

# Commit et fermeture
conn.commit()
cursor.close()
conn.close()

print("Données insérées dans MySQL avec succès.")
      