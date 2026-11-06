from openpyxl.styles import Alignment, PatternFill, Font,Side,Border
import pandas as pd
import io
from ...Class.classlist import ResultAllProduct
import base64
from pathlib import Path
import warnings

def exporter_excel(resultats:dict[str,ResultAllProduct],mes_metadonnees,output:Path):
    lignes_excel_offres = [] 
    lignes_excel_technique = []
    if resultats == {}:
        return None
    for ref,produit in resultats.items():
            if "Erreur" in produit:
                continue
                
            # ref = produit.get("REF_FAB", "")
            fab = produit.main.Fabricant
            consensus = produit.main.Statut_Global.Consensus or ""
            # conflit = produit.main.Statut_Global.Alerte_Conflit or False
            # detail_conflit = produit.main.Statut_Global.Details_Distributeurs or {}
            datasheet = produit.main.Fiche_Technique or ""

            for ref_fab, donnees in produit.liste_products.items():
                if ref_fab =="main":
                    continue
                technique=produit.liste_products.get(ref_fab,{}).techniques or []
                lignes_excel_technique.append({
                    "REF": ref,
                    "Fabricant": fab,
                    "Statut Global": consensus,
                    "REF_Fab" : ref_fab,
                    "Température de fonctionnement":technique[0].Temp_fonc,
                    "Température de stockage":technique[0].Temp_stock,
                    "Humidité":technique[0].humidity,
                    "Status Rohs":technique[0].Rohs,
                    "Statut Reach":technique[0].Reach,
                    "Boîtier":technique[0].boitier,
                    "Dimensions":technique[0].Dimensions,
                    "Fiche technique" : datasheet
                })
                for offre in donnees.offres or []:   
                    lignes_excel_offres.append({
                        "REF": ref,
                        "Fabricant": fab,
                        "Statut Global": consensus,
                        # "Alerte Statut": f"⚠️ Conflit" if conflit else "OK",
                        "REF_Fab" : ref_fab,
                        "Distributeur": offre.Distributeur or "N/A",
                        "Conditionnement": offre.Conditionnement or "N/A",
                        "Stock Dispo": offre.Stock or 0,
                        "MOQ": offre.MOQ or 1,
                        "Grille Tarifaire": offre.Prix_Unitaire or [],
                    })
        
    if lignes_excel_offres and lignes_excel_technique:
            df_offres = pd.DataFrame(lignes_excel_offres)
            df_technique = pd.DataFrame(lignes_excel_technique)
            df_meta = pd.DataFrame(list(mes_metadonnees.items()), columns=['Propriété', 'Valeur'])
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df_meta.to_excel(writer, sheet_name='Metadata', index=False)
                df_offres.to_excel(writer, index=False, sheet_name='Achat')
                df_technique.to_excel(writer, index=False, sheet_name='Technique')
                
                workbook = writer.book
                worksheet_offres = writer.sheets['Achat']
                worksheet_technique = writer.sheets['Technique']
                worksheet_metadata = writer.sheets['Metadata']
                worksheet_offres.freeze_panes = "D1"
                worksheet_technique.freeze_panes = "D1"
                worksheet_metadata.sheet_view.showGridLines = False
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
                    worksheet_offres[f"J{i}"].alignment = left_align_top
        
                    if rupture_ref:
                        end_row = i
                        if start_row < end_row:
                            # Fusion des informations générales
                            for col in ['A', 'B', 'C']:
                                worksheet_offres.merge_cells(f"{col}{start_row}:{col}{end_row}")
                                worksheet_offres[f"{col}{start_row}"].alignment = center_align
        
                            # Fusion secondaire des REF_Fab
                            ref_start = start_row
                            for r in range(start_row, end_row + 1):
                                val_actuelle = worksheet_offres.cell(row=r, column=5).value
                                val_suivante = worksheet_offres.cell(row=r+1, column=5).value if r < end_row else None
                                worksheet_offres[f"E{ref_start}"].alignment = center_align
                                if val_actuelle != val_suivante:
                                    if ref_start < r:
                                        worksheet_offres.merge_cells(f"E{ref_start}:E{r}")

                                    ref_start = r + 1
                            
                        # # Couleurs des statuts
                        # cell_alerte = worksheet_offres[f"D{start_row}"]
                        # if "⚠️ Conflit" in cell_alerte.value :
                        #     cell_alerte.fill = PatternFill(start_color="FFC7CE", fill_type="solid")
                        #     cell_alerte.font = Font(color="9C0006", bold=True)
                        # elif cell_alerte.value == "OK":
                        #     cell_alerte.fill = PatternFill(start_color="C6EFCE", fill_type="solid")
                        #     cell_alerte.font = Font(color="006100", bold=True)
        
                        # Couleurs Actif
                        cell_alerte = worksheet_offres[f"C{start_row}"]
                        if cell_alerte.value == "Actif":
                            cell_alerte.fill = PatternFill(start_color="0DF34F", fill_type="solid")
                            cell_alerte.font = Font(color="040404", bold=True)
                        elif cell_alerte.value == "Obsolète":
                            cell_alerte.fill = PatternFill(start_color="EE1212", fill_type="solid")
                            cell_alerte.font = Font(color="040404", bold=True)
                        elif cell_alerte.value == "Non Recommandé":
                                cell_alerte.fill = PatternFill(start_color="F69C0A", fill_type="solid")
                                cell_alerte.font = Font(color="040404", bold=True)
                            
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
                            for col in ['A', 'B', 'C','L',]:
                                worksheet_technique.merge_cells(f"{col}{start_row}:{col}{end_row}")
                                worksheet_technique[f"{col}{start_row}"].alignment = center_align
        
                            # Fusion secondaire des Distributeurs
                            ref_start = start_row
                            for r in range(start_row, end_row + 1):
                                val_actuelle = worksheet_technique.cell(row=r, column=4).value
                                val_suivante = worksheet_technique.cell(row=r+1, column=4).value if r < end_row else None
                                worksheet_technique[f"D{ref_start}"].alignment = center_align
                                if val_actuelle != val_suivante:
                                    if ref_start < r:
                                        worksheet_technique.merge_cells(f"D{ref_start}:D{r}")
                                        
                                    ref_start = r + 1
                        worksheet_technique[f"C{start_row}"].alignment = center_align
                        # Lien hypertexte de la Fiche Technique
                        cell_lien = worksheet_technique[f"L{start_row}"]
                        if cell_lien.value and str(cell_lien.value).startswith("http"):
                            url = cell_lien.value
                            cell_lien.value = "📄 Ouvrir la datasheet"
                            cell_lien.hyperlink = url
                            cell_lien.font = link_font
                            cell_lien.alignment = center_align
                            
        
                        # Couleurs Actif
                        cell_alerte = worksheet_technique[f"C{start_row}"]
                        if cell_alerte.value == "Actif":
                            cell_alerte.fill = PatternFill(start_color="0DF34F", fill_type="solid")
                            cell_alerte.font = Font(color="040404", bold=True)
                        elif cell_alerte.value == "Obsolète":
                            cell_alerte.fill = PatternFill(start_color="EE1212", fill_type="solid")
                            cell_alerte.font = Font(color="040404", bold=True)
                        elif cell_alerte.value == "Non Recommandé":
                                cell_alerte.fill = PatternFill(start_color="F69C0A", fill_type="solid")
                                cell_alerte.font = Font(color="040404", bold=True)
                            
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

                # Largeurs de colonnes sur-mesure
                largueurs = {'A': [20,20], 'B': [20,20], 'C':[15,15], 'D': [22,22], 'E':[15,15] , 'F': [50,15], 'G': [10,20], 'H':  [10,20], 'I':[120,20], 'J': [20,30],'K': [20,40],'L': [20,40]}
                for col_letter, width in largueurs.items():
                    worksheet_offres.column_dimensions[col_letter].width = width[0]
                    worksheet_technique.column_dimensions[col_letter].width = width[1]
            # processed_data = output.getvalue()
            # processed_data = base64.b64encode(processed_data).decode('utf-8')
            return output








    #----- (FAC) : Enregistrement données dans un fichier Excel


    # # Aplatir les données
    # lignes_excel = []

    # for produit in resultats:
    #     if "Erreur" in produit:
    #         continue
            
    #     ref = produit.get("REF_FAB", "")
    #     fab = produit.get("Fabricant", "")
    #     consensus = produit.get("Statut_Global", {}).get("Consensus", "")
    #     conflit = produit.get("Statut_Global", {}).get("Alerte_Conflit", False)
    #     detail_conflit = produit.get("Statut_Global", {}).get("Details_Distributeurs",{})
    #     datasheet = produit.get("Fiche_Technique", "")
    #     if datasheet.startswith("//"):
    #         datasheet = "https:" + datasheet
    #     offres = produit.get("Offres_Disponibles", [])
    #     if not offres:
    #         offres = [{}]

    #     for offre in offres:
    #         prix_bruts = offre.get("Prix", [])
    #         # Grille tarifaire élégante avec retours à la ligne propres (Alt+Enter)
    #         grille_str = " ".join([f"{p['Quantite']} pcs : {p['Prix_Unitaire']} €" for p in prix_bruts]) if prix_bruts else "N/A"
    #         prix_base = prix_bruts[0]['Prix_Unitaire'] if prix_bruts else "N/A"

    #         lignes_excel.append({
    #             "REF_FAB": ref,
    #             "Fabricant": fab,
                
    #             "Statut Global": consensus,
    #             "Alerte Statut": f"⚠️ Conflit : \n -Farnell : {detail_conflit.get('Farnell')} \n -Mouser : {detail_conflit.get('Mouser')}  \n -DigiKey : {detail_conflit.get('DigiKey')}" if conflit else "OK",
    #             "Distributeur": offre.get("Distributeur", "N/A"),
    #             "Conditionnement": offre.get("Conditionnement", "N/A"),
    #             "Stock Dispo": offre.get("Stock_Disponible", 0),
    #             "MOQ": offre.get("MOQ", 1),
    #             "Prix Unitaire (Base)": prix_base,
    #             "Grille Tarifaire": grille_str,
    #             "Fiche Technique": datasheet,
    #         })

    # if lignes_excel:
    #     df_export = pd.DataFrame(lignes_excel)
    #     nom_fichier = "BOM_Analyse_1357LC001_02.xlsx"
        
    #     writer = pd.ExcelWriter(nom_fichier, engine='openpyxl')
    #     df_export.to_excel(writer, index=False, sheet_name='Analyse BOM')
        
    #     workbook = writer.book
    #     worksheet = writer.sheets['Analyse BOM']
        
    #     # Styles globaux
    #     header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    #     header_font = Font(color="FFFFFF", bold=True)
    #     center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    #     left_align_top = Alignment(horizontal="left", vertical="top", wrap_text=True)
    #     link_font = Font(color="0563C1", underline="single")
        
    #     for cell in worksheet[1]:
    #         cell.fill = header_fill
    #         cell.font = header_font
    #         cell.alignment = center_align

    #     #Fusion
    #     start_row = 2
    #     for i in range(2, len(df_export) + 2):
    #         is_last_row = (i == len(df_export) + 1)
            
    #         # Condition de rupture pour les blocs globaux du composant (Cols A-E)
    #         rupture_ref = is_last_row or worksheet.cell(row=i, column=1).value != worksheet.cell(row=i+1, column=1).value
            
    #         # Gestion alignement pour la grille tarifaire (Col K)
    #         worksheet[f"J{i}"].alignment = left_align_top

    #         if rupture_ref:
    #             end_row = i
    #             if start_row < end_row:
    #                 # Fusion des informations générales
    #                 for col in ['A', 'B', 'C', 'D','K']:
    #                     worksheet.merge_cells(f"{col}{start_row}:{col}{end_row}")
    #                     worksheet[f"{col}{start_row}"].alignment = center_align

    #                 # Fusion secondaire des Distributeurs
    #                 dist_start = start_row
    #                 for r in range(start_row, end_row + 1):
    #                     val_actuelle = worksheet.cell(row=r, column=5).value
    #                     val_suivante = worksheet.cell(row=r+1, column=5).value if r < end_row else None
                        
    #                     if val_actuelle != val_suivante:
    #                         if dist_start < r:
    #                             worksheet.merge_cells(f"E{dist_start}:E{r}")
    #                             worksheet[f"E{dist_start}"].alignment = center_align
    #                         dist_start = r + 1

    #             # Lien hypertexte de la Fiche Technique
    #             cell_lien = worksheet[f"K{start_row}"]
    #             if cell_lien.value and str(cell_lien.value).startswith("http"):
    #                 url = cell_lien.value
    #                 cell_lien.value = "📄 Ouvrir le PDF"
    #                 cell_lien.hyperlink = url
    #                 cell_lien.font = link_font
    #                 cell_lien.alignment = center_align
                    
    #             # Couleurs des statuts
    #             cell_alerte = worksheet[f"D{start_row}"]
    #             if "⚠️ Conflit" in cell_alerte.value :
    #                 cell_alerte.fill = PatternFill(start_color="FFC7CE", fill_type="solid")
    #                 cell_alerte.font = Font(color="9C0006", bold=True)
    #             elif cell_alerte.value == "OK":
    #                 cell_alerte.fill = PatternFill(start_color="C6EFCE", fill_type="solid")
    #                 cell_alerte.font = Font(color="006100", bold=True)

    #             # Couleurs Actif
    #             cell_alerte = worksheet[f"C{start_row}"]
    #             if cell_alerte.value == "Actif":
    #                 cell_alerte.fill = PatternFill(start_color="0DF34F", fill_type="solid")
    #                 cell_alerte.font = Font(color="040404", bold=True)
    #             elif cell_alerte.value == "Obsolète":
    #                 cell_alerte.fill = PatternFill(start_color="EE1212", fill_type="solid")
    #                 cell_alerte.font = Font(color="040404", bold=True)
    #             elif cell_alerte.value == "Non Recommandé":
    #                     cell_alerte.fill = PatternFill(start_color="F69C0A", fill_type="solid")
    #                     cell_alerte.font = Font(color="040404", bold=True)
                    
    #             start_row = end_row + 1

    #     # Largeurs de colonnes sur-mesure
    #     largueurs = {'A': 20, 'B': 20, 'C': 20, 'D': 30, 'E': 14, 'F': 50, 'G': 10, 'H': 10, 'I': 10, 'J': 120, 'K': 30}
    #     for col_letter, width in largueurs.items():
    #         worksheet.column_dimensions[col_letter].width = width

    #     writer.close()
    #     print(f"\nFichier Excel : {nom_fichier}")



