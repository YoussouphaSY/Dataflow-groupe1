import os
import pandas as pd 
from sqlalchemy import create_engine
from pymongo import MongoClient
import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class Gestion_des_donnees:

    def __init__(self, dossiers_sources):
        self.dossiers = dossiers_sources
        self.postgres_connection = self.get_postCon()
        self.mongo_connection = self.get_mongoCon() 
        self.date = datetime.date.today()
        self.mysql_connection = self.get_mysql_conn()
        self.cassadra_connection = self.get_cassandra()
    
    #-------------- connection Mysql -----------------------#
    def get_mysql_conn(self):
        user="root"
        host = "localhost"
        password = "admin"
        port = "3310"
        db = "mysql_db_collecte"

        return create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
    
    #-------------- connection Postgres -----------------------#
    def get_postCon(self):
        user = "admin"
        host = "localhost"
        password="admin"
        port ="5445"
        db= "post_db_collect"
        return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")
    
    #-------------- connection MongoDB -----------------------#
    def get_mongoCon(self, nom_de_la_base="Donnees_collectes"):
        user_mongo = "admin"
        password = "admin"
        host = "localhost"
        port = "27025"
        uri = f"mongodb://{user_mongo}:{password}@{host}:{port}/"
        client = MongoClient(uri)
        db = client[nom_de_la_base]
        return db
    
    #-------------- connection Cassandra -----------------------#
    def get_cassandra(self, keyspace = "donnee_fao"):
        user = "admin"
        password="admin"
        host = "localhost"
        port = "9055"

        auth_provider = PlainTextAuthProvider(username=user, password=password)
        cluster = Cluster([host], port=port, auth_provider=auth_provider)
        session = cluster.connect()
        session.set_keyspace(keyspace)
        return session

        



    #-------------- connection Neo4J -----------------------#



    
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
                  name= f"{nom_du_table}_{self.date}".replace('-','_'), 
                  con= self.postgres_connection,          
                  if_exists="replace",       
                  index=False                
                )
            elif el.endswith('.xls'or '.xlsx'):
                pd_excel = pd.read_excel(el)
                pd_excel.to_sql(
                    name=f"{nom_du_table}_{self.date}".replace('-','_'),
                    con= self.postgres_connection,
                    if_exists="replace",
                    index=False
                )

            elif el.endswith('.json'):
                pd_json = pd.read_json(el)
                pd_json.to_sql(
                    name=f"{nom_du_table}_{self.date}".replace('-','_'),
                    con= self.postgres_connection,
                    if_exists="replace",
                    index=False
                )


    ### --------------------ingection mysql------------------------------####

    def Mysql_ingection(self):
        fichiers = self.liens_des_fichiers()
        for el in fichiers:
            nom_du_table = self.extrait_nom(el)
            if el.endswith('.csv'):
                pd_csv = pd.read_csv(el)
                pd_csv.to_sql(
                  name= f"{nom_du_table}_{self.date}".replace('-','_'),   
                  con= self.mysql_connection,          
                  if_exists="replace",       
                  index=False                
                )
            elif el.endswith('.xls'or '.xlsx'):
                pd_excel = pd.read_excel(el)
                pd_excel.to_sql(
                    name=f"{nom_du_table}_{self.date}".replace('-','_'),
                    con= self.mysql_connection,
                    if_exists="replace",
                    index=False
                )
            elif el.endswith('.json'):
                pd_json = pd.read_json(el)
                pd_json.to_sql(
                    name=f"{nom_du_table}_{self.date}".replace('-','_'),
                    con= self.mysql_connection,
                    if_exists="replace",
                    index=False
                )

### -------------------Injection MongoDB----------------------------- ####

    def creer_collection(self):
        fichiers = self.liens_des_fichiers()
        for el in fichiers:
            nom_de_la_collection = self.extrait_nom(el) # chaque fichier est une collection
            collection = self.mongo_connection[f"{nom_de_la_collection}_{self.date}".replace('-','_')]
            # stockage des fichier csv 
            if el.endswith('.csv'):
                pd_csv = pd.read_csv(el)
                donnees = pd_csv.to_dict(orient='records')
                collection.insert_many(donnees)
            # stockage des fichiers excel 
            elif el.endswith('.xls'or '.xlsx'):
                pd_excel = pd.read_excel(el)
                donnees = pd_excel.to_dict(orient='records')
                collection.insert_many(donnees)
            # Stockage des fichiers json 
            elif el.endswith('.json'):
                pd_json = pd.read_json(el)            
                donnees = pd_json.to_dict(orient='records')
                collection.insert_many(donnees)

## -----Ingection cassandra -------------------------------------#####
    def creer_Table(self, keyspace='donnee_fao'):
        cluster = Cluster(['127.0.0.1'], port=9055)
        session = cluster.connect()

        # Créer le keyspace si inexistant
        session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {keyspace}
            WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
        """)
        session.set_keyspace(keyspace)

        fichiers = self.liens_des_fichiers()
        for el in fichiers:
            if el.endswith('.csv'):
                pd_csv = pd.read_csv(el)
                table_name = self.extrait_nom(el).replace('-', '_')

                # Créer une table avec toutes les colonnes en text
                colonnes = ", ".join([f"{col} text" for col in pd_csv.columns])
                session.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({colonnes}, PRIMARY KEY ({pd_csv.columns[0]}))")

                # Insérer les données
                for _, row in pd_csv.iterrows():
                    valeurs = ", ".join([f"'{str(v)}'" for v in row])
                    session.execute(f"INSERT INTO {table_name} ({', '.join(pd_csv.columns)}) VALUES ({valeurs})")