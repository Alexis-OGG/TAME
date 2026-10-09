
#Librairies
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import logging
import urllib.parse
import os 
from dotenv import load_dotenv
import json



logger = logging.getLogger(__name__)
#Mots-clés
Dico_MSL ={
  "MSL 1": {
    "Floor Life": "Illimité",
    "stockage" : "≤30°C",
    "humidite" : "≤ 85% RH",
    "Dry Pack Required": "No"
  },
  "MSL 2": {
    "Floor Life": "1 an",
    "stockage" : "≤30°C",
    "humidite" : "≤ 60% RH",
    "Dry Pack Required": "Yes"
  },
  "MSL 2a": {
    "Floor Life": "4 semaines",
    "stockage" : "≤30°C",
    "humidite" : "≤ 60% RH",
    "Dry Pack Required": "Yes"
  },
  "MSL 3": {
    "Floor Life": "168 heures (7 jours)",
    "stockage" : "≤30°C",
    "humidite" : "≤ 60% RH",
    "Dry Pack Required": "Yes"
  },
  "MSL 4": {
    "Floor Life": "72 heures (3 jours)",
    "stockage" : "≤30°C",
    "humidite" : "≤ 60% RH",
    "Dry Pack Required": "Yes"
  },
  "MSL 5": {
    "Floor Life": "48 heures (2 jours)",
    "stockage" : "≤30°C",
    "humidite" : "≤ 60% RH",
    "Dry Pack Required": "Yes"
  },
  "MSL 5a": {
    "Floor Life": "24 heures (1 jours)",
    "stockage" : "≤30°C",
    "humidite" : "≤ 60% RH",
    "Dry Pack Required": "Yes"
  },
  "MSL 6": {
    "Floor Life": "étuvage obligatoire",
    "stockage" : "",
    "humidite" : "",
    "Conditions": "Time on Label (TOL)",
    "Dry Pack Required": "Yes"
  }
}
     

def info_MSL(msl):

    if "1" in msl :
        return Dico_MSL["MSL 1"]
    if " 2" in msl :
        return Dico_MSL["MSL 2"]
    if "2a" in msl :
        return Dico_MSL["MSL 2a"]
    if "3" in msl :
        return Dico_MSL["MSL 3"]
    if "4" in msl :
        return Dico_MSL["MSL 4"]
    if " 5" in msl :
        return Dico_MSL["MSL 5"]
    if "5a" in msl :
        return Dico_MSL["MSL 5a"]
    if "6" in msl :
        return Dico_MSL["MSL 6"]
    else:
        return {}


def creer_session_resiliente():
    """Crée une session HTTP configurée pour réessayer automatiquement en cas d'échec."""
    session = requests.Session()
    
    # Configuration de la stratégie de Retry
    strategie = Retry(
        total=3,                # Nombre maximum de tentatives (3 retours d'erreur acceptés)
        backoff_factor=2,       # Attente exponentielle entre les essais : 2s, puis 4s, puis 8s...
        status_forcelist=[500, 502, 503, 504], # Codes HTTP déclenchant la nouvelle tentative
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"] # Crucial d'inclure POST pour Mouser et Digi-Key
    )
    
    # Application de la stratégie à la session
    adaptateur = HTTPAdapter(max_retries=strategie)
    session.mount("https://", adaptateur)
    session.mount("http://", adaptateur)
    
    return session

# Initialisation de vos sessions globales indestructibles
session_dk = creer_session_resiliente()
session_ms = creer_session_resiliente()
session_fn = creer_session_resiliente()
session_fe = creer_session_resiliente()

