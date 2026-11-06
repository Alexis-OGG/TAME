import os
from seleniumbase import SB
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from seleniumbase import SB
BASE_URL = "https://www.digikey.fr"
import json
with open(os.path.join(os.path.dirname(__file__),"site.html"), "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

leaf_links = []

for a in soup.find_all("a", href=True):
    href = a["href"]

    # Une feuille DigiKey mène directement au filtre produits
    if "/products/filter/" in href:
        leaf_links.append(urljoin(BASE_URL, href))

# suppression des doublons en conservant l'ordre
leaf_links = list(dict.fromkeys(leaf_links))
taille = len(leaf_links)
print(f"{taille} feuilles trouvées")


descriptiuon= []
bug=[]
with SB(uc=True, test=True, guest=True) as sb:
    sb.activate_cdp_mode()
    for index,site in enumerate(leaf_links):
        try : 
            sb.goto(site+"?s=N4IgrCBcoA5QjAGhDOl4AYMF9tA")
            sb.sleep(1)
            toutes_les_divs = sb.find_elements("div.tss-css-7dp38y-productColExpandedDescription")
            for element in toutes_les_divs:
                    # Récupérer le texte
                    texte = element.text
                    descriptiuon.append(texte)
            print(f"{index+1}/{taille} : True")
        except:
             bug.append(site)
             print(f"{index+1}/{taille} : False")

with open("digikey_leaves.json", "w", encoding="utf-8") as f:
    json.dump(
        {"ref": list(set(descriptiuon)),"bug":bug},
        f,
        ensure_ascii=False,
        indent=4
    )