def extraire_colonnes(file_path : Path):
  """
  Goal : 
    Cette fonction Analyse les 50 premières ligne de chaque feuille d'un Classeur Excel etextrait le noms des colonnes du premier tableau identifié de la feuill. 
    Cette fonction n'est pas efficace si plusieurs tableaux sont présents dans une même feuille
  Input : Chemin de fichier Excel
  Output : Prompt IA listes entêtes de chaque feuille
  """
  try : 
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
    excel_data = pd.read_excel(file_path, sheet_name=None, header=None, nrows=50)
    texte_pour_ia = "Identify the exact column reference for the electronic components (Manufacturer Part Number,REF) and the Bill of Materials (BOM)/Nomenclature sheet. Here are the available columns per sheet:\n"
    for nom_feuille, df in excel_data.items():
        df = df.dropna(how='all').dropna(axis=1, how='all')
        if df.empty:
          continue
      
        df_bouche = df.ffill(axis=0)
        max_cases_remplies = df_bouche.count(axis=1).max()
        seuil_acceptation = max_cases_remplies * 0.8
        lignes_candidates = df_bouche[df_bouche.count(axis=1) >= seuil_acceptation]

        if lignes_candidates.empty:
          continue
        ligne_entetes_index = lignes_candidates.index[0]
        vraies_colonnes = df.loc[ligne_entetes_index].dropna().astype(str).tolist()

        vraies_colonnes = [col.strip().replace('\n', ' ') for col in vraies_colonnes if col.strip()]
        colonnes_texte = ", ".join(vraies_colonnes)
        texte_pour_ia += f"- [sheet : {nom_feuille} ( line : {ligne_entetes_index})] : {colonnes_texte}\n"
    return {"Status" : "Success", "content" : texte_pour_ia}
  except Exception as e:
    return {"Status" : "Failed", "content" : str(e)}



