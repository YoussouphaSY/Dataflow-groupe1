from sqlalchemy import create_engine
from pymongo import MongoClient
import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from hdfs import InsecureClient
from dotenv import load_dotenv
load_dotenv()


class GestionnairesConnexion:

    def __init__(self):
        self.postgres_connection = self.get_postCon()
        self.mongo_connection = self.get_mongoCon() 
        self.date = datetime.date.today()
        self.mysql_connection = self.get_mysql_conn()
        #self.cassadra_connection = self.get_cassandra()
        self.client_hadoop = self.get_client_hadoop()

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
    
    # ---------- Connection sur haddop hdfs---------------------#

    def get_client_hadoop(self):
        client = InsecureClient("http://localhost:9870", user="hadoop")
        return client


    

        