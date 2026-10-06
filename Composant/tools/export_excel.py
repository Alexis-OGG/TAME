from openpyxl.styles import Alignment, PatternFill, Font
import pandas as pd
import io

def exporter_excel(resultats:dict):
    lignes_excel_offres = [] 
    lignes_excel_technique = []

    if resultats == {}:
        return None
    for ref,produit in resultats.items():
            if "Erreur" in produit:
                continue
                
            # ref = produit.get("REF_FAB", "")
            fab = produit["main"].get("Fabricant", "")
            consensus = produit["main"].get("Statut_Global", {}).get("Consensus", "")
            conflit = produit["main"].get("Statut_Global", {}).get("Alerte_Conflit", False)
            detail_conflit = produit["main"].get("Statut_Global", {}).get("Details_Distributeurs",{})
            datasheet = produit["main"].get("Fiche_Technique", "")

            for ref_fab, donnees in produit.items():
                if ref_fab =="main":
                    continue
                technique=produit[ref_fab]["techniques"]
                lignes_excel_technique.append({
                    "REF": ref,
                    "Fabricant": fab,
                    "Statut Global": consensus,
                    "REF_Fab" : ref_fab,
                    "Température de fonctionnement":technique[0].get("Temp_fonc"),
                    "Température de stockage":technique[0].get("Temp_stock"),
                    "Humidité":technique[0].get("humidity"),
                    "Status Rohs":technique[0].get("Rohs"),
                    "Statut Reach":technique[0].get( "Reach"),
                    "Boîtier":technique[0].get("boitier"),
                    "Dimensions":technique[0].get("Dimensions"),
                    "Fiche technique" : datasheet
                })
                for offre in donnees["offres"]:   
                    lignes_excel_offres.append({
                        "REF": ref,
                        "Fabricant": fab,
                        "Statut Global": consensus,
                        "Alerte Statut": f"⚠️ Conflit" if conflit else "OK",
                        "REF_Fab" : ref_fab,
                        "Distributeur": offre.get("Distributeur", "N/A"),
                        "Conditionnement": offre.get("Conditionnement", "N/A"),
                        "Stock Dispo": offre.get("Stock", 0),
                        "MOQ": offre.get("MOQ", 1),
                        "Grille Tarifaire": offre.get("Prix_Unitaire", []),
                    })
        
    if lignes_excel_offres and lignes_excel_technique:
            df_offres = pd.DataFrame(lignes_excel_offres)
            df_technique = pd.DataFrame(lignes_excel_technique)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df_offres.to_excel(writer, index=False, sheet_name='Achat')
                df_technique.to_excel(writer, index=False, sheet_name='Technique')
                
                workbook = writer.book
                worksheet_offres = writer.sheets['Achat']
                worksheet_technique = writer.sheets['Technique']
                for sheet_name in workbook.sheetnames:
                    worksheet = workbook[sheet_name]
                    worksheet.freeze_panes = "D1"
                # Styles globaux
                header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
                header_font = Font(color="FFFFFF", bold=True)
                center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
                left_align_top = Alignment(horizontal="left", vertical="top", wrap_text=True)
                link_font = Font(color="0563C1", underline="single")
                
                for cell in worksheet_offres[1]:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = center_align
                for cell in worksheet_technique[1]:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = center_align

                #Fusion
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
                            for col in ['A', 'B', 'C', 'D']:
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
                            
                        # Couleurs des statuts
                        cell_alerte = worksheet_offres[f"D{start_row}"]
                        if "⚠️ Conflit" in cell_alerte.value :
                            cell_alerte.fill = PatternFill(start_color="FFC7CE", fill_type="solid")
                            cell_alerte.font = Font(color="9C0006", bold=True)
                        elif cell_alerte.value == "OK":
                            cell_alerte.fill = PatternFill(start_color="C6EFCE", fill_type="solid")
                            cell_alerte.font = Font(color="006100", bold=True)
        
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
                            for col in ['A', 'B', 'C','L']:
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
                        
                # Largeurs de colonnes sur-mesure
                largueurs = {'A': [20,20], 'B': [20,20], 'C':[15,15], 'D': [30,22], 'E': [22,15], 'F':[15,15] , 'G': [50,15], 'H': [10,20], 'I': [10,15], 'J': [120,20],'K': [20,50],'L': [20,40]}
                for col_letter, width in largueurs.items():
                    worksheet_offres.column_dimensions[col_letter].width = width[0]
                    worksheet_technique.column_dimensions[col_letter].width = width[1]
            processed_data = output.getvalue()
            return processed_data








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
