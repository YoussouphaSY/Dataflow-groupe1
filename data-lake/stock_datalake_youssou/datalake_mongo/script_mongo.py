from pymongo import MongoClient
from hdfs import InsecureClient
import json

# --- MongoDB ---
user = "admin"
password = "admin"
host = "mongodb:27017"  
mongo_uri = f"mongodb://{user}:{password}@{host}/?authSource=admin"
client = MongoClient(mongo_uri)
db = client["agriculture_db"]
collection = db["farms"]
print("Connexion à MongoDB réussie.")

documents = list(collection.find({}))
data_json = [json.loads(json.dumps(doc, default=str)) for doc in documents]

# --- HDFS ---
hdfs_client = InsecureClient("http://namenode:9870", user="hadoop")
hdfs_path = "/user/hadoop/data-lake/raw/data-json"
hdfs_client.makedirs(hdfs_path)

file_path = f"{hdfs_path}/mongo_export.json"
with hdfs_client.write(file_path, encoding="utf-8", overwrite=True) as writer:
    json.dump(data_json, writer, ensure_ascii=False, indent=2)

print(f"Données exportées vers HDFS avec succès dans {file_path}.")
