#Modules Outils
from tools.API_Distrib import get_digikey_token
from tools.Find_Equiv import Recherche_eq_gen,Recherche_substitut_digikey
from tools.build_liste_comp import build_unified_json
from tools.export_excel import exporter_excel

#Librairies
import time
import concurrent.futures
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
  
#Outils
def gerer_upload():
    st.session_state.mon_fichier = st.session_state.uploader_widget
    st.session_state.resultats_bom = {}

#Page Analyse BOM
def Analyse_BOM_st():
    st.title("Analyse de Nomenclature (BOM)")
    

    if st.session_state.mon_fichier is not None :


        col1, col2 = st.columns([3, 1])
    
        with col1:
            st.success(f"📁 Fichier en cours d'Analyse : **{st.session_state.mon_fichier.name}**")
            
        with col2:
            # Bouton pour supprimer le fichier
            if st.button("Changer de BOM", use_container_width=True):
                st.session_state.mon_fichier = None
                st.rerun()
        
        #Détection nouvelle BOM 
        if st.session_state.bom_futures=={} and st.session_state.resultats_bom=={}:
            token_digykey = get_digikey_token()
            df = pd.read_excel(st.session_state.mon_fichier)
            references = df['REF_FAB'].astype(str).tolist()
            st.session_state.index =0
            st.session_state.reference = len(references)
            for mpn in references:
                # On soumet la tâche à l'exécuteur persistant
                future = st.session_state.bom_executor.submit(
                    build_unified_json, mpn, token_digykey, True, True, False
                )
                # On sauvegarde la "future" dans le session_state
                st.session_state.bom_futures[future] = mpn

        barre_progression = st.progress((st.session_state.index ) / st.session_state.reference)
        texte_statut = st.empty()
        conteneur_resultats = st.container()

        #Affichage ref analysée
        texte_statut.text(f"Traitement : {st.session_state.index} / {st.session_state.reference}")
        for mpn,donnee in st.session_state.resultats_bom.items():
            with conteneur_resultats:
                                    
                # --- LIGNE PRINCIPALE ---
                col1, col2, col3, col4,col6 = st.columns([2, 2, 2, 1,1])
                col1.markdown(f"**{mpn}**")
                col2.write(f"{donnee["main"]["Fabricant"]}")
                
                # Code couleur simple pour le statut
                statut = donnee["main"].get("Statut_Global", {}).get("Consensus", "Inconnu")
                
                if statut == "Actif":
                    col3.success("🟢 Actif")
                elif statut == "Obsolète":
                    col3.error("🔴 Obsolète")
                else:
                    col3.warning(f"🟠 {statut}")
                Alerte = donnee["main"].get("Statut_Global",False).get("Alerte_Conflit",False)
                col4.write( "OK" if not Alerte else f"⚠️ Conflit")

                col6.markdown(f"[Fiche technique]({donnee["main"]["Fiche_Technique"]})")
                # print(json.dumps(result, indent=2, ensure_ascii=False))
                # --- LE MENU DÉROULANT (SOUS-LIGNE) ---
                with st.expander("Voir les offres et spécifications techniques", expanded=False):

                    # Affichage propre du sous-tableau
                    if len(donnee.keys())>=2:
                        
                        for key in donnee.keys():
                            if key!="main":
                                st.markdown(key)
                                st.dataframe(donnee[key]["techniques"],column_config={}, hide_index=True)
                                st.dataframe(donnee[key]["offres"],column_config={}, hide_index=True)

                    else:
                        st.info("Aucune offre avec stock disponible.")
                        
                st.divider() 

        #Affichage ref en cours d'analyse
        for future in concurrent.futures.as_completed(st.session_state.bom_futures):
            mpn = st.session_state.bom_futures[future]
            result = future.result()
            del st.session_state.bom_futures[future]
            
            try :   
                # print(json.dumps(result, indent=2, ensure_ascii=False))
                
                statut=""
                # 2. On dessine la ligne DANS le conteneur dès que la donnée arrive
                with conteneur_resultats:
                        col1, col2, col3, col4,col6 = st.columns([2, 2, 2,1,1])
                        if result== None : 
                            col1.markdown(f"**{mpn}**")
                            col3.error("🔴 INTROUVABLE")
                            continue
                        Tableau_ref={"main":{}}
                        Tableau_ref["main"]["Fabricant"]=result.get('Fabricant', 'Inconnu')
                        Tableau_ref["main"]["Equivalents_Suggeres"]=result.get('Equivalents_Suggeres', [])
                        Tableau_ref["main"]["Statut_Global"]= result.get("Statut_Global", {})
                        # --- LIGNE PRINCIPALE ---
                       
                        col1.markdown(f"**{mpn}**")
                        col2.write(f"{result.get('Fabricant', 'Inconnu')}")
                        
                        # Code couleur simple pour le statut
                        statut = result.get("Statut_Global", "").get("Consensus", "Inconnu")
                        
                        if statut == "Actif":
                            col3.success("🟢 Actif")
                        elif statut == "Obsolète":
                            col3.error("🔴 Obsolète")
                        else:
                            col3.warning(f"🟠 {statut}")
                        Alerte = result.get("Statut_Global",False).get("Alerte_Conflit",False)
                        col4.write( "OK" if not Alerte else f"⚠️ Conflit")
                        
                        offres = result.get("Offres_Disponibles", [])
                        
                        datasheet = result.get("Fiche_Technique", "")
                        if datasheet.startswith("//"):
                            datasheet = "https:" + datasheet
                        Tableau_ref["main"]["Fiche_Technique"]=datasheet
                        col6.markdown(f"[Fiche technique]({datasheet})")
                        # print(json.dumps(result, indenensure_ascii=False))
                        # --- LE MENU DÉROULANT (SOUS-LIGNE) ---
                        with st.expander("Voir les offres et spécifications techniques", expanded=False):
                            #Gestion plusieurs composants avec la même ref 
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
                                    if Tableau_ref[ref_dist]["techniques"][0]["Température de fonctionnement"]==chargement: Tableau_ref[ref_dist]["techniques"][0]["Température de fonctionnement"] = Temp_fonc
                                    if Tableau_ref[ref_dist]["techniques"][0]["Température de stockage"]==chargement:Tableau_ref[ref_dist]["techniques"][0]["Température de stockage"]=Temp_Stock
                                    if Tableau_ref[ref_dist]["techniques"][0]["Humidité"]==chargement:Tableau_ref[ref_dist]["techniques"][0]["Humidité"]=humidity
                                    if Tableau_ref[ref_dist]["techniques"][0]["Status Rohs"]==chargement:Tableau_ref[ref_dist]["techniques"][0]["Status Rohs"]=Rohs
                                    if Tableau_ref[ref_dist]["techniques"][0]["Statut Reach"]==chargement:Tableau_ref[ref_dist]["techniques"][0]["Statut Reach"]=Reach
                                    if Tableau_ref[ref_dist]["techniques"][0]["Boîtier"]==chargement: Tableau_ref[ref_dist]["techniques"][0]["Boîtier"]=boitier
                                    if Tableau_ref[ref_dist]["techniques"][0]["Dimensions"]==chargement: Tableau_ref[ref_dist]["techniques"][0]["Dimensions"]=Dimensions
                                    if Tableau_ref[ref_dist]["techniques"][0]["Durée de conservation"]==chargement: Tableau_ref[ref_dist]["techniques"][0]["Durée de conservation"]=Floor_life
                                else:
                                    liste_ref.append(ref_dist)
                                    Tableau_ref[ref_dist]={"techniques":[{
                                        "Température de fonctionnement":Temp_fonc,
                                        "Température de stockage":Temp_Stock,
                                        "Humidité":humidity,
                                        "Durée de conservation":Floor_life,
                                        "Status Rohs":Rohs,
                                        "Statut Reach":Reach,
                                        "Boîtier":boitier,
                                        "Dimensions":Dimensions,
                                    }],"offres":[]}

                                packages = offre["Package"]
                                for pkg in packages:
                                    
                                    Tableau_ref[ref_dist]["offres"].append({
                                        "Distributeur": distri,
                                        "Conditionnement": pkg["Conditionnement"],
                                        "Stock": pkg["Stock_Disponible"],
                                        "Prix Unitaire" : " ".join([f"{p['Prix_Unitaire']} € (< {p['Quantite'] })" for p in pkg["Prix"]]) if pkg["Prix"] else "N/A" ,
                                        "MOQ" : pkg["MOQ"]
                                    })

                                    

                            #print(json.dumps(Tableau_ref, indent=2, ensure_ascii=False))
                            # Affichage propre du sous-tableau
                            if len(Tableau_ref.keys())>=2:
                                
                                for key in Tableau_ref.keys():
                                    if key!="main":
                                        st.markdown(key)
                                        st.dataframe(Tableau_ref[key]["techniques"],column_config={}, hide_index=True)
                                        st.dataframe(Tableau_ref[key]["offres"],column_config={}, hide_index=True)

                            else:
                                st.info("Aucune offre avec stock disponible.")
                                
                        st.divider() # Ligne grise de séparation entre les composants
                if statut == "Obsolète" or statut=="Non Recommandé" : 
                    st.session_state.obsolete[mpn]=Tableau_ref
                st.session_state.resultats_bom[mpn]=Tableau_ref
                # Mise à jour des compteurs et délai
                texte_statut.text(f"Traitement : {st.session_state.index+1} / {st.session_state.reference} terminés ({mpn})")
                barre_progression.progress((st.session_state.index + 1) / st.session_state.reference)
                
                st.session_state.index +=1
                time.sleep(0.5)
                
            except Exception as e : 
                st.error({"Crash" : f"{mpn} : {e}"})

        donnees_extraites = exporter_excel(st.session_state.resultats_bom)
        if donnees_extraites is not None:
            st.download_button(
                    label=" Exporter dans un fichier Excel",
                    data=donnees_extraites,
                    file_name=f"Analyse_{st.session_state.mon_fichier.name}",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

              
        with st.expander("Outils de débuggage", expanded=False):
            st.json(st.session_state.resultats_bom)

    else :
        st.file_uploader("Chargez votre fichier BOM.xlsx",key="uploader_widget", type=["xlsx"],on_change=gerer_upload)

#Page Recherche Eq
def Recherche_eq_st():
    st.title("Recherche de composants équivalents")
    st.text_input(label="Outil de recherche",type="search",placeholder="Rechercher des alternatives composants obscolètes")
    if len(st.session_state.obsolete.keys())>=1:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.warning(f"Détection de {len(st.session_state.obsolete.keys())} composant(s) obsolète(s) ou non recommandé(s) d'après la recherche l'analyse de la BOM") 
        with col2:
            # Bouton pour supprimer le fichier
            if st.button("Recherche équivalents", use_container_width=True):
                for mpn,donnee in st.session_state.obsolete.items():
                        token_digykey=get_digikey_token()
                        
                        #Aucun équivalent trouvé durant l'analyse BOM
                        if donnee["main"]["Equivalents_Suggeres"] == []:
                            future = st.session_state.bom_executor.submit(
                                Recherche_substitut_digikey, mpn, token_digykey)
                            st.session_state.obso_futures[future] = mpn
                        #Liste d'équivalents suggérés
                        else:
                            future = st.session_state.bom_executor.submit(
                                Recherche_eq_gen, mpn, token_digykey)
                            st.session_state.obso_futures[future] = mpn
    st.divider()

    for future in concurrent.futures.as_completed(st.session_state.bom_futures):
        mpn = st.session_state.bom_futures[future]
        result = future.result()
        del st.session_state.bom_futures[future]

def main():
    
    st.set_page_config(page_title="Radar BOM", layout="wide")
    
    # Construction de la barre latérale
    st.sidebar.title("Outils Disponibles")
    st.sidebar.markdown("---")
    # Sélection de la page
    if "mon_fichier" not in st.session_state:
        st.session_state.mon_fichier = None   

    if "bom_executor" not in st.session_state:
        st.session_state.bom_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    # 2. Créer un dictionnaire persistant pour stocker les tâches en cours
    if "bom_futures" not in st.session_state:
        st.session_state.bom_futures = {}

    if "resultats_bom" not in st.session_state:
        st.session_state.resultats_bom = {}

    if "index" not in st.session_state:
        st.session_state.index = 0
    if "reference" not in st.session_state:
        st.session_state.reference = 0
    if "obsolete" not in st.session_state:
            st.session_state.obsolete = {}
    if "obso_futures" not in st.session_state:
        st.session_state.obso_futures = {}
    
    choix_page = st.sidebar.radio(
        "Aller à :",
        ["Analyse BOM", "Recherche Equivalents"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("v1.0")
    # Routage vers la bonne fonction selon le choix
    if choix_page == "Analyse BOM":
        Analyse_BOM_st()
    elif choix_page == "Recherche Equivalents":
        Recherche_eq_st()



if __name__ == "__main__":
    load_dotenv()

    #     bruh = exporter_excel({PIC32CM6408PL10028-E/SS 
    # test = query_digikey_sub("BAS116T,115",get_digikey_token())
    # print(json.dumps(test, indent=2, ensure_ascii=False))
    # url ="https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8942/490_Chip_Multilayer_CAT2021_MLCC.pdf" 
    main()

    # test1=query_farnell("Capacitor 22uF 10V 0805",True,True,True)
    # test1=analyse_liste(["GRM21BR61A226ME51"],False,False)
    # test1=query_farnell("GRM21BR61A226ME51",False,False,False)

    # print(json.dumps(test1, indent=2, ensure_ascii=False))
    # result = analyse_liste([  "GRM21BR61A226ME51"])
    # liste1 = [
    #   "3039",
    #   "CR2477N",
    #   "C0603C103K4RACTU",
    #   "06033C104KAT2A",
    #   "GRM32ER71A476KE15L",
    #   "GRM32ER71A476KE15L",
    #   "BAS116T,115",
    #   "BAS116TT1G",
    #   "SMT-1324-TW-1V-R",
    #   "SDR08540M3-01",
    #   "MMBT3906LT1G",
    #   "MMBT3904LT1G",
    #   "IRLML2502TRPBF",
    #   "CRCW0603470RFKEA",
    #   "CRCW0603100KFKEA",
    #   "CRCW0603470KFKEA",
    #   "CRCW06031K00FKEA",
    #   "CRCW060320K0FKEA",
    #   "RC0603FR-0720KL",
    #   "CRCW0603330RJNEA",
    #   "CRCW060330K0FKEA",
    #   "CRCW06030000Z0EA",
    #   "CRCW06030000Z0EA",
    #   "CRCW0603560KFKEA",
    #   "CRCW060320K0FKEA",
    #   "RC0603FR-0720KL",
    #   "SKRNPME010",
    #   "RFD21733",
    #   "MAX6778XK+",
    #   "1355PCB001 IND 02",
    #   "1355C1001 IND 02",
    #   "PAN 511 REMO 019 IND 00",
    #   "1355ET001 IND 02",
    #   "BRADY THT-38-727-10",
    #   "BRADY R-6002",
    #   "1355ET002 IND 01",
    #   "BRADY THT-38-727-10",
    #   "BRADY R-6002"
    # ]
    #     liste2=[
    #   "C0603C103K4RACTU",
    #   "06033C104KAT2A",
    #   "C1210C476M4PACTU",
    #   "C1210C476M4PACTU",
    #   "HSMD-C190",
    #   "SMBJ5.0CA",
    #   "HSMG-C190",
    #   "5749767-1",
    #   "5206052-3",
    #   "MMBT3904LT1G",
    #   "MMBT3906LT1G",
    #   "CRCW06032OKOFKEA",
    #   "RC0603FR-0720KL",
    #   "CRCW06032OKOFKEA",
    #   "RC0603FR-0720KL",
    #   "CRCW0603110RFKEA",
    #   "CRCW0603470RFKEA",
    #   "RC0603FR-0747KL",
    #   "CRCW060347K0FKEA",
    #   "RC0603FR-07330RL",
    #   "CRCW06030000Z0EA",
    #   "CRCW06030000Z0EA",
    #   "CRG1206ZR",
    #   "7914J-1-000E",
    #   "RFD21733",
    #   "MC74HC03ADG",
    #   "1357PCB001 IND 02",
    #   "1357C1001 IND 02",
    #   "PAN 511 INTE 020 IND 00",
    #   "1357ET001 IND 02",
    #   "BRADY THT-1-719-10",
    #   "BRADY R-6002"
    # ]
    #     resultats = analyse_liste(liste2,True,True)
    #resultats = analyse_liste(get_excel_column_data(file_path="./1357LC001_02.xlsx",column_name=),True,True)







