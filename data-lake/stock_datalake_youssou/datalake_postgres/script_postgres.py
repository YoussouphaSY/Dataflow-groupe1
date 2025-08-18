import pandas as pd
import psycopg2
from hdfs import InsecureClient
import json

# --- Connexion à PostgreSQL ---
# Attention : host doit être le nom du service dans docker-compose
conn = psycopg2.connect(
    host="postgres",  # nom du service PostgreSQL dans docker-compose
    port=5432,        # port interne du conteneur PostgreSQL
    database="post_db_collect",
    user="admin",
    password="admin"
)
cursor = conn.cursor()

# --- Extraire les données ---
query = "SELECT * FROM crops;"
cursor.execute(query)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

# Création DataFrame
df = pd.DataFrame(rows, columns=columns)
data_json = df.to_dict(orient='records')

cursor.close()
conn.close()
print(f"{len(data_json)} lignes récupérées depuis PostgreSQL.")

# --- Connexion à HDFS ---
hdfs_client = InsecureClient("http://namenode:9870", user="hadoop")
hdfs_path = "/user/hadoop/data-lake/raw/crops"
hdfs_client.makedirs(hdfs_path)

# Écriture du JSON dans HDFS
file_path = f"{hdfs_path}/crops_export.json"
with hdfs_client.write(file_path, encoding="utf-8", overwrite=True) as writer:
    json.dump(data_json, writer, ensure_ascii=False, indent=2)

print(f"Données exportées vers HDFS avec succès dans {file_path}.")
