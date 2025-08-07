import xml.etree.ElementTree as ET
import json

# Chemin vers ton fichier XML
xml_file = 'cooperatives.xml'
json_file = 'cooperatives.json'

# Parse le fichier XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Liste pour stocker les coopératives
cooperatives = []

# Parcours chaque élément <cooperative>
for coop in root.findall('cooperative'):
    data = {}
    for child in coop:
        data[child.tag] = child.text
    cooperatives.append(data)

# Écriture en JSON
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(cooperatives, f, ensure_ascii=False, indent=2)

print(f"Conversion terminée, fichier JSON créé : {json_file}")
