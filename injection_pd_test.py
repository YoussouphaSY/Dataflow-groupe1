from generator.generator_ben.scripts_python.generate_script\
import Gestion_des_donnees

import os 


if __name__ == "__main__":

    # Donnees stockés en postgres

    doc = "./stockage_data/stock_data_ben/sources_donnees2"
    #print(os.listdir(doc))
    dossiers = Gestion_des_donnees(doc)
    dossiers.Postgres_ingection()

    # Donnees stockes en mysql 

    doc2 = "./stockage_data/stock_data_youssou"
    # print(os.listdir(doc2))
    dossier2 = Gestion_des_donnees(doc2)
    dossier2.Mysql_ingection()

    # Donnees stockes en mongodb 
    
    doc3 = "./stockage_data/stock_data_amina/csv"
    # print(os.listdir(doc3))
    #dossier3 = Gestion_des_donnees(doc3)
    #dossier3.creer_collection()