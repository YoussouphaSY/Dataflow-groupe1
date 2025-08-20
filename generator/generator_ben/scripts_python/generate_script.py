import os
import unidecode
import pandas as pd 
from generator.generator_ben.scripts_python.connexion import GestionnairesConnexion
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider




class Gestion_des_donnees(GestionnairesConnexion):
    def __init__(self, dossiers_sources):
        super().__init__()  
        self.dossiers = dossiers_sources

        

#------ Lectures des fichiers -----------------------------------# 

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
                table_name = unidecode.unidecode(table_name).lower()

                    # Colonnes sans accent
                colonnes_sans_accent = [unidecode.unidecode(col).replace(' ', '_').lower() for col in pd_csv.columns]
                columns_def = ", ".join([f'"{col}" text'for col in colonnes_sans_accent])
                primary_key = colonnes_sans_accent[0]

                    # Créer la table
                session.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_def}, PRIMARY KEY ({primary_key}))')

                    # Insérer les données
                for _, row in pd_csv.iterrows():
                    valeurs = ", ".join([f"'{str(v)}'" for v in row])
                    session.execute(f"""INSERT INTO {table_name} ({', '.join(colonnes_sans_accent)}) VALUES ({valeurs})""")

 