def get_digikey_token():
    """Récupère un nouveau jeton d'accès (Token) depuis la Sandbox Digi-Key."""
    url = "https://api.digikey.com/v1/oauth2/token"
    DIGIKEY_CLIENT_ID= os.getenv("DIGIKEY_CLIENT_ID")
    DIGIKEY_CLIENT_SECRET= os.getenv("DIGIKEY_CLIENT_SECRET")
    payload = {
        "client_id": DIGIKEY_CLIENT_ID,
        "client_secret": DIGIKEY_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = None
  
    try:
        
        response = requests.post(url, data=payload)

        token_data = response.json()
        return token_data.get("access_token")
    except requests.exceptions.RequestException as e:
        logger.info(f"Erreur lors de la récupération du token : {e}")
        if response is not None:
            logger.info("Détails :", response.text)
        return None

#API DIGIKEY
def query_digikey(mpn,token_digykey,Actif,Rohs,Type_Research):
    url = "https://api.digikey.com/products/v4/search/keyword"
    if token_digykey == None : return {"Erreur" : "Token API échoué OU Erreur réseau"}
    DIGIKEY_CLIENT_ID= os.getenv("DIGIKEY_CLIENT_ID")
    headers = {
        "Authorization": f"Bearer {token_digykey}",
        "X-DIGIKEY-Client-Id": DIGIKEY_CLIENT_ID,
        "X-DIGIKEY-Locale-Site": "FR", 
        "X-DIGIKEY-Locale-Language": "fr", 
        "X-DIGIKEY-Locale-Currency": "EUR",
        "Content-Type": "application/json"
    }
    payload = {
        "Keywords": mpn,
        "Limit" : 5, 
        "FilterOptions":{}
    }
    if Actif :
        payload["FilterOptions"]["LifecycleStatuses"] = ["Active"]
        payload["FilterOptions"]["SearchOptions"] = ["InStock"]
    if Rohs :
        payload["FilterOptions"]["RohsStatuses"] = ["RoHS Compliant"]

    try:

        res = requests.post(url, json=payload, headers=headers)
       
        if res.status_code in [429,401,403]: 

                return {"Erreur" : "Conexion API échoué"}
        data = res.json()
        parts = data.get('Products', [])
        # print(json.dumps(data, indent=2, ensure_ascii=False))        
        if not parts and data.get('ExactMatches'):
            parts = data.get('ExactMatches', [])
        
        if res.status_code == 200 and parts:
            toutes_offres = []
            fabricant = ""
            datasheet = ""
            status = "Unknown"
            boitier=""
            temp_fonc=""
            Dimensions=""
            for index, prod in enumerate(parts):
                # On récupère les informations génériques sur le premier composant valide
                if index == 0:
                    fabricant = prod.get("Manufacturer", {}).get("Name", "")
                    datasheet = prod.get("DatasheetUrl", "")
                    status_dict = prod.get("ProductStatus", {})
                    status = status_dict.get("Status", "Unknown") if isinstance(status_dict, dict) else "Unknown"
                # Extraction de toutes les variations (conditionnements) du composant
                
                MSL = info_MSL(prod.get("Classifications","").get("MoistureSensitivityLevel",""))

                touts_conditionnement = []
                for var in prod.get("ProductVariations", []):
                    conditionnement = var.get("PackageType", {}).get("Name", "Inconnu")
                    stock = var.get("QuantityAvailableforPackageType", 0)
                    # Ajout visuel des frais de bobinage si applicables
                    frais_reel = var.get("DigiReelFee", 0.0)
                    if frais_reel > 0:
                        conditionnement += f" (+{frais_reel}€)"
                    
                    # Construction de la grille tarifaire
                    prix_list = []
                    standard_pricing = var.get("StandardPricing", [])
                    for p in standard_pricing:
                        prix_list.append({
                            "Quantite": p.get("BreakQuantity"),
                            "Prix_Unitaire": p.get("UnitPrice")
                        })
                        
                    # Priorité au MOQ fourni dans la variation, sinon on prend le premier palier de prix
                    moq = var.get("MinimumOrderQuantity")
                    if not moq and standard_pricing:
                        moq = standard_pricing[0].get("BreakQuantity", 1)
                    elif not moq:
                        moq = 1
                        
                    touts_conditionnement.append({
                        "Conditionnement": conditionnement,
                        "Stock_Disponible": stock,
                        "MOQ": moq,
                        "Prix": prix_list,
                    })

                for param in prod.get("Parameters"):
                    valueLabel = param.get("ParameterText")
                    value = param.get("ValueText")
                    if value!="-" :
                        match valueLabel:
                            case "Température de fonctionnement":
                                temp_fonc = value
                            case "Boîtier":
                                boitier = value
                            case "Taille /dimension":
                                Dimensions = value
                        # touts_parameters.append({
                        #     "Nom" : valueLabel,
                        #     "Value" : value
                        # })

                toutes_offres.append({
                    "Distributeur": "DigiKey",
                    "REF" : prod.get("ManufacturerProductNumber"),
                    "Description" : prod.get("Description",{}).get("DetailedDescription","") ,
                    "Package" : touts_conditionnement,
                    "Rohs" : prod.get("Classifications","").get("RohsStatus",""),
                    "Reach" : prod.get("Classifications","").get("ReachStatus",""),
                    "boitier":boitier,
                    "Dimensions":Dimensions,
                    "Temp_fonc": temp_fonc,
                    "Temp_stock" : MSL.get("stockage",""),
                    "humidity": MSL.get("humidite",""),
                    "Floor_life" : MSL.get("Floor Life","")
                })

                
            return {
                "fabricant": fabricant,
                "datasheet": datasheet,
                "status": status,
                "offres": toutes_offres,
                "alternatives": [],
            }

    except Exception as e:
        logger.info(f" [Crash Python/Réseau] Erreur sur {mpn} : {e}")
        return {"Erreur" : f"Crash {mpn} : {e}"}

def query_digikey_sub(mpn,token_digykey):
    mpn_encode = urllib.parse.quote(mpn, safe='')
    url=f"https://api.digikey.com/products/v4/search/{mpn}/substitutions"
    if token_digykey == None : return {"Erreur" : "Token API échoué OU Erreur réseau"}
    headers = {
        "Authorization": f"Bearer {token_digykey}",
        "X-DIGIKEY-Client-Id": DIGIKEY_CLIENT_ID,
        "X-DIGIKEY-Locale-Site": "FR", 
        "X-DIGIKEY-Locale-Language": "fr", 
        "X-DIGIKEY-Locale-Currency": "EUR",
        "Content-Type": "application/json"
    }

    try:

        res = requests.get(url, headers=headers)
        print(res.json())
        if res.status_code in [429,401,403]: 
                return {"Erreur" : "Conexion API échoué"}
        data = res.json()
        parts = data.get('ProductSubstitutes', [])
        if res.status_code == 200 and parts!=[]:
            liste={}
            for index, part in enumerate(parts):
                liste[part.get("ManufacturerProductNumber","")] = part.get("SubstituteType","")
            return {mpn:liste}


    except Exception as e:
        logger.info(f" [Crash Python/Réseau] Erreur sur {mpn} : {e}")
        return {"Erreur" : f"Crash {mpn} : {e}"}


#API MOUSER
def query_mouser(mpn,Actif,Rohs,Type_Research):
    Search_Request = ""
    payload={}
    MOUSER_API_KEY= os.getenv("MOUSER_API_KEY")
    if Type_Research :
        url = f"https://api.mouser.com/api/v1/search/keyword?apiKey={MOUSER_API_KEY}"
        Search_Request="SearchByKeywordRequest"
        payload={
            Search_Request: {
                "keyword": mpn,
                "records": 5,
                "searchOptions": "2"
            }
        }
    else :
        url = f"https://api.mouser.com/api/v1/search/partnumber?apiKey={MOUSER_API_KEY}"
        Search_Request="SearchByPartRequest"
        payload={
                    Search_Request: {
                        "mouserPartNumber": mpn,
                        "searchOptions": "2"
                    }
                } 
    
    
    if Actif and Rohs:
            payload[Search_Request]["PartSearchOptions"] = "Active,RoHS"   
    elif Actif :
            payload[Search_Request]["PartSearchOptions"] = "Active"
    elif Rohs :
            payload[Search_Request]["PartSearchOptions"] = "RoHS"
    #print(payload)
    try:
        res = session_ms.post(url, json=payload, headers={'Content-Type': 'application/json'})
        # print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        donnees_json = res.json() or {}
        search_results = donnees_json.get('SearchResults') or {}
        parts = search_results.get('Parts') or []
        if res.status_code == 200 :
            # print(json.dumps(parts, indent=2, ensure_ascii=False))
            toutes_offres = []
            fabricant = ""
            datasheet = ""
            status = "Unknown"
            alternatives = set()
            Main_info = True #Récupère les Principales infos de l'ensenmble des produits
            for  prod in parts:
                boitier=""
                temp_fonc=""
                temp_stock=""
                humidity=""
                Dimensions=""
                ManufacturerPartNumber = prod.get("ManufacturerPartNumber")
                if ManufacturerPartNumber == "N/A":
                    continue

                if not ManufacturerPartNumber.lower().startswith(mpn.lower()):
                    alternatives.add(ManufacturerPartNumber)
                    continue
                if Main_info :
                    fabricant = prod.get("Manufacturer", "")
                    datasheet = prod.get("DataSheetUrl", "")
                    status = prod.get("LifecycleStatus", "") or "Active"
                    spec = prod.get("Description",None)
                    Main_info = False
                remplacement = prod.get("SuggestedReplacement", "")
                if remplacement:
                    alternatives.add(remplacement)
                    
                conditionnement = "Standard"
                attributes = prod.get("ProductAttributes", [])
                cond_list = [attr.get("AttributeValue") for attr in attributes if attr.get("AttributeName") == "Conditionnement"]
                if cond_list:
                    # Si Mouser liste plusieurs conditionnements (ex: Reel / Cut Tape), on les fusionne
                    conditionnement = " / ".join(cond_list)

                stock_str = str(prod.get("AvailabilityInStock", "0") or "0")
                stock_clean = ''.join(filter(str.isdigit, stock_str))
                stock = int(stock_clean) if stock_clean else 0


                

                moq_str = str(prod.get("Min", "1") or "1")
                moq_clean = ''.join(filter(str.isdigit, moq_str))
                moq = int(moq_clean) if moq_clean else 1
                
                prix_list = []
                for p in prod.get("PriceBreaks", []):
                    try:
                        price_clean = p.get("Price", "0").replace('€', '').replace('$', '').replace(' ', '').replace(',', '.')
                        prix_list.append({
                            "Quantite": p.get("Quantity"),
                            "Prix_Unitaire": float(price_clean)
                        })
                    except ValueError:
                        continue
                
                # # Ajout de l'offre uniquement s'il y a un prix ou du stock
                if  normalize_status(status) =="Actif" and prod.get("AvailabilityInStock")==None:
                    toutes_offres.append({
                        "Distributeur": "Mouser",
                        "REF" : prod.get("ManufacturerPartNumber"),
                        "Description" : prod.get("Description"),
                        "Package": [{
                            "Conditionnement" : conditionnement,
                            "Stock_Disponible": stock,
                            "MOQ": moq,
                            "Prix": prix_list
                            }],
                        "Rohs" : prod.get("ROHSStatus",""),
                        "Reach" : prod.get("ReachStatus",""),
                        "Floor_life":"",
                        "boitier":boitier,
                        "Dimensions":Dimensions,
                        "Temp_fonc": temp_fonc,
                        "Temp_stock" : temp_stock,
                        "humidity": humidity
                        
                    })
            
            return {
                "fabricant": fabricant,
                "datasheet": datasheet,
                "status": status,
                "offres": toutes_offres,
                "alternatives": list(alternatives),
                
            }

        
        if res.status_code in [429,401,403]: 

            return {"Erreur" : "Conexion API échoué"}
        return {"Erreur" : "Aucun produits trouvés"}
        
    except Exception as e:
            logger.info(f" [Crash Python/Réseau] Erreur sur {mpn} : {e}")
            return {"Erreur" : f"Crash : {e}"}

#API FERNELL
def query_farnell(mpn,Actif,Rohs,Type_Research):
    # Endpoint de l'API element14/Farnell
    url = "https://api.element14.com/catalog/products"
    FARNELL_API_KEY= os.getenv("FARNELL_API_KEY")
    params = {
           # Recherche par référence fabricant
        "storeInfo.id": "fr.farnell.com",       # Boutique France (Euros)
        "resultsSettings.offset": 0,  
        "resultsSettings.numberOfResults" : 5,
        "resultsSettings.responseGroup": "large", # Nécessaire pour prix et stock
        "callInfo.responseDataFormat": "json",  # CRUCIAL : Force la réponse en JSON
        "callInfo.apiKey": FARNELL_API_KEY,
    }
    if Type_Research :
        params["term"] =  f"any:{mpn}" 
    else :
        params["term"] =  f"manuPartNum:{mpn}"

    if Actif :
        params["lifecycleState"]="Active"
    if Rohs :
        params["rohsStatusCode"]="ROHS_COMPLIANT"
    
    headers = {
        "Accept": "application/json"
    }
    
    try:
        res = session_fn.get(url, params=params,headers=headers)
        if res.status_code == 200:
            data = res.json()
            # print(json.dumps(data, indent=2, ensure_ascii=False))
            search_return = data.get("manufacturerPartNumberSearchReturn", {}) or {}
            parts = search_return.get("products", [])
    
            if not parts and data.get("keywordSearchReturn"):
                parts = data.get("keywordSearchReturn", {}).get("products", [])
                
            if parts:
                toutes_offres = []
                alternatives = set()
                fabricant = ""
                datasheet = ""
                status = "Unknown"

                for index, prod in enumerate(parts):
                    ref_farnell = prod.get("translatedManufacturerPartNumber", "")
                    if not ref_farnell.lower().startswith(mpn.lower()):
                        alternatives.add(f"{ref_farnell}")
                        continue

                    if index == 0:
                        fabricant = prod.get("vendorName", "")
                        datasheets_list = prod.get("datasheets", [])
                        if datasheets_list:
                            datasheet = datasheets_list[0].get("url", "")
                        
                        status = prod.get("productStatus", "")
                    
                    conditionnement = prod.get("unitOfMeasure")
                    if prod.get("packaging"):
                        conditionnement += f" ({prod.get('packaging')})"

                    is_reeling = prod.get("reeling", False)
                    if is_reeling:
                        conditionnement += " [+ Option Reeling/Mini-Bobine]"

                    stock_info = prod.get("stock", {})
                    stock_dispo = int(stock_info.get("level", 0))
                    boitier=""
                    temp_fonc=""
                    Dimensions=""
                    rohs = ""
                    reach= ""
                    MSL={}
                    for param in prod.get("attributes"):
                        valueLabel = param.get("attributeLabel")
                        value = param.get("attributeValue")
                        if "min" in valueLabel: temp_fonc = value + temp_fonc
                        match valueLabel:
                            case "rohsCompliant":
                                rohs = value
                            case "Boîtier de condensateur":
                                boitier=value
                            case "Température d'utilisation Max.":
                                temp_fonc = temp_fonc + " to " + value +" "+ param.get("attributeUnit","")
                            case "Largeur du produit":
                                Dimensions = Dimensions + " x " + value +" "+ param.get("attributeUnit")
                            case "Longueur du produit":
                                Dimensions =  value+Dimensions
                            case "MSL":
                                MSL= info_MSL(value)


                                 

                        # if valueLabel not in ["tariffCode","euEccn", "Gamme de produit" ,"isCanonical","MSL","productTraceability","usEccn"] and value!="-" :
                        #     #Récupération ROSH:
                        #     if valueLabel =="rohsCompliant":
                                
                        #     else : 
                        #         touts_parameters.append({
                        #             "Nom" : valueLabel,
                        #             "Value" : value,
                        #         })
                    moq = int(prod.get("minOrderQty", 1))
                    
                    prix_list = []
                    for price_break in prod.get("prices", []):
                        try:
                            prix_list.append({
                                "Quantite": int(price_break.get("from", 1)),
                                "Prix_Unitaire": float(price_break.get("cost", 0))
                            })
                        except (ValueError, TypeError):
                            continue
                            
                    # # Ajout de l'offre si elle est valide
                    if  normalize_status(status) =="Actif" :
                        toutes_offres.append({
                            "Distributeur": "Farnell",
                            "REF" : ref_farnell,
                            "Description" : prod.get("displayName","") ,
                            "Package" :[{
                                "Conditionnement" : conditionnement,
                                "Stock_Disponible": stock_dispo,
                                "MOQ": moq,
                                "Prix": prix_list,
                            }],
                            "Rohs" : rohs,
                            "Reach" : reach,
                            "boitier":boitier,
                            "Dimensions":Dimensions,
                            "Temp_fonc": temp_fonc,
                            "Temp_stock" : MSL.get("stockage",""),
                            "humidity": MSL.get("humidite",""),
                            "Floor_life" : MSL.get("Floor Life","")
                        })
                
                return {
                    "fabricant": fabricant,
                    "datasheet": datasheet,
                    "status": status,
                    "offres": toutes_offres,
                    "alternatives": list(alternatives),
                }
        elif res.status_code in [429,401,403]: 
            return {"Erreur" : "Conexion API échoué ou produit non trouvé"}
        return {"Erreur" : "Aucun produits trouvés"}
    except Exception as e:
        logger.info(f" [Crash Python/Réseau] Erreur sur {mpn} : {e}")
        return {"Erreur" : f"Conexion API échoué {e}"}

def query_future_electronics(mpn, Actif, Rohs, Type_Research):
    # L'endpoint exact dépend de la version de l'API Future Electronics (v1/v2)
    url = "https://api.futureelectronics.com/api/v1/pim-future/lookup" 
    FUTURE_ELECTRONICS_KEY= os.getenv("FUTURE_ELECTRONICS_KEY")

    # Configuration de l'authentification (souvent via un header x-api-key)
    headers = {
        "Accept": "application/json",
        "x-orbweaver-licensekey": FUTURE_ELECTRONICS_KEY, # Assurez-vous que cette variable est définie
        "Content-Type": "application/json"
    }
    
    # Paramétrage de la requête
    params = {
        "part_number":mpn,
        "lookup_type" : "starts_with"
    }

        
    try:
        # L'API Future utilise souvent GET pour la recherche, mais vérifiez si votre version nécessite un POST avec un payload JSON.
        res = session_fe.get(url, params=params, headers=headers)

        if res.status_code == 200:
            data = res.json()
            # print(json.dumps(data, indent=2, ensure_ascii=False))  
            # La clé exacte ('offers', 'parts', 'results') dépend de la documentation de votre accès Future
            parts = data.get("offers", []) 
            
            if parts:
                toutes_offres = []
                alternatives = set()
                fabricant = ""
                datasheet = ""
                status = "Unknown"
                
                for index, prod in enumerate(parts):
                    # Mapping des clés spécifiques à Future Electronics
                    ref_future = prod.get("part_id", "").get("mpn","")
                    
                    if not ref_future.lower().startswith(mpn.lower()):
                        alternatives.add(f"{ref_future}")
                        continue

                    if index == 0:
                        datasheet = prod.get("documents", [])[0].get("url","")
                    
                    
                    # # Récupération du stock
                    stock_dispo = prod.get("quantities", {}).get("quantity_available",0)

                    # Extraction des attributs techniques
                    rohs_status = ""
                    reach_status = ""
                    
                    for param in prod.get("part_attributes", []):
                        valueLabel = param.get("name")
                        
                        value = param.get("value")
                        match valueLabel:
                            case "quantity_minimum":
                                moq = int(value)
                                continue
                            case "packageType":
                                conditionnement = value
                                continue
                            case "productLifeCycle":
                                status = value
                                continue
                            case "rohs" :
                                rohs_status = value
                                continue
                            case "manufacturerName" :
                                if index==0 : fabricant = value
                                continue
                            case "description (en)":
                                description = value
                    
                    # Extraction de la grille tarifaire
                    prix_list = []
                    for price_break in prod.get("pricing", []):
                        try:
                            prix_list.append({
                                "Quantite": int(price_break.get("quantity_from", 1)),
                                "Prix_Unitaire": float(price_break.get("unit_price", 0))
                            })
                        except (ValueError, TypeError):
                            continue
                            
                    # Ajout de l'offre si le stock est valide
                    if normalize_status(status) =="Actif":
                        toutes_offres.append({
                            "Distributeur": "Future Electronics",
                            "REF": ref_future,
                            "Description" :description, 
                            "Package": [{
                                "Conditionnement": conditionnement,
                                "Stock_Disponible": stock_dispo,
                                "MOQ": moq,
                                "Prix": prix_list,
                            }],
                            "Rohs": rohs_status,
                            "Reach": reach_status,
                            "Temp_fonc":"",
                            "Temp_stock":"",
                            "humidity":"",
                            "Floor_life":"",
                            "Dimensions":"",
                            "boitier":""
                        })
                
                return {
                    "fabricant": fabricant,
                    "datasheet": datasheet,
                    "status": status,
                    "offres": toutes_offres,
                    "alternatives": list(alternatives),
                }
            else:
                return {"Erreur": f"Aucun Offres disponibles pour le produit {mpn})"}
        elif res.status_code in [401, 403, 429,406]: 
            return {"Erreur": f"Connexion API échouée (Erreur {res.status_code})"}


    except Exception as e:
        logger.info(f" [Crash Python/Réseau] Erreur sur {mpn} chez Future Electronics : {e}")
        return {"Erreur": f"Connexion API échouée {e}"}

#Normalistion status Produits
def normalize_status(raw_status):
    if not raw_status: return "Inconnu"
    s = str(raw_status).lower()
    if "direct_ship" in s or "acti" in s or "production" in s or "stocked" in s or 'new' in s: return "Actif"
    if "obsol" in s or "eol" in s or "fin de cycle" in s or "end of life"  in s or 'no_longer_manufactured' in s or "restricted" in s: return "Obsolète"
    if "nrnd" in s or "pas pour les nouvelles conceptions" in s or "not recommended for new designs" in s or"not recommended" in s: return "Non Recommandé"
    return "Autre"


if __name__ == "__main__":

    DIGIKEY_CLIENT_ID= os.getenv("DIGIKEY_CLIENT_ID")
    DIGIKEY_CLIENT_SECRET= os.getenv("DIGIKEY_CLIENT_SECRET")
    test = query_farnell("SDR08540M3-01",True,True,False)
    print(json.dumps(test,indent=2,ensure_ascii=False))