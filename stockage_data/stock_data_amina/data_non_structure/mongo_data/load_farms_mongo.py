# Donnees depuis CSV vers MongoDB 
from pymongo import MongoClient
import pandas as pd

# Connexion sécurisée avec auth
client = MongoClient("mongodb://mongo_admin:mongo_pass123@localhost:27017/")
db = client["agriculture_db"]
collection = db["farms"]

# Lire CSV et insérer dans Mongo
df = pd.read_csv("stockage_data/stockage_youssou/data_csv/farms.csv")
records = df.to_dict(orient="records")
collection.insert_many(records)

print("Données CSV stockées dans MongoDB avec authentification !")
