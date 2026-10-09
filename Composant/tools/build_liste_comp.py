from tools.API_Distrib import *
import concurrent.futures
import time
from tools.classlist import ResultAllProduct
from collections import Counter

#Création JSON unique pour un produit
def build_unified_json(mpn,token_digykey,Actif,Rohs,Type_Research)->ResultAllProduct:

    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_dk = executor.submit(query_digikey, mpn,token_digykey,Actif,Rohs,Type_Research)
        future_ms = executor.submit(query_mouser, mpn,Actif,Rohs,Type_Research)
        future_fn = executor.submit(query_farnell, mpn,Actif,Rohs,Type_Research)
        future_fu = executor.submit(query_future_electronics, mpn,Actif,Rohs,Type_Research)
        
        #Attente des API
        results["DigiKey"] = future_dk.result()
        results["Mouser"] = future_ms.result()
        results["Farnell"] = future_fn.result()
        results["Future_Electronics"] = future_fu.result()
    valid_results = {dist: data for dist, data in results.items() if data and "Erreur" not in data}
    if not valid_results:
        return None

    # Agrégation des informations générales
    first_valid = list(valid_results.values())[0]
    fabricant = first_valid.get("fabricant", "")
    datasheet = next((data["datasheet"] for data in valid_results.values() if data.get("datasheet")), "")

    # Calcul du consensus des statuts
    status_details = {dist: normalize_status(data["status"]) for dist, data in valid_results.items()}
    status_counts = Counter(status_details.values())
    
    # TrouveTraitér le statut majoritaire
    consensus = ("Non Recommandé" if ((len(status_counts)==len(status_details.keys())) and (len(status_details.keys())>1)) else status_counts.most_common(1)[0][0]) if status_counts else "Inconnu"
    alerte_conflit = len(status_counts) > 1 # Vrai s'il y a plus d'un type de statut renvoyé
    # Regroupement de toutes les offres
    toutes_offres = []
    toutes_alternatives = set()
    for data in valid_results.values():
        toutes_offres.extend(data.get("offres", []))
        for alt in data.get("alternatives", []):
                    if alt:
                        toutes_alternatives.add(alt)


    Tableau_ref={"main":{},"liste_products":{}}
    Tableau_ref["main"]["Fabricant"]=fabricant
    Tableau_ref["main"]["Equivalents_Suggeres"]=list(toutes_alternatives)
    Tableau_ref["main"]["Statut_Global"]=  {
            "Consensus": consensus,
            "Alerte_Conflit": alerte_conflit,
            "Details_Distributeurs": status_details
        }
    if datasheet.startswith("//"):
        datasheet = "https:" + datasheet
    Tableau_ref["main"]["Fiche_Technique"]=datasheet
    offres = toutes_offres
    liste_ref=[]
    for offre in offres:
        chargement = "voir Datasheet"
        distri = offre["Distributeur"]
        ref_dist = offre["REF"]
        Temp_fonc = chargement if offre["Temp_fonc"]=="" else offre["Temp_fonc"]
        Temp_Stock = chargement if offre["Temp_stock"]=="" else offre["Temp_stock"]
        humidity = chargement if offre["humidity"]=="" else offre["humidity"]
        Floor_life = chargement if offre["Floor_life"]=="" else offre["Floor_life"]
        Rohs = chargement if offre["Rohs"]=="" else offre["Rohs"]
        Reach = chargement if offre["Reach"]=="" or "Non" in offre["Reach"] else offre["Reach"]
        boitier = chargement if offre["boitier"]=="" else offre["boitier"]
        Dimensions = chargement if offre["Dimensions"]=="" else offre["Dimensions"]
        

        if ref_dist in liste_ref :
            if Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Temp_fonc"]==chargement: Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Temp_fonc"] = Temp_fonc
            if Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Temp_stock"]==chargement:Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Temp_stock"]=Temp_Stock
            if Tableau_ref["liste_products"][ref_dist]["techniques"][0]["humidity"]==chargement:Tableau_ref["liste_products"][ref_dist]["techniques"][0]["humidity"]=humidity
            if Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Rohs"]==chargement:Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Rohs"]=Rohs
            if Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Reach"]==chargement:Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Reach"]=Reach
            if Tableau_ref["liste_products"][ref_dist]["techniques"][0]["boitier"]==chargement: Tableau_ref["liste_products"][ref_dist]["techniques"][0]["boitier"]=boitier
            if Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Dimensions"]==chargement: Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Dimensions"]=Dimensions
            if Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Floor_life"]==chargement: Tableau_ref["liste_products"][ref_dist]["techniques"][0]["Floor_life"]=Floor_life
        else:
            liste_ref.append(ref_dist)
            Tableau_ref["liste_products"][ref_dist]={"techniques":[{
                "Temp_fonc":Temp_fonc,
                "Temp_stock":Temp_Stock,
                "humidity":humidity,
                "Floor_life":Floor_life,
                "Rohs":Rohs,
                "Reach":Reach,
                "boitier":boitier,
                "Dimensions":Dimensions,
            }],"offres":[]}

        packages = offre["Package"]
        for pkg in packages:
            
            Tableau_ref["liste_products"][ref_dist]["offres"].append({
                "Distributeur": distri,
                "Conditionnement": pkg["Conditionnement"],
                "Stock": pkg["Stock_Disponible"],
                "Prix_Unitaire" : " ".join([f"{p['Prix_Unitaire']} € (< {p['Quantite'] })" for p in pkg["Prix"]]) if pkg["Prix"] else "N/A" ,
                "MOQ" : pkg["MOQ"]
            })
    return Tableau_ref

def analyse_liste(liste_mpn,Actif,Rohs)->dict[str,ResultAllProduct] :
    token_digykey = get_digikey_token()
    resultats = {}# {"Actif":[],"Non Recommandé":[],"Obsolète":[],"Autre":[]}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # On lance l'analyse de plusieurs composants en même temps
            futures = {executor.submit(build_unified_json, mpn,token_digykey,Actif,Rohs,False): mpn for mpn in liste_mpn}
            i = 0
            for future in concurrent.futures.as_completed(futures):
                mpn = futures[future]
                try:
                    result = future.result()
                    if result:
                        resultats[mpn]=result
                        i+=1
                    logger.info(f"✅ Traité ({i}) : {mpn}")
                    # Délai vital pour lisser la charge et éviter les erreurs 429 de Mouser/Farnell
                    time.sleep(0.5) 
                    
                except Exception as e:
                    logger.info(f"❌ Erreur ({i}) sur {mpn}: {e}")
            return resultats


# def analyse_keywords(liste_keywords,Actif,Rohs) -> ResultAllProduct:
#     token_digykey = get_digikey_token()
#     result={}
#     try : 
#         result = build_unified_json(liste_keywords,token_digykey,Actif,Rohs,True)
        
#     except Exception as e:
#         logger.info(f"❌ Erreur sur {liste_keywords}: {e}")
   
#     return result

if __name__ == "__main__":
    load_dotenv()
    test = analyse_liste(["BRADY THT-38-727-10","SDR08540M3-01","BAS116T,115"],True,True)
    print(json.dumps(test, indent=2, ensure_ascii=False))