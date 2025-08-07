from generator.generator_ben.scripts_python.generate_script\
import Gestion_des_donnees

import os 


if __name__ == "__main__":
    doc = "./stockage_data/stock_data_ben/sources_donnees2"
    #print(os.listdir(doc))
    #dossiers = Gestion_des_donnees(doc)
    #dossiers.Postgres_ingection()

    doc2 = "./stockage_data/stock_data_youssou"
    print(os.listdir(doc2))
    dossier2 = Gestion_des_donnees(doc2)
    dossier2.Mysql_ingection()