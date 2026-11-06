import concurrent.futures
from .Offre import Offre
from ..tools.API_Distrib import *
from .Component import Component
import re

def find_consensus(status_details):
    
    liste_state=status_details.values()
    if "Obsolète" in liste_state:
        return "Obsolète"
    if "Non Recommandé" in liste_state:
        return "Non Recommandé"
    if "Actif" in liste_state:
        return "Actif"
    return "Autre"



class Demande:
    def __init__(self,mpn):
        self.mpn_demande:str=mpn
        self.list_mpn_response:list[Component]=[]
        self.equivalent:list[Demande]=[]
        self.global_status="Unknown"
        self.istreated:bool=False 
        self.Equiv_treated:bool=False
    
    def __find_gobal_status(self):
        for mpn in self.list_mpn_response:
            if mpn.status == "Obsolète":
                self.global_status=mpn.status
            elif mpn.status == "Non Recommandé" and self.global_status!="Obsolète":
                self.global_status=mpn.status
            elif mpn.status == "Actif" and self.global_status!="Obsolète" and self.global_status!="Non Recommandé":
                self.global_status=mpn.status
            elif mpn.status == "Autre" and self.global_status!="Obsolète" and self.global_status!="Non Recommandé" and self.global_status!="Actif":
                self.global_status=mpn.status
    
    def analyse_mpn(self,token_digykey,Actif=True,Rohs=True,Type_Research=False):
            results = {}
            liste_status=[]
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                future_dk = executor.submit(query_digikey, self.mpn_demande,token_digykey,Actif,Rohs,Type_Research)
                future_ms = executor.submit(query_mouser, self.mpn_demande,Actif,Rohs,Type_Research)
                future_fn = executor.submit(query_farnell, self.mpn_demande,Actif,Rohs,Type_Research)
                future_fu = executor.submit(query_future_electronics, self.mpn_demande,Actif,Rohs,Type_Research)
                
                #Attente des API
                results["DigiKey"] = future_dk.result()
                results["Mouser"] = future_ms.result()
                results["Farnell"] = future_fn.result()
                results["Future_Electronics"] = future_fu.result()
    
            valid_results = {dist: data for dist, data in results.items() if data and "Erreur" not in data}
            if not valid_results:
                erreurs = {
                distributeur: valeur.get("Erreur", "Réponse vide")
                if isinstance(valeur, dict)
                else "Réponse vide"
                for distributeur, valeur in results.items()
                }
        
                return {
                    "Status": "Failed", "content" :f"Aucun distributeur n'a retourné de résultat valide : {erreurs}",
                }
            # Regroupement de toutes les offres
            toutes_offres = []
            toutes_alternatives = set()
            for data in valid_results.values():
                toutes_offres.extend(data.get("offres", []))
                for alt in data.get("alternatives", []):
                            if alt:
                                toutes_alternatives.add(alt)
            for comp in list(toutes_alternatives):
                self.equivalent.append(Demande(comp))

            for offre in toutes_offres:
                chargement = ""

                ref_dist = re.sub(r'[:;$@}{#¤£&"|`^=+§*_]',"",offre["REF"])
                fabricant = chargement if offre["fabricant"]==""else offre["fabricant"]
                datasheet=chargement if offre["datasheet"]==""else offre["datasheet"]
                status=normalize_status(offre["status"])
                Temp_fonc = chargement if offre["Temp_fonc"]=="" else offre["Temp_fonc"]
                Description = chargement if offre["Description"]=="" else offre["Description"]
                Temp_Stock = chargement if offre["Temp_stock"]=="" else offre["Temp_stock"]
                humidity = chargement if offre["humidity"]=="" else offre["humidity"]
                Floor_life = chargement if offre["Floor_life"]=="" else offre["Floor_life"]
                Rohs = chargement if offre["Rohs"]=="" else offre["Rohs"]
                Reach = chargement if offre["Reach"]=="" or "Non" in offre["Reach"] else offre["Reach"]
                boitier = chargement if offre["boitier"]=="" else offre["boitier"]
                Dimensions = chargement if offre["Dimensions"]=="" else offre["Dimensions"]
                
                target_component= next((comp for comp in self.list_mpn_response if comp.mpn == ref_dist), None)
                if target_component :
                    if status==("Obsolète" or "Non Recommandé") or target_component.status == "Autre" : target_component.status = status
                    if target_component.Fabricant==chargement: target_component.Fabricant = fabricant
                    if target_component.Fiche_Technique==chargement: target_component.Fiche_Technique = datasheet
                    if target_component.Temp_fonc==chargement: target_component.Temp_fonc = Temp_fonc
                    if target_component.Description==chargement: target_component.Description = Description
                    if target_component.Temp_stock==chargement:target_component.Temp_stock=Temp_Stock
                    if target_component.humidity==chargement:target_component.humidity=humidity
                    if target_component.Rohs==chargement:target_component.Rohs=Rohs
                    if target_component.Reach==chargement:target_component.Reach=Reach
                    if target_component.boitier==chargement: target_component.boitier=boitier
                    if target_component.Dimensions==chargement: target_component.Dimensions=Dimensions
                    if target_component.Floor_life==chargement: target_component.Floor_life=Floor_life
                else:
                    target_component=Component(mpn=ref_dist,Temp_fonc=Temp_fonc,Description=Description,Temp_stock=Temp_Stock,humidity=humidity,Floor_life=Floor_life,Rohs=Rohs,Reach=Reach,boitier=boitier,Dimensions=Dimensions,fabricant=fabricant,datasheet=datasheet,status=status)
                    self.list_mpn_response.append(target_component)
    
                packages = offre["Package"]
                for pkg in packages:
                    target_component.offres.append(Offre(Distributeur= pkg["Distributeur"],Conditionnement= pkg["Conditionnement"],Stock= pkg["Stock_Disponible"],Prix_Unitaire= (" ".join([f"{p['Prix_Unitaire']} € (< {p['Quantite'] })" for p in pkg["Prix"]]) if pkg["Prix"] else "N/A") ,MOQ= pkg["MOQ"]))
                self.istreated = True
            
            self.__find_gobal_status()
            return {"Status": "Success"}

    def find_and_analyse_equiv(self,token_digykey,Actif=True,Rohs=True,Type_Research=False,nb_max_equiv=1):
        liste= []
        if self.equivalent == []:
            liste = query_digikey_sub(self.mpn_demande,token_digykey)
            if liste["Status"] =="Failed" : return  {"Status": "Failed","content":f"{self.mpn_demande} : Aucun Equivalents trouvés ou Erreur API"}
            else:
                for comp in liste["content"]:
                    self.equivalent.append(Demande(comp))
        nb_analyzed=0
        # Self.quivalent not empty
        for i in range(min(nb_max_equiv,len(self.equivalent))):
            response = self.equivalent[i].analyse_mpn(token_digykey=token_digykey,Actif=Actif,Rohs=Rohs,Type_Research=Type_Research)
            if response["Status"]=="Success" : 
                nb_analyzed+=1
                # Catégoriser le composant par rapport à Tronico
                response = self.equivalent[i].list_mpn_response[0].find_category()
                if response["Status"]=="Success" : 
                    #Remplir les champs 
                    self.equivalent[i].list_mpn_response[0].fill_champs_category()
                    if response["Status"]=="Success" :
                        self.Equiv_treated = True
                        return {"Status" :"Success","content":f"{nb_analyzed}/{min(nb_max_equiv,len(self.equivalent))} Equivalents analysé(s)"}
                    else:
                        return response
                else:
                    return response
            else:
                return response
          
    def get_liste_mpn_equiv(self):
        liste_temp:list[str]=[]
        for comp in self.equivalent:
             liste_temp.append(comp.mpn_demande)
        return liste_temp

    def get_liste_mpn_response(self):
        liste_temp:list[str]=[]
        for comp in self.list_mpn_response:
                liste_temp.append(comp.mpn)
        return liste_temp
    

    def __str__(self):
        texte = f"""
            ====== DEMANDE MPN : {self.mpn_demande} ======
            Equivalent(s) : {self.get_liste_mpn_equiv()}
            status global : {self.global_status}
            ====== DETAILS =====\n"""
        for comp in self.list_mpn_response:
            texte+= comp.__str__()

        return texte

if __name__=="__main__":
    demande = Demande("SMT-0927-S-8-R")
    print(demande.analyse_mpn(get_digikey_token(),True,True))
    print(demande)