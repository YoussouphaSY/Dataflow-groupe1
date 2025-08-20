
import pandas as pd 
from generator.generator_ben.scripts_python.connexion import GestionnairesConnexion
import os 
from dotenv import load_dotenv

load_dotenv()

class GestionLake(GestionnairesConnexion):

    def __init__(self):
        super().__init__()

    def voir_listes_tables(self):
        db_name = os.getenv("db")
        tables = pd.read_sql("show tables", self.mysql_connection)
        listes_tables = list(tables[f'Tables_in_{db_name}'].values)
        return listes_tables
        
    def mysql_to_hdfs(self):
        resultats = []
        for el in self.voir_listes_tables():
            df = pd.read_sql(f"SELECT * FROM {el}", self.mysql_connection)
            parquet_file = f"{el}.parquet"
            df.to_parquet(parquet_file, engine='pyarrow', index=False)
            resultat = self.client_hadoop.upload(f"/user/hadoop/{parquet_file}", parquet_file)
            resultats.append(resultat)
            os.remove(parquet_file)  
        return resultats
