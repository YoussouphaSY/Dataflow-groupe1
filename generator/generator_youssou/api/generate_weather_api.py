# ===============================================
# Script : Récupération et conversion des données météo horaires
# Objectif : Interroger l'API Open-Meteo pour récupérer les températures horaires
# de la ville de Dakar, puis convertir les données JSON en fichier XML.
# ===============================================

import requests
import xml.etree.ElementTree as ET
import os

def json_to_xml(json_data):
    """
    Convertit les données météo JSON en un arbre XML structuré.

    Structure XML générée :
    <weather_data>
        <hourly>
            <entry>
                <time>...</time>
                <temperature_2m>...</temperature_2m>
            </entry>
            ...
        </hourly>
    </weather_data>

    Args:
        json_data (dict): Données JSON issues de l'API météo.

    Returns:
        ET.ElementTree : Arbre XML contenant les données converties.
    """
    root = ET.Element("weather_data")
    hourly = ET.SubElement(root, "hourly")

    times = json_data["hourly"]["time"]  # Liste des timestamps horaires
    temperatures = json_data["hourly"]["temperature_2m"]  # Liste des températures à 2m d'altitude

    for i in range(len(times)):
        entry = ET.SubElement(hourly, "entry")
        ET.SubElement(entry, "time").text = times[i]  # Heure (format ISO 8601)
        ET.SubElement(entry, "temperature_2m").text = str(temperatures[i])  # Température en °C

    return ET.ElementTree(root)

def get_weather_xml(lat=14.6928, lon=-17.4467):
    """
    Appelle l'API Open-Meteo pour récupérer les données météo horaires d'une localisation,
    convertit les données en XML, et sauvegarde dans un fichier.

    Args:
        lat (float): Latitude (par défaut celle de Dakar)
        lon (float): Longitude (par défaut celle de Dakar)
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # Récupère les données JSON
        xml_tree = json_to_xml(data)  # Conversion en XML

        # Création du dossier s'il n'existe pas
        os.makedirs("stockage_data/data_xml", exist_ok=True)

        # Écriture du fichier XML
        xml_tree.write("stockage_data/stockage_youssou/data_xml/weather_data.xml", encoding="utf-8", xml_declaration=True)
        print("weather_data.xml généré à partir de l'API JSON Open-Meteo !")
    else:
        print("Erreur lors de l'appel API :", response.status_code, response.text)

if __name__ == "__main__":
    get_weather_xml()
