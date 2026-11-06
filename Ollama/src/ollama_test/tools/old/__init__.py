


from dotenv import load_dotenv
from .build_liste_comp import analyse_liste
from .utils_excel import extraire_colonnes,extraire_liste_colonne,exporter_excel
from .data import extract_mpns,find_obs
from .query_AI import *
from pathlib import Path
import time
import datetime as dt
import os
load_dotenv()

def main(file_path:Path,output_path:Path,model:str='qwen3.5:2b'):

  #1. Extraction des colonnes du fichier Excel
  message = extraire_colonnes(file_path=file_path)
  if message.get("Status","") == "Failed":
    return {"Status" : "Failed" , "content" : "Erreur Extraction colonnes"}
  
  #2. Extraction par IA de la colonne cible
  response = AI_query(message["content"],model)

  #Demande validation UTILISATEUR !!!!

  #3. Extraction des éléments de la colonne cible
  response = extraire_liste_colonne(file_path,response)
   
  if response.get("Status","") == "Failed":
    return {"Status" : "Failed" , "content" : "Erreur Extraction éléments colonne cible"}

  #4. Nettoyage des éléments pour identifier uniquement les refs fabricants
  nb_ligne_init =len(response["content"])
  response = extract_mpns(response["content"],model)
  nb_ligne_identified =len(response["content"])
  if response.get("Status","") == "Failed":
    return {"Status" : "Failed" , "content" : "Erreur Extraction des mpn"}
  print(response["content"])
  response = analyse_liste(response["content"])
  if response.get("Status","") == "Failed":
    return {"Status" : "Failed" , "content" : f"Erreur Analyse BOM"}
  nb_ligne_success = len(response["content"].keys())

  #DEMANDER à l'UTILISATEUR DE CORRIGER SES MPN POUR COMPLETER LA RECHERCHE : CHOIX DE PASSER 


  #TROUVER COMPOSANTS OBSOLETES ET FAIRE RECHERCHE

  

#   mes_metadonnees = {
#     'Projet': 'Analyse BOM',
#     'Auteur': 'AUGER Alexis',
#     'Date d\'exécution': str(dt.datetime.now().strftime("%d-%m-%Y")),
#     'Fichier source': str(os.path.basename(file_path)),
#     'Modèle IA': f"{model} (Local)",
#     'Nombre de lignes de la colonne MPN du Fichier Source': nb_ligne_init,
#     'Nombre de MPN identifié(s)' : nb_ligne_identified,
#     'Nombre de MPN traité(s) avec succès' : nb_ligne_success,
#     'Nombre de MPN ayant rencontré(s) une erreur' : nb_ligne_identified-nb_ligne_success,
#     'Taux de réussite' : f"{round(nb_ligne_success/nb_ligne_identified * 100,ndigits=2)} %"

# }
#   chemin = exporter_excel(response["content"],mes_metadonnees,output_path)

#   #6. Nettoyer les données pour ne garder que les composants non actifs
#   # response = find_obs(response["content"])

  return {"Status" : "Success" , "content" : "chemin"}







if __name__=="__main__":
  
  debut = time.time()

  # file_path=Path("C:/Users/alexis.auger/Documents/taff/Projet_BOM/BOM.xlsx")
  # file_path = Path("C:/Users/alexis.auger/Documents/GitHub/Ollama/src/assets/1355LC001_03.xlsx")
  Excel_path = Path("C:/Users/alexis.auger/Documents/GitHub/Ollama/src/assets/TEst.xlsx")
  file_path = Path("C:/Users/alexis.auger/Documents/GitHub/Ollama/src/assets/1355LC001_03.xlsx")
  print(main(file_path,Excel_path))
  #Réponse de find_obs
  # dico = {'Status': 'Success', 'content': [{'ref': 'R-6002', 'Equiv': ['R6002END3TL1', 'R6002ENHTB1', 'LR600240D25R', 'LR600240D40RH', 'LR600240D40H', 'TBC7-22-00-62', 'LR600240D40R', 'MF-R600', 'R6002JND4TL1', 'KABR600 2R2 J', 'KABR600 27R J', 'R6002HF-PC', 'LR600240D25H', 'LR600240D40', 'CUSA-TR60-02-2000-TH67', 'MF-R600-2', 'CB1-600G', 'IP-R6002', 'MF-R600-AP', 'LR600240D25', 'RDD023N50TL', 'KABR600 22R J', 'R6002HF', 'MF-R600-2-14', 'BSS138WAHZGT106', 'R6002']}, {'ref': 'BAS116T,115', 'Equiv': ['771-BAS716-T/R']}, {'ref': 'IRLML2502TRPBF', 'Equiv': ['DMG2302U-7', 'DMG3414U']}, {'ref': '1355PCB001', 'Equiv': None}, {'ref': 'SDR08540M3-01', 'Equiv': ['CSS-73B16K-SMT']}, {'ref': 'RFD21733', 'Equiv': None}, {'ref': '1355CI001', 'Equiv': None}, {'ref': '1355ET002', 'Equiv': None}, {'ref': '1355ET001', 'Equiv': None}, {'ref': 'THT-38-727-10', 'Equiv': ['THT-38-797-10']}]}

  fin = time.time()

  print(f"Temps Query : {round(fin-debut)} s")

