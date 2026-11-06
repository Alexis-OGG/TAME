from ..tools.API_Distrib import *
import concurrent.futures
from .Demande import Demande
import time
from openpyxl.styles import Alignment, PatternFill, Font,Side,Border
from openpyxl.worksheet.errors import IgnoredError, IgnoredErrors
import pandas as pd
from pathlib import Path
import datetime as dt

class Analyse:
    def __init__(self,liste_mpn:list[str]):
        self.id=""
        self.liste_demandes:list[Demande]=[]
        self.liste_mpn_demandes_echoue:list[str]=[]
        self.liste_to_treat:list[str] = list(dict.fromkeys(liste_mpn))
        self.nb_obso=0
        self.metadatas={'Auteur': 'AUGER Alexis','Date d\'exécution': str(dt.datetime.now().strftime("%d-%m-%Y")),}

    def __get_success_Demandes(self):
        liste:list[Demande]=[]
        for demande in self.liste_demandes:
            if demande.istreated :
                liste.append(demande)
        return liste

    def __get_success_Demandes_obso(self):
            liste:list[Demande]=[]
            for demande in self.liste_demandes:
                if demande.istreated and (demande.global_status == "Obsolète" or demande.global_status == "Non Recommandé") :
                    liste.append(demande)
            return liste  
    
    def add_mpn(self,mpn:str|list[str]):
        try :
            nb=0
            if isinstance(mpn,str):
                if mpn not in self.liste_to_treat:
                    self.liste_to_treat.append(mpn)
                    nb+=1
            else:
                for elem in mpn:
                    if elem not in self.liste_to_treat:
                        self.liste_to_treat.append(elem)
                        nb+=1
            return {"Status":"Success","content" : f" {nb} MPN ajouté(s)"}
        except :
            return {"Status":"Failed","content" : f" Erreur lors de l'ajout"}                   

    def add_metadatas(self,dico : dict[str,str]):
        try :
            self.metadatas.update(dico)
            return {"Status":"Success","content" : " Données ajoutées"}
        except :
            return {"Status":"Failed","content" :" Erreur lors de l'ajout"}

    def analyse_components(self,Actif=True,Rohs=True):
        for mpn in self.liste_to_treat:
            self.liste_demandes.append(Demande(mpn=mpn))
        token_digykey = get_digikey_token()
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                # On lance l'analyse de plusieurs composants en même temps
                futures = {executor.submit(mpn.analyse_mpn,token_digykey,Actif,Rohs,False): mpn.mpn_demande for mpn in self.liste_demandes}
                i=0
                for future in concurrent.futures.as_completed(futures):
                    mpn = futures[future]
                    
                    result = future.result()
                    if result["Status"]=="Success":
                        i+=1
                        print(f"✅ Traité ({i}) : {mpn}",file=sys.stderr)

                    else:
                        self.liste_demandes_echoue.append(mpn)
                        print(
                            f" {mpn} : Analyse échoué",
                            file=sys.stderr
                        )
                    self.liste_to_treat.remove(mpn)
                    # Délai vital pour lisser la charge et éviter les erreurs 429 de Mouser/Farnell
                    time.sleep(0.5)        
        return {"Status" : "Success"}

    def analyse_obso(self,nb_equivalents):
        #Liste des composants analysés
        token_digykey = get_digikey_token()
        success_analyzed_demandes = self.__get_success_Demandes()

        #Anlayser composants obsolète
        nb_local_obso=0
        nb_success_obso=0
        content_erros= []
        for demande in success_analyzed_demandes:
            if demande.global_status == "Obsolète" or demande.global_status == "Non Recommandé" and not demande.Equiv_treated:
                self.nb_obso+=1
                nb_local_obso+=1
                #Analyse + Catégorise + Remplissage champs
                response = demande.find_and_analyse_equiv(token_digykey=token_digykey,Actif=True,Rohs=True,nb_max_equiv=nb_equivalents)
                if demande.Equiv_treated : nb_success_obso+=1
                else: content_erros.append((demande.mpn_demande,response["content"]))
        if nb_local_obso==nb_success_obso :
            return {'status' :'Sucess'}
        elif nb_local_obso>nb_success_obso and nb_success_obso>0:
            return {'status' :'Partial', 'content' : content_erros}
        else:
            return {'status' :'Failed', 'content' : content_erros}
    
    def exporter_excel(self,output:Path):
        lignes_excel_offres = [] 
        lignes_excel_technique = []
        lignes_obso = []
        if self.liste_demandes == []:
            return {"Status":"Failed", "content" : "Aucune données présentes"}
        for demande in self.liste_demandes:
                for mpn_response in demande.list_mpn_response:
                    lignes_excel_technique.append({
                        "MPN Identifié(s)": demande.mpn_demande,
                        "Equivalent(s) trouvé(s)" : '\n'.join(demande.get_liste_mpn_equiv()),
                        "MPN Trouvé(s)" : mpn_response.mpn,
                        "Statut ": mpn_response.status,
                        "Fabricant": mpn_response.Fabricant,
                        "Description" : mpn_response.Description,
                        "Température de fonctionnement":mpn_response.Temp_fonc,
                        "Température de stockage":mpn_response.Temp_stock,
                        "Humidité":mpn_response.humidity,
                        "Status Rohs":mpn_response.Rohs,
                        "Statut Reach":mpn_response.Reach,
                        "Boîtier":mpn_response.boitier,
                        "Dimensions":mpn_response.Dimensions,
                        "Fiche technique" : mpn_response.Fiche_Technique
                    })
                    for offre in mpn_response.offres :   
                        lignes_excel_offres.append({
                            "MPN Identifié(s)": demande.mpn_demande,
                            "MPN Trouvé(s)" : mpn_response.mpn,
                            "Statut ": mpn_response.status,
                            "Fabricant": mpn_response.Fabricant,
                            "Distributeur": offre.Distributeur,
                            "Conditionnement": offre.Conditionnement ,
                            "Stock Dispo": offre.Stock,
                            "MOQ": offre.MOQ,
                            "Grille Tarifaire": offre.Prix_Unitaire,
                        })

                if demande.Equiv_treated:
                    for mpn_equiv in demande.equivalent:
                        if mpn_equiv.istreated : 
                            lignes_obso.append({
                                "MPN Obsolète ou NRND": demande.mpn_demande,
                                "Equivalent(s) trouvé(s)" : mpn_equiv.mpn_demande,
                                "Statut ": mpn_equiv.global_status,
                                "FAMILLE": mpn_equiv.list_mpn_response[0].category[0],
                                "SS_FAMILLE": mpn_equiv.list_mpn_response[0].category[1],
                                "CHAMPS 1" : mpn_equiv.list_mpn_response[0].champs.get(1,(None,None))[1],
                                "CHAMPS 2" : mpn_equiv.list_mpn_response[0].champs.get(2,(None,None))[1],
                                "CHAMPS 3" : mpn_equiv.list_mpn_response[0].champs.get(3,(None,None))[1],
                                "CHAMPS 4" : mpn_equiv.list_mpn_response[0].champs.get(4,(None,None))[1],
                                "CHAMPS 5" : mpn_equiv.list_mpn_response[0].champs.get(5,(None,None))[1],
                                "CHAMPS 6" : mpn_equiv.list_mpn_response[0].champs.get(6,(None,None))[1],
                                "CHAMPS 7" : mpn_equiv.list_mpn_response[0].champs.get(7,(None,None))[1],
                                "CHAMPS 8" : mpn_equiv.list_mpn_response[0].champs.get(8,(None,None))[1],
                                "CHAMPS 9" : mpn_equiv.list_mpn_response[0].champs.get(9,(None,None))[1],
                                "CHAMPS 10" : mpn_equiv.list_mpn_response[0].champs.get(10,(None,None))[1],
                            })

        #Update Metadatas :
        self.metadatas.update({
            'Nombre de MPN identifié(s)' : len(self.liste_demandes)+len(self.liste_mpn_demandes_echoue)+len(self.liste_to_treat),
            'Nombre de MPN non analysé(s)' : len(self.liste_to_treat),
            'Nombre de MPN traité(s) avec succès' : len(self.liste_demandes),
            'Nombre de MPN ayant rencontré(s) une erreur' : len(self.liste_mpn_demandes_echoue),
            'Taux de réussite' : f"{round(len(self.liste_demandes)/(len(self.liste_demandes)+len(self.liste_mpn_demandes_echoue)) * 100,ndigits=2)} %"
        })   
        
        if lignes_excel_offres and lignes_excel_technique:
                df_offres = pd.DataFrame(lignes_excel_offres)
                df_technique = pd.DataFrame(lignes_excel_technique)
                df_meta = pd.DataFrame(list(self.metadatas.items()), columns=['Propriété', 'Valeur'])
                df_obso = pd.DataFrame(lignes_obso)
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df_meta.to_excel(writer, sheet_name='Metadata', index=False)
                    df_offres.to_excel(writer, index=False, sheet_name='Achat')
                    df_technique.to_excel(writer, index=False, sheet_name='Technique')
                    df_obso.to_excel(writer, index=False, sheet_name='Obso_NRND')
                    workbook = writer.book
                    worksheet_offres = writer.sheets['Achat']
                    worksheet_technique = writer.sheets['Technique']
                    worksheet_metadata = writer.sheets['Metadata']
                    worksheet_obso = writer.sheets['Obso_NRND']
                    worksheet_offres.freeze_panes = "D1"
                    worksheet_obso.freeze_panes = "D1"
                    worksheet_technique.freeze_panes = "E1"
                    worksheet_metadata.sheet_view.showGridLines = False
                    erreur_ignoree = IgnoredError(
                        sqref="A2:Z100000",
                        numberStoredAsText=True     
                    ),

                    worksheet_technique.ignored_errors = IgnoredErrors(ignoredError=[erreur_ignoree])
                    worksheet_offres.ignored_errors = IgnoredErrors(ignoredError=[erreur_ignoree])
                    # Styles globaux
                    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
                    key_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
                    header_font = Font(color="FFFFFF", bold=True)
                    key_font = Font(bold=True, color="333333", size=11)
                    value_font = Font(color="000000", size=11)
                    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
                    left_align_top = Alignment(horizontal="left", vertical="top", wrap_text=True)
                    align_left = Alignment(horizontal="left", vertical="center", indent=1)
                    link_font = Font(color="0563C1", underline="single")
                    fine_border = Border(
                        left=Side(style='thin', color='D9D9D9'),
                        right=Side(style='thin', color='D9D9D9'),
                        top=Side(style='thin', color='D9D9D9'),
                        bottom=Side(style='thin', color='D9D9D9')
                    )
                    
                    for cell in worksheet_offres[1]:
                        cell.fill = header_fill
                        cell.font = header_font
                        cell.alignment = center_align
                    for cell in worksheet_technique[1]:
                        cell.fill = header_fill
                        cell.font = header_font
                        cell.alignment = center_align
                    for cell in worksheet_obso[1]:
                        cell.fill = header_fill
                        cell.font = header_font
                        cell.alignment = center_align
                    for cell in worksheet_metadata["1:1"]:
                        if cell.value:
                            cell.fill = header_fill
                            cell.font = header_font
                            cell.alignment = center_align
                            cell.border = fine_border


                    #worksheet_offres
                    start_row = 2
                    for i in range(2, len(df_offres) + 2):
                        is_last_row = (i == len(df_offres) + 1)
                        
                        # Condition de rupture pour les blocs globaux du composant (Cols A-E)
                        rupture_ref = is_last_row or worksheet_offres.cell(row=i, column=1).value != worksheet_offres.cell(row=i+1, column=1).value
                        
                        # Gestion alignement pour la grille tarifaire (Col K)
                        # worksheet_offres[f"J{i}"].alignment = left_align_top
            
                        if rupture_ref:
                            end_row = i
                            if start_row < end_row:
                                # Fusion des informations générales
                                for col in ['A']:
                                    worksheet_offres.merge_cells(f"{col}{start_row}:{col}{end_row}")
                                    worksheet_offres[f"{col}{start_row}"].alignment = center_align
            
                                # Fusion secondaire des MPN_trouvés
                                ref_start = start_row
                                for r in range(start_row, end_row + 1):
                                    val_actuelle = worksheet_offres.cell(row=r, column=2).value
                                    val_suivante = worksheet_offres.cell(row=r+1, column=2).value if r < end_row else None
                                    worksheet_offres[f"B{ref_start}"].alignment = center_align
                                    if val_actuelle != val_suivante:
                                        if ref_start < r:
                                            worksheet_offres.merge_cells(f"B{ref_start}:B{r}")
                                            worksheet_offres.merge_cells(f"C{ref_start}:C{r}")

                                        ref_start = r + 1
                
                            # Couleurs Actif
                            All_cell_status = worksheet_offres[f"C{start_row}:C{end_row}"]
                            for tuple in All_cell_status:
                                cell_status = tuple[0]
                                if cell_status.value == "Actif":
                                    cell_status.fill = PatternFill(start_color="0DF34F", fill_type="solid")
                                    cell_status.font = Font(color="040404", bold=True)
                                elif cell_status.value == "Obsolète":
                                    cell_status.fill = PatternFill(start_color="EE1212", fill_type="solid")
                                    cell_status.font = Font(color="040404", bold=True)
                                elif cell_status.value == "Non Recommandé":
                                        cell_status.fill = PatternFill(start_color="F69C0A", fill_type="solid")
                                        cell_status.font = Font(color="040404", bold=True)
                                
                            start_row = end_row + 1

                    #worksheet_technique
                    start_row = 2
                    for i in range(2, len(df_technique) + 2):
                        is_last_row = (i == len(df_offres) + 1)
                        
                        # Condition de rupture pour les blocs globaux du composant (Cols A-E)
                        rupture_ref = is_last_row or worksheet_technique.cell(row=i, column=1).value != worksheet_technique.cell(row=i+1, column=1).value
                                        
                        # Gestion alignement pour la grille tarifaire (Col K)
                        worksheet_technique[f"J{i}"].alignment = left_align_top
                            
                        if rupture_ref:
                            end_row = i
                            if start_row < end_row:
                                # Fusion des informations générales
                                for col in ['A', 'B']:
                                    worksheet_technique.merge_cells(f"{col}{start_row}:{col}{end_row}")
                                    worksheet_technique[f"{col}{start_row}"].alignment = center_align
            
                                # Fusion secondaire des Distributeurs
                                # ref_start = start_row
                                # for r in range(start_row, end_row + 1):
                                #     val_actuelle = worksheet_technique.cell(row=r, column=4).value
                                #     val_suivante = worksheet_technique.cell(row=r+1, column=4).value if r < end_row else None
                                #     worksheet_technique[f"D{ref_start}"].alignment = center_align
                                #     if val_actuelle != val_suivante:
                                #         if ref_start < r:
                                #             worksheet_technique.merge_cells(f"D{ref_start}:D{r}")
                                            
                                        # ref_start = r + 1
                            worksheet_technique[f"C{start_row}"].alignment = center_align
                            # Lien hypertexte de la Fiche Technique
                            All_cell_lien = worksheet_technique[f"N{start_row}:N{end_row}"]
                            for tuple in All_cell_lien:
                                cell_lien = tuple[0]
                                if cell_lien.value and str(cell_lien.value).startswith("http"):
                                    url = cell_lien.value
                                    cell_lien.value = "📄 Ouvrir la datasheet"
                                    cell_lien.hyperlink = url
                                    cell_lien.font = link_font
                                    cell_lien.alignment = center_align
                                
            
                            # Couleurs Actif
                            All_cell_status = worksheet_technique[f"D{start_row}:D{end_row}"]
                            for tuple in All_cell_status:
                                cell_status = tuple[0]
                                if cell_status.value == "Actif":
                                    cell_status.fill = PatternFill(start_color="0DF34F", fill_type="solid")
                                    cell_status.font = Font(color="040404", bold=True)
                                elif cell_status.value == "Obsolète":
                                    cell_status.fill = PatternFill(start_color="EE1212", fill_type="solid")
                                    cell_status.font = Font(color="040404", bold=True)
                                elif cell_status.value == "Non Recommandé":
                                        cell_status.fill = PatternFill(start_color="F69C0A", fill_type="solid")
                                        cell_status.font = Font(color="040404", bold=True)
                                
                            start_row = end_row + 1

                    #worksheet_metadata 
                    for row in range(2, len(df_meta) + 2):
                        cell_key = worksheet_metadata.cell(row=row, column=1)
                        cell_value = worksheet_metadata.cell(row=row, column=2)
                        
                        # Style Colonne A (Les propriétés)
                        cell_key.fill = key_fill
                        cell_key.font = key_font
                        cell_key.alignment = align_left
                        cell_key.border = fine_border
                        
                        # Style Colonne B (Les valeurs)
                        cell_value.font = value_font
                        cell_value.alignment = align_left
                        cell_value.border = fine_border
                        
                    # Ajuster la largeur des colonnes worksheet_metadata
                    worksheet_metadata.column_dimensions['A'].width = 50
                    worksheet_metadata.column_dimensions['B'].width = 50
                    worksheet_metadata.column_dimensions['C'].width = 5 


                    #worksheet_obso
                    start_row = 2
                    for i in range(2, len(df_obso) + 2):
                        is_last_row = (i == len(df_obso) + 1)
                        
                        # Condition de rupture pour les blocs globaux du composant (Cols A-E)
                        rupture_ref = is_last_row or worksheet_obso.cell(row=i, column=1).value != worksheet_obso.cell(row=i+1, column=1).value
                        
                        # Gestion alignement pour la grille tarifaire (Col K)
                        # worksheet_obso[f"J{i}"].alignment = left_align_top
            
                        if rupture_ref:
                            end_row = i
                            if start_row < end_row:
                                # Fusion des informations générales
                                for col in ['A']:
                                    worksheet_obso.merge_cells(f"{col}{start_row}:{col}{end_row}")
                                    worksheet_obso[f"{col}{start_row}"].alignment = center_align
            
                                # Fusion secondaire des MPN_trouvés
                                ref_start = start_row
                                for r in range(start_row, end_row + 1):
                                    worksheet_obso[f"B{r}"].alignment = center_align
                
                            # Couleurs Actif
                            All_cell_status = worksheet_obso[f"C{start_row}:C{end_row}"]
                            for tuple in All_cell_status:
                                cell_status = tuple[0]
                                if cell_status.value == "Actif":
                                    cell_status.fill = PatternFill(start_color="0DF34F", fill_type="solid")
                                    cell_status.font = Font(color="040404", bold=True)
                                elif cell_status.value == "Obsolète":
                                    cell_status.fill = PatternFill(start_color="EE1212", fill_type="solid")
                                    cell_status.font = Font(color="040404", bold=True)
                                elif cell_status.value == "Non Recommandé":
                                        cell_status.fill = PatternFill(start_color="F69C0A", fill_type="solid")
                                        cell_status.font = Font(color="040404", bold=True)
                                
                            start_row = end_row + 1

                    # Largeurs de colonnes sur-mesure
                    largueurs = {'A': [20,20,20], 'B': [20,20,20], 'C':[15,25,15], 'D': [30,15,20], 'E':[20,30,20,20] , 'F': [50,120,20], 'G': [10,15,20], 'H':  [10,15,20], 'I':[150,20,20], 'J': [20,20,20],'K': [20,20,20],'L': [20,20,20],'M': [20,40,20],'N': [20,40,20],'O':[20,40,20]}
                    for col_letter, width in largueurs.items():
                        worksheet_offres.column_dimensions[col_letter].width = width[0]
                        worksheet_technique.column_dimensions[col_letter].width = width[1]
                        worksheet_obso.column_dimensions[col_letter].width = width[2]
                return output

    def __str__(self):
        demande_success = self.__get_success_Demandes()
        texte = ""
        for index,demande in enumerate(demande_success):
            texte += (f"============DEMANDE n°{index+1}===========\n")
            texte += demande.__str__()
        return texte

if __name__=="__main__":
    import pickle
    test = Analyse(["SDR08540M3-01"])
    mes_metadonnees = {
        'Projet': 'Analyse BOM'}
    test.add_metadatas(mes_metadonnees)
    print(test.analyse_components(True,True))
    print(test.analyse_obso(1))
    print(test)
    test.exporter_excel(Path("C:/Users/alexis.auger/Documents/GitHub/Ollama/src/assets/V2.xlsx"))
    with open(Path("C:/Users/alexis.auger/Documents/GitHub/Ollama/src/assets/test.pkl"),'wb')as f:
        pickle.dump(test,f)
