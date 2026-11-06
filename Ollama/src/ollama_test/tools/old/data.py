from ...Class.classlist import *
from .Find_Equiv import Recherche_substitut_digikey
import re
from .query_AI import AI_query_mpn

def is_likely_mpn(word):
    """Vérifie si un mot ressemble à un MPN (Lettres + Chiffres, taille > 4)"""
    if len(word) < 5 or len(word) > 30:
        return False
    # Contient au moins une lettre et au moins un chiffre
    if not (re.search(r'[0-9]', word)):
        return False
    return True

def extract_mpns(strings_list:str,model:str):
    extracted_mpns = []
    try: 
      #1 ligne = 1 MPN
      for line in strings_list:
        #Nettoyage caractères inutiles
        line= re.sub(r'[:;$@}{#¤£&"|`^=+§*_]', ' ', line)
        words = re.split(r'[\s,]+', line)
        # Cas 1 : Un seul mot dans la ligne
        if len(words)==1:
          extracted_mpns.append(words[0])
          continue

        potential_mpns = [w for w in words if is_likely_mpn(w)]    
        if len(potential_mpns) == 1:
            extracted_mpns.append(potential_mpns[0])
            continue
        print(f"[{line}] -> Délégation à l'IA...")
        extracted_mpns.extend(AI_query_mpn(line,model))
         
          
      
      return {"Status" : "Success", "content" : list(dict.fromkeys(extracted_mpns))}
    except Exception as e:
              return {"Status" : "Failed", "content" : str(e)}


#TROUVER COMPOSANTS OBSOLETES RESULTATS ANALYSES
def find_obs(analyse:dict[str,ResultAllProduct]):
  dico_obs=[]
  try:
    for ref,info in analyse.items():
      
      try:
        for elem in info.liste_products.values():
          description = elem.techniques[0].Description
      except Exception as e:
        description = ""    
      if info.main.Statut_Global.Consensus !="Actif":
        if info.main.Equivalents_Suggeres == []:
          liste = Recherche_substitut_digikey(ref)
          if liste["Status"]=="Failed":
            dico_obs.append({'ref':ref,"Equiv":[],"description":description})
          else:
            dico_obs.append({'ref':ref,"Equiv":liste["content"],"description":description})
        else :
          dico_obs.append({'ref':ref,"Equiv":info.main.Equivalents_Suggeres,"description":description})

    return {"Status" : "Success" , "content" : dico_obs}
  except Exception as e:
    return {"Status" : "Failed" , "content" : f"Analyse de BOM échoué : {e}"}


if __name__ == "__main__" :
  result = {'SDR08540M3-01': ResultAllProduct(main=main(Fabricant='TDK', Fiche_Technique='https://product.tdk.com/en/system/files?file=dam/doc/product/sw_piezo/sw_piezo/em-buzzer/catalog/electromagnetic_buzzer_sd_en.pdf', Equivalents_Suggeres=[], Statut_Global=StatutGlobal(Consensus='Obsolète', Details_Distributeurs={'DigiKey': 'Obsolète', 'Mouser': 'Obsolète', 'Farnell': 'Obsolète'})), liste_products={'SDR08540M3-01': ResultFabProduct(techniques=[Tech(Description='Buzzers Transducteur, commande externe Magnétique 3 V 85mA 2,67kHz 88dB à 3V, 10cm Montage en surface Plots de brasage', Rohs='Conforme à RoHS\xa03', Reach='voir Datasheet', Temp_fonc='-40°C ~ 85°C', Temp_stock='≤30°C', humidity='≤ 85% RH', Floor_life='Illimité', boitier='voir Datasheet', Dimensions='0,335po L x 0,335po l (8,50mm x 8,50mm)')], offres=[Offres(Distributeur='DigiKey', Conditionnement='Bande et bobine', Stock=0, MOQ=1.0, Prix_Unitaire='N/A'), Offres(Distributeur='DigiKey', Conditionnement='Bande coupée (CT)', Stock=0, MOQ=1.0, Prix_Unitaire='N/A'), Offres(Distributeur='DigiKey', Conditionnement='Digi-Reel® (+5.5€)', Stock=0, MOQ=1.0, Prix_Unitaire='N/A')])})}
  print(find_obs(result))