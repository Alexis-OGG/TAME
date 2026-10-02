
from classes import *

from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
# ============================================================
# AJOUT TABLEAU SYNTHESE
# ============================================================


def set_dashed_borders(cell):
    """Applique une bordure noire en pointillés (dash) aux 4 côtés d'une cellule."""
    tcPr = cell._tc.get_or_add_tcPr()
    # lnL = Left, lnR = Right, lnT = Top, lnB = Bottom
    for border_name in ['a:lnL', 'a:lnR', 'a:lnT', 'a:lnB']:
        ln = OxmlElement(border_name)
        ln.set('w', str(Pt(0.75))) # Épaisseur de la ligne
        
        # Couleur noire
        solidFill = OxmlElement('a:solidFill')
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', '000000')
        solidFill.append(srgbClr)
        ln.append(solidFill)
        
        # Style pointillé (sysDash, dash, ou sysDot)
        prstDash = OxmlElement('a:prstDash')
        prstDash.set('val', 'sysDash') 
        ln.append(prstDash)
        
        tcPr.append(ln)


def dessiner_tableau_dynamique(slide, placeholder, donnees_synthese: SyntheseFinanciere):
    """
    Génère un tableau dont la taille et le contenu sont dictés par l'IA.
    """
    # 1. Dimensions
    left = placeholder.left
    top = placeholder.top
    width = placeholder.width
    height = placeholder.height
    
    # Nettoyage
    element_xml = placeholder.element
    element_xml.getparent().remove(element_xml)
    colonnes = {"LOTS":"nom", "Durée (Semaines)":"duree","Facturation":"facturation"} #"Coût du lot":"cout"
    tot_duree=0
    tot_cout=0
    tot_fact=0
    lots = donnees_synthese.lots
    
    nb_colonnes = len(colonnes)
    if nb_colonnes == 0:
        return 
        
    nb_lignes = len(lots) + 2
    
    # 3. Création du tableau
    shape_tableau = slide.shapes.add_table(nb_lignes, nb_colonnes, left, top, width, height)
    table = shape_tableau.table
    
    # 4. Largeur des colonnes (Répartition égale automatique)
    
    largeur_colonne = int(width / nb_colonnes)
    for i in range(nb_colonnes):
        table.columns[i].width = largeur_colonne

    # --- Fonction utilitaire (avec correction des marges) ---
    def ecrire_cellule(cellule, texte, couleur, gras=False):
        cellule.text = str(texte)

        p = cellule.text_frame.paragraphs[0]
        p.font.color.rgb = couleur
        p.font.bold = gras
        p.font.size = Pt(9)
        p.alignment = PP_ALIGN.CENTER
        cellule.fill.transparency = 0.5
        cellule.vertical_anchor = 3 # Milieu
        
        # Annulation des puces cachées
        pPr = p._p.get_or_add_pPr()
        pPr.set('marL', '0')
        pPr.set('indent', '0')

    couleur_blanc = RGBColor(255, 255, 255)
    couleur_noir = RGBColor(0, 0, 0)

    # 5. REMPLISSAGE DE L'EN-TÊTE
    for col_idx, nom_colonne in enumerate(colonnes):
        ecrire_cellule(table.cell(0, col_idx), nom_colonne, couleur_blanc)
        table.cell(0, col_idx).fill.solid()
        table.cell(0, col_idx).fill.fore_color.rgb = RGBColor(48, 84, 150)

    # 6. REMPLISSAGE DES LIGNES (LOTS)
    for row_idx, lot in enumerate(lots, start=1):
        for col_idx, nom_colonne in enumerate(colonnes):
            valeur_cellule = getattr(lot,colonnes[nom_colonne])
            if col_idx>1: valeur_cellule = f"{valeur_cellule} €"
            # On met en gras la première colonne pour faire ressortir le nom du lot
            set_dashed_borders(table.cell(row_idx, col_idx))
            ecrire_cellule(table.cell(row_idx, col_idx), valeur_cellule, couleur_noir)
            table.cell(row_idx, col_idx).fill.solid()
            table.cell(row_idx, col_idx).fill.fore_color.rgb = couleur_blanc

        tot_duree+= getattr(lot,"duree")
        tot_cout+=getattr(lot,"cout")
        tot_fact+=getattr(lot,"facturation")

    derniere_ligne = nb_lignes - 1
    for col_idx, nom_colonne in enumerate(colonnes):

        set_dashed_borders(table.cell(derniere_ligne, col_idx))
        table.cell(derniere_ligne, col_idx).fill.solid()
        table.cell(derniere_ligne, col_idx).fill.fore_color.rgb = RGBColor(244, 118, 55)


    ecrire_cellule(table.cell(derniere_ligne, 0), "Total", couleur_noir, gras=True)
    ecrire_cellule(table.cell(derniere_ligne, 1), f"{round(tot_duree,ndigits=2)}", couleur_noir, gras=True)
    ecrire_cellule(table.cell(derniere_ligne, 2), f"{round(tot_cout,ndigits=2)} €", couleur_noir, gras=True)
    # ecrire_cellule(table.cell(derniere_ligne, 3), f"{round(tot_fact,ndigits=2)} €", couleur_noir, gras=True)

if __name__ == "__main__" :
    pass