from pyspark.sql import SparkSession

class Gestion_dataWarehouse:

    def __init__(self, table_sql):
        self.table = table_sql
        self.spark = self.pySession()
    
    def __str__(self):
        return self.spark
    
    def pySession(self):
        return SparkSession.builder \
               .appName("Session ETL vers le dataWarehouse") \
               .getOrCreate() 
    
    

