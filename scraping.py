import requests  
from bs4 import BeautifulSoup as bs
from statistics import median, mode
import pandas as pd
import re
headers = {
    "User-Agent": "Mozilla/5.0"
}

def scraper_villas_raw(nb_pages=1):
    base_url = "https://sn.coinafrique.com/categorie/villas?page="
    data = []

    for page in range(1, nb_pages + 1):
        url = base_url + str(page)
        try:
            response = requests.get(url)
            response.encoding = "utf-8"
            soup = bs(response.text, "html.parser")
            containers = soup.find_all("div", class_="col s6 m4 l3")

            for container in containers:
                try:
                    # Type d'annonce
                    type_annonce = container.find("p", class_="ad__card-description").a.text.strip().split()[0]

                    # Nombre de pièces
                    desc_tag = container.find("p", class_="ad__card-description")
                    nombre_pieces = None
                    if desc_tag:
                        pieces_element = desc_tag.a.text
                        match = re.search(r"(\d+)\s*pièces?", pieces_element.lower())
                        if match:
                            nombre_pieces = int(match.group(1))

                    # Prix
                    prix = None
                    prix_tag = container.find("p", class_="ad__card-price")
                    if prix_tag and prix_tag.a:
                        prix_text = prix_tag.a.text.strip().replace("CFA", "").replace(" ", "")
                        if prix_text.isdigit():
                            prix = int(prix_text)

                    # Adresse
                    adresse = container.find("p", class_="ad__card-location").span.text.strip()

                    # Image
                    lien_image = container.find("img")["src"]

                    data.append({
                        "Type annonce": type_annonce,
                        "Pièces": nombre_pieces,
                        "Prix": prix,
                        "Adresse": adresse,
                        "Image": lien_image
                    })

                except Exception as e:
                    print(f"Erreur dans une annonce : {e}")
                    continue

        except Exception as e:
            print(f"Erreur lors du chargement de la page {page} : {e}")
            continue

    return data  # Liste de dicts

import requests
from bs4 import BeautifulSoup as bs
import re

def scraper_terrains_raw(nb_pages=1):
    base_url = "https://sn.coinafrique.com/categorie/terrains?page="
    data = []

    for page in range(1, nb_pages + 1):
        url = base_url + str(page)
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = bs(response.content, "html.parser")
            containers = soup.find_all("div", class_="col s6 m4 l3")

            for container in containers:
                try:
                    # Prix
                    prix_tag = container.find("p", class_="ad__card-price")
                    prix = None
                    if prix_tag and prix_tag.a:
                        prix_text = prix_tag.a.text.strip().replace("CFA", "").replace(" ", "")
                        if prix_text.isdigit():
                            prix = int(prix_text)

                    # Adresse
                    adresse = container.find("p", class_="ad__card-location").span.text.strip()

                    # Image
                    lien_image = container.find("img")["src"]

                    # Superficie
                    superficie = None
                    desc = container.find("p", class_="ad__card-description")
                    if desc:
                        desc_text = desc.get_text().lower()
                        match = re.search(r"(\d+)\s*(?:m2|m²|mètre carré|mètres carrés)", desc_text)
                        if match:
                            superficie = int(match.group(1))

                    data.append({
                        "Superficie": superficie,
                        "Prix": prix,
                        "Adresse": adresse,
                        "Image": lien_image
                    })

                except Exception as e:
                    print(f"Erreur dans une annonce : {e}")
                    continue

        except Exception as e:
            print(f"Erreur lors du chargement de la page {page} : {e}")
            continue

    return data


def scraper_appartements_raw(nb_pages=1):
    base_url = "https://sn.coinafrique.com/categorie/appartements?page="
    data = []

    for page in range(1, nb_pages + 1):
        url = base_url + str(page)
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = bs(response.content, "html.parser")
            containers = soup.find_all("div", class_="col s6 m4 l3")

            for container in containers:
                try:
                    # Nombre de pièces
                    desc_tag = container.find("p", class_="ad__card-description")
                    nombre_pieces = None
                    if desc_tag and desc_tag.a:
                        text = desc_tag.a.text
                        match = re.search(r"(\d+)\s*pièces?", text.lower())
                        if match:
                            nombre_pieces = int(match.group(1))

                    # Prix
                    prix = None
                    prix_tag = container.find("p", class_="ad__card-price")
                    if prix_tag and prix_tag.a:
                        prix_text = prix_tag.a.text.strip().replace("CFA", "").replace(" ", "")
                        if prix_text.isdigit():
                            prix = int(prix_text)

                    # Adresse
                    adresse = container.find("p", class_="ad__card-location").span.text.strip()

                    # Image
                    lien_image = container.find("img")["src"]

                    data.append({
                        "Pièces": nombre_pieces,
                        "Prix": prix,
                        "Adresse": adresse,
                        "Image": lien_image
                    })

                except Exception as e:
                    print(f"Erreur dans une annonce : {e}")
                    continue

        except Exception as e:
            print(f"Erreur lors du chargement de la page {page} : {e}")
            continue

    return data