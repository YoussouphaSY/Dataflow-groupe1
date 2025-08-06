import requests
import json

url="https://semantic.csr.unibo.it/morefarming/ndvi_single_pixel.php"
response= requests.get(url)

data=response.json()
print(data)

with open("stockage_data/api.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

print("donnee api stocké dans le fichier json réussi")
