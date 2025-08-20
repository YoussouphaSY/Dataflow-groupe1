from generator.generator_ben.scripts_python.script_datalake\
import GestionLake


if __name__=="__main__":

    ingestion = GestionLake()
    print(ingestion.voir_listes_tables())
    ingestion.mysql_to_hdfs()