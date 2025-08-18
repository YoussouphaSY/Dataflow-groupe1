sudo chown -R $USER:$USER ./Donnees_sources_bd/Mongodata/

sudo chown -R $USER:$USER /home/exemplesy/Bureau/ODC/DataFlow360/DataFlow360/Donnees_sources_bd/Mongodata/.mongodb


docker exec -it script_python360_2 python /root/scripts/mongo/script_mongo.py