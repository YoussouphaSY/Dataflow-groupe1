from pymongo import MongoClient
import pandas as pd

# Connexion avec authentification
user = "admin"
password = "admin"
host = "localhost:27017"  

mongo_uri = f"mongodb://{user}:{password}@{host}/?authSource=admin"
client = MongoClient(mongo_uri)

db = client["agriculture_db"]
collection = db["farms"]

# Lire CSV et insérer dans Mongo
df = pd.read_csv("stockage_data/stock_data_youssou/data_csv/farms.csv")
records = df.to_dict(orient="records")
collection.insert_many(records)

print("Données CSV stockées dans MongoDB avec authentification !")
