# Donnees depuis data_json vers Postgres
import json
import psycopg2

# Connexion PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5433",  # Port modifié pour correspondre au docker-compose
    database="agriculture_db",
    user="admin",
    password="admin123"
)
cur = conn.cursor()

# Créer table si elle n’existe pas
cur.execute("""
CREATE TABLE IF NOT EXISTS crops (
    crop_id INT PRIMARY KEY,
    name TEXT,
    season TEXT,
    avg_yield_kg_per_hectare FLOAT
);
""")

# Charger le fichier JSON
with open("stockage_data/stockage_youssou/data_json/crops.json", "r", encoding="utf-8") as f:
    crops = json.load(f)

# Insérer les données
for crop in crops:
    cur.execute("""
        INSERT INTO crops (crop_id, name, season, avg_yield_kg_per_hectare)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (crop_id) DO NOTHING;
    """, (
        crop["crop_id"],
        crop["name"],
        crop["season"],
        crop["avg_yield_kg_per_hectare"]
    ))

conn.commit()
cur.close()
conn.close()
print("Données JSON stockées dans PostgreSQL !")
