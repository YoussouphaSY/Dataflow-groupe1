import os
import pandas as pd 
from sqlalchemy import create_engine
from pymongo import MongoClient
import re 

class Gestion_des_donnees:

    def __init__(self, dossiers_sources):
        self.dossiers = dossiers_sources
        self.postgres_connection = self.get_postCon()
        self.mongo_connection = self.get_mongoCon() 
    
    def get_postCon(self):
        user = "admin"
        host = "localhost"
        password="admin"
        port ="5445"
        db= "post_db_collect"
        return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")
    
    def get_mongoCon(self, nom_de_la_base="base_de_donnees"):
        user_mongo = "admin"
        password = "admin"
        host = "localhost"
        port = "27025"
        uri = f"mongodb://{user_mongo}:{password}@{host}:{port}/"
        client = MongoClient(uri)
        db = client[nom_de_la_base]
        return db
    
    def liens_des_fichiers(self):

        listes_des_fichiers = []
        for root, dirs, files in os.walk(self.dossiers):
            for file in files:
                if file.endswith('.csv') or file.endswith('.xls' or '.xlsx') or file.endswith('.json'):
                    full_path = os.path.join(root, file)
                    listes_des_fichiers.append(full_path)
        return listes_des_fichiers
    
    def extrait_nom(self, chemin_fichier):
        nom_table = os.path.basename(chemin_fichier).split(".")[0]
        return nom_table
    
    ###------------ INgection sur Postgres--------------------####
    def Postgres_ingection(self):
        fichiers = self.liens_des_fichiers()
        for el in fichiers:
            nom_du_table = self.extrait_nom(el)
            if el.endswith('.csv'):
                pd_csv = pd.read_csv(el)
                pd_csv.to_sql(
                  name= nom_du_table,   
                  con= self.postgres_connection,          
                  if_exists="replace",       
                  index=False                
                )
            elif el.endswith('.xls'or '.xlsx'):
                pd_excel = pd.read_excel(el)
                pd_excel.to_sql(
                    name=nom_du_table,
                    con= self.postgres_connection,
                    if_exists="replace",
                    index=False
                )

            elif el.endswith('.json'):
                pd_json = pd.read_json(el)
                pd_json.to_sql(
                    name=nom_du_table,
                    con= self.postgres_connection,
                    if_exists="replace",
                    index=False
                )


