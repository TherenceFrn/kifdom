import requests
from bs4 import BeautifulSoup
import json
import os

# URL de la page à récupérer
url = "https://kifdom.com"

# Faire la requête GET
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text  # Contenu HTML de la page

    # Utiliser BeautifulSoup pour analyser le HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Trouver toutes les lignes (<tr>) dans le <tbody>
    rows = soup.select("tbody tr")

    # Structure pour stocker les données
    results = {"sites": []}

    # Parcourir les lignes et extraire les informations
    for row in rows:
        try:
            domain = row.select_one("td:nth-child(1) span").text.strip()
            kifrank = int(row.select_one("td:nth-child(2)").text.strip())
            price = row.select_one("td:nth-child(7)").text.strip()

            # Ajouter les données dans la structure
            results["sites"].append({
                "domain": domain,
                "kifrank": kifrank,
                "price": price
            })
        except Exception as e:
            print(f"Erreur lors de l'extraction d'une ligne : {e}")

    # Créer un dossier pour stocker les résultats
    os.makedirs("results", exist_ok=True)

    # Enregistrer les données dans un fichier JSON
    with open("results/sites_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print("Les données ont été enregistrées dans le fichier 'results/sites_data.json'.")
else:
    print(f"Erreur : {response.status_code}")