def extraire_liste_colonne(fichier_excel, response):
    """
    Extrait les données d'une colonne spécifique sous forme de liste de strings.
    
    :param fichier_excel: Chemin vers le fichier (str)
    :param nom_feuille: Nom de la feuille Excel (str)
    :param ligne_entete_index: Numéro de la ligne d'en-tête (Index Python commençant à 0. 
                               Si c'est la ligne 10 dans Excel, mettre 9).
    :param nom_colonne: Nom exact de la colonne (str)
    """

    try : 
      warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
      nom_feuille = response.sheet
      ligne_entete_index = response.line
      nom_colonne = response.column
      df = pd.read_excel(fichier_excel, sheet_name=nom_feuille, header=ligne_entete_index)
      df_columns = df.columns.astype(str).str.strip().str.replace('\n', ' ')

      if nom_colonne not in df_columns:
          return {"Status" : "Failed", "content" : f"La colonne '{nom_colonne}' n'existe pas à cette ligne"}
      donnees_brutes = df[nom_colonne]
      liste_strings = donnees_brutes.dropna().astype(str).str.strip().str.replace('\n', ' ').tolist()
      liste_finale = [val for val in liste_strings if val]
      
      return {"Status" : "Success", "content" : liste_finale}
    except Exception as e:
          return {"Status" : "Failed", "content" : str(e)}

