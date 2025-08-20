
import pandas as pd 
from generator.generator_ben.scripts_python.connexion import GestionnairesConnexion
import os 
from dotenv import load_dotenv

load_dotenv()

class GestionLake(GestionnairesConnexion):

    def __init__(self):
        super().__init__()
    
  #--------------Mysql-----------------------------------------------------#  
    def voir_listes_tablesMysql(self):
        db_name = os.getenv("db")
        tables = pd.read_sql("show tables", self.mysql_connection)
        listes_tables = list(tables[f'Tables_in_{db_name}'].values)
        return listes_tables
  #-------------------Posgres----------------------------------------------#
    def voirlistes_tablesPostgres(self):
        db_name=os.getenv("POSTGRES_DB")
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
        tables = pd.read_sql(query, self.postgres_connection)
        return tables["table_name"].tolist()
        
    def mysql_to_hdfs(self):
        for el in self.voir_listes_tablesMysql():
            df = pd.read_sql(f"SELECT * FROM {el}", self.mysql_connection)
            parquet_file = f"{el}.parquet"
            df.to_parquet(parquet_file, engine='pyarrow', index=False)
            self.client_hadoop.upload(f"/user/hadoop/{parquet_file}",parquet_file, overwrite=True)
            os.remove(parquet_file)  


    def postgres_to_hdfs(self):
        for el in self.voirlistes_tablesPostgres():
            df = pd.read_sql(f"SELECT * FROM {el}", self.postgres_connection)
            parquet_file = f"{el}.parquet"
            df.to_parquet(parquet_file, engine='pyarrow', index=False)
            self.client_hadoop.upload(f"/user/hadoop/{parquet_file}", parquet_file, overwrite=True)
            os.remove(parquet_file)

