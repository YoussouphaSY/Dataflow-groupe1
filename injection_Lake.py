from generator.generator_ben.scripts_python.script_datalake\
import GestionLake


if __name__=="__main__":

    ingestion = GestionLake()
    print(ingestion.voir_listes_tablesMysql())
    #ingestion.mysql_to_hdfs()
    ingestion.postgres_to_hdfs()
