from seleniumbase import SB
from curl_cffi import requests as rq
import requests
from unidecode import unidecode

from mcp.server import MCPServer
import os
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify as md
import re
from urllib.parse import urljoin

mcp = MCPServer("Devis_MCP")

#Optionnel comm ressources car mal formatée
@mcp.resource(uri="file///categories/")
def get_instrument_categories():
    chemin =Path("./Ressources/")
    fichiers = os.listdir(path=chemin)
    response = ""
    for fichier in fichiers:
        with open(os.path.join(chemin,fichier),'r',encoding="utf-8") as f:
            if response=="":
                response += f"============= Website : {fichier[:-4]}============\n" + f.read()
            else:
                response += f"\n\n=============Website : {fichier[:-4]}============\n" + f.read()
    return response

def search_website_by_infos(name_website:str,name_category:str,name_sub_category:str):
    url=""  
    if "rs-online" in name_website.lower():
        url = f"https://fr.rs-online.com/web/c/test-mesure/{unidecode(name_category.replace(" ","-").lower())}/{unidecode(name_sub_category.replace(" ","-").lower())}/"
    if "level" in name_website.lower():
        url = f"https://www.leveldevelopments.com/products/{unidecode(name_category.replace(" ","-").lower())}/{unidecode(name_sub_category.replace(" ","-").lower())}/"
    if "imada" in name_website.lower():
        url = f"https://imada.com/product-category/{unidecode(name_category.replace(" ","-").lower())}/{unidecode(name_sub_category.replace(" ","-").lower())}/"
    if "keyence" in name_website.lower():
        url = f"https://www.keyence.com/products/{unidecode(name_category.replace(" ","-").lower())}/{unidecode(name_sub_category.replace(" ","-").lower())}/"
    if "sensel" in name_website.lower():
        url = f"https://sensel-measurement.fr/en/{unidecode(name_sub_category.replace(" ","-").lower())}/"
    return search_website_by_url(url)

#-------------------OUTIL Recherche --------------------------

@mcp.tool()
def search_website_by_url(url:str):
    #Requête
    try : 

        #Requête
        request = rq.get(
            url, 
            impersonate="chrome116",
            timeout=15.0
        )
        
        if request.status_code in [403]:
            html_brute = extraire_page_rs_online(url)     

        elif request.status_code==200:
            html_brute= request.text

        else:
            return f"Erreur requête Website"
            
        # result_propre = BeautifulSoup(html_brute,"html.parser")
        # for a_tag in result_propre.find_all("a", href=True):
        #     a_tag["href"] = urljoin(url, a_tag["href"])
        # #Suppression
        
        # menus_parasites = result_propre.find_all(["nav", "aside","script", "style", "footer","header"]) # Les balises de menu classiques
        # elem_a_garder = result_propre.find("div",class_="ca-mega-menu level-1")
        # if elem_a_garder and url=="https://www.chauvin-arnoux.com/fr/":
        #     elem_a_garder.extract()
        # menus_parasites += result_propre.find_all("div", class_=["print:hidden","ensBannerContainer","flex flex-col gap-4 py-6 legacy-container","cookie-notice","info_customer_log_to_display_price","cl-table","block-categories", "theme-options"]) 
        # menus_parasites += result_propre.find_all("div", id=["column-left", "column-right", "sidebar","header_menu","footer","header","header_mobile_menu"])
        # menus_parasites += result_propre.find_all("section", class_=["prd-disclosure","bloc-banner-slider theme-light","bloc-top-news theme-transparent  ","bloc-reinsurance all","bloc-solutions","bloc-certification theme-default","prefooter theme-group"])
        # for element in menus_parasites:
        #     element.decompose()
        # if elem_a_garder:
        #         result_propre.append(elem_a_garder)
        





        # for tr in result_propre.find_all("tr"):
        #     Show_url=True
        #     for a in tr.find_all("a"):
        #         if "cartButton" in a.get("class", []):
        #             a.decompose()
        #         else:
        #             if Show_url: 
        #                 Show_url=False
        #             else:
        #                 a.unwrap()
                        
        # #Conversion Markdown sans les images et les espaces inutiles    
        # texte_propre = md(str(result_propre), strip=['img'])
        # texte_propre = re.sub(r'\n{3,}', '\n\n', texte_propre)
        # texte_propre= re.sub(r'\[?\(?(https?://[^\)\]]+)\)?\]?\(\1\)', r'\1', texte_propre)
        result_propre = BeautifulSoup(html_brute, "html.parser")
        # return(md(str(result_propre)))
        elem_a_garder = None
        if "chauvin-arnoux.com" in url:
            elem_a_garder = result_propre.find("div", class_="ca-mega-menu level-1")
            if elem_a_garder:
                elem_a_garder.extract()

        selecteurs = [
            "nav", "aside", "script", "style", "footer", "header", "noscript",
            ".print\:hidden", ".ensBannerContainer", ".legacy-container", ".cookie-notice", 
            ".info_customer_log_to_display_price", ".cl-table", ".block-categories", ".theme-options",
            "#column-left", "#column-right", "#sidebar", "#header_menu", "#footer", "#header", "#header_mobile_menu",
            "section.prd-disclosure", "section.bloc-banner-slider", "section.bloc-top-news", 
            "section.bloc-reinsurance", "section.bloc-solutions", "section.bloc-certification", "section.prefooter"
        ]
        for element in result_propre.select(", ".join(selecteurs)):
                element.decompose()
        if elem_a_garder:
            result_propre.append(elem_a_garder)
        for tr in result_propre.find_all("tr"):
            premier_lien_vu = False   
            for a in tr.find_all("a"):
                if "cartButton" in a.get("class", []):
                    a.decompose()
                elif not premier_lien_vu:
                    if a.get("href"):
                        a["href"] = urljoin(url, a["href"])
                    premier_lien_vu = True
                else:
                    a.unwrap()

        for a in result_propre.find_all("a", href=True):
            a["href"] = urljoin(url, a["href"])

        texte_propre = md(str(result_propre), strip=['img'], heading_style="ATX")
        texte_propre = re.sub(r'\n{3,}', '\n\n', texte_propre)
        texte_propre = re.sub(r'\[?\(?(https?://[^\)\]]+)\)?\]?\(\1\)', r'\1', texte_propre)
        texte_propre = texte_propre.strip()

        return texte_propre.strip()
        
    except Exception as e: 
        return f"Erreur requête Website {url} : {e}"

def extraire_page_rs_online(url: str) -> str:
    with SB(uc=True, locale="en",headless=True,block_images=True) as sb:
        try:
            sb.activate_cdp_mode()
            sb.goto(url,)
            sb.sleep(2)
            result = sb.get_page_source()
            return result
        except :
            return ""

if __name__ == "__main__":
    # print(search_website_by_infos("rs-online","Mesures de pressions","Calibrateurs de pression"))
    # extraire_page_rs_online("https://fr.rs-online.com/web/c/test-mesure/mesures-de-pressions/calibrateurs-de-pression/")
    # print(extraire_page_rs_online("https://fr.rs-online.com/web/c/test-mesure/mesures-de-pressions/calibrateurs-de-pression/"))
    # print(search_website_by_url("https://imada.com/product-category/"))
    # print(search_website_by_infos("imada","Torque Testers","Digital Torque Screwdrivers"))

    # print("============")
    print(search_website_by_url("https://imada.com/product-category/force-displacement-testers/"))