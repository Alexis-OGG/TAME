from pptx import Presentation
from classes import *
from pptx.util import Cm, Pt,Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_AUTO_SIZE,PP_ALIGN,MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement
import math
import re
import pandas as pd
import datetime as dt
# ============================================================
# Sommaire Lots Création
# ============================================================

def dessiner_diagramme_lots(slide, placeholder, liste_lots):
    """
    Dessine le diagramme des phases et des lots dans l'espace réservé.
    :param liste_lots: Liste d'objets issus de votre classe Pydantic 'Lot'
    """
    
    # 1. Regroupement des lots par phase
    # On crée un dictionnaire : {"Phase 1": [lot1, lot2], "Phase 2": [lot3]}
    groupes_phases = {}
    for lot in liste_lots:
        if lot.phase not in groupes_phases:
            groupes_phases[lot.phase] = []
        groupes_phases[lot.phase].append(lot)
        
    # 2. Coordonnées de base (issues du placeholder)
    zone_x = placeholder.left
    zone_y = placeholder.top
    zone_largeur = placeholder.width
    
    # Nettoyage du placeholder vide
    element_xml = placeholder.element
    element_xml.getparent().remove(element_xml)
    
    # 3. Paramètres de dimensionnement et couleurs
    largeur_gauche = zone_largeur * 0.25      # Le bloc phase prend 25% de la largeur
    espace_milieu = zone_largeur * 0.03       # Espace de 3% entre gauche et droite
    largeur_droite = zone_largeur * 0.72      # Les lots prennent le reste (72%)
    
    hauteur_lot = Cm(1.2)       # Hauteur d'une barre de lot
    espace_lot = Cm(0.2)        # Espace vertical entre chaque lot
    espace_phase = Cm(0.5)      # Espace vertical entre chaque grand bloc de phase
    
    # Palette de couleurs extraite de votre image
    couleur_fond_phase = RGBColor(234, 230, 223) # Beige clair
    couleur_fond_lot = RGBColor(226, 235, 244)   # Bleu/Gris très clair
    couleur_texte = RGBColor(38, 74, 127)        # Bleu foncé/Gris
    
    pos_y_courante = zone_y
    
    # 4. Boucle de dessin
    for nom_phase, lots_de_la_phase in groupes_phases.items():
        
        nb_lots = len(lots_de_la_phase)
        
        # La hauteur du grand bloc de gauche dépend du nombre de lots à droite
        hauteur_phase_totale = (nb_lots * hauteur_lot) + ((nb_lots - 1) * espace_lot)
        
        # --- A. DESSIN DU GROS BLOC GAUCHE (PHASE) ---
        bloc_gauche = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            zone_x, pos_y_courante, largeur_gauche, hauteur_phase_totale
        )
        
        # Style du bloc gauche
        bloc_gauche.fill.solid()
        bloc_gauche.fill.fore_color.rgb = couleur_fond_phase
        bloc_gauche.line.fill.background() # Pas de bordure
        
        # Texte du bloc gauche
        tf_gauche = bloc_gauche.text_frame
        tf_gauche.word_wrap = True
        p_gauche = tf_gauche.paragraphs[0]
        p_gauche.text = nom_phase
        p_gauche.font.bold = True
        p_gauche.font.size = Pt(12)
        p_gauche.font.color.rgb = couleur_texte
        p_gauche.alignment = PP_ALIGN.CENTER
        
        # --- B. DESSIN DES BLOCS DROITS (LOTS) ---
        pos_y_lot = pos_y_courante
        
        for lot in lots_de_la_phase:
            
            x_droite = zone_x + largeur_gauche + espace_milieu
            
            # 1. Le fond du bloc (Rectangle arrondi)
            bloc_droit = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                x_droite, pos_y_lot, largeur_droite, hauteur_lot
            )
            bloc_droit.fill.solid()
            bloc_droit.fill.fore_color.rgb = couleur_fond_lot
            bloc_droit.line.fill.background()
            
            # 2. Le texte du lot (intégré directement dans la forme)
            tf_droit = bloc_droit.text_frame
            # MAGIE ICI : On ajoute une marge à gauche dans la boîte de texte
            # pour laisser la place à l'icône, sans que le texte ne se superpose !
            tf_droit.margin_left = Cm(1.5) 
            
            p_droit = tf_droit.paragraphs[0]
            p_droit.text = lot.nom.upper() # Mis en majuscule comme sur l'image
            p_droit.font.bold = True
            p_droit.font.size = Pt(11)
            p_droit.font.color.rgb = couleur_texte
            p_droit.alignment = PP_ALIGN.LEFT
            
            # 3. L'icône du lot
            if lot.image_lot and lot.image_lot.strip() != "":
                try:
                    # On insère l'image par-dessus le bloc droit
                    slide.shapes.add_picture(
                        lot.image_lot, 
                        x_droite + Cm(0.3),   # Marge interne de l'image
                        pos_y_lot + Cm(0.2),  # Centrage vertical approximatif
                        height=Cm(0.8)        # L'image est plus petite que la barre (1.2cm)
                    )
                except Exception as e:
                    print(f"⚠️ Image {lot.image_lot} introuvable : {e}")
            
            # On descend pour le prochain lot
            pos_y_lot += hauteur_lot + espace_lot
            
        # On descend pour la prochaine Phase
        pos_y_courante += hauteur_phase_totale + espace_phase

# ============================================================
# REMPLISSAGE HYPOTHESES
# ============================================================

def remplir_placeholder_hypotheses(placeholder, contenu: str) -> None:
    """
    Remplit un placeholder PowerPoint en conservant les styles définis
    dans le masque selon les niveaux de paragraphes.

    Niveau 0 :
        Titre de section défini dans le masque
        Exemple : bleu, 14 pt, sans puce.

    Niveau 1 :
        Élément de liste défini dans le masque
        Exemple : gris, 12 pt, avec une puce orange.
    """

    if not placeholder.has_text_frame:
        raise ValueError(
            f"La forme '{placeholder.name}' ne possède pas de zone de texte."
        )

    text_frame = placeholder.text_frame

    # Permet au texte de revenir automatiquement à la ligne.
    text_frame.word_wrap = True

    # Réduit automatiquement la taille du texte si celui-ci dépasse
    # de la zone prévue par le masque.
    text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE

    # Supprime l'ancien contenu tout en conservant le placeholder.
    text_frame.clear()

    lignes = [
        ligne.strip()
        for ligne in contenu.splitlines()
        if ligne.strip()
    ]

    if not lignes:
        return

    for index, ligne in enumerate(lignes):
        # clear() conserve un premier paragraphe vide.
        if index == 0:
            paragraphe = text_frame.paragraphs[0]
        else:
            paragraphe = text_frame.add_paragraph()

        if ligne.startswith("-"):
            # Élément de liste utilisant le niveau 2 du masque.
            paragraphe.text = ligne.removeprefix("-").strip()
            paragraphe.font.size = Pt(12)
            paragraphe.level = 1
        else:
            # Titre de section utilisant le niveau 1 du masque.
            paragraphe.text = ligne
            paragraphe.font.size = Pt(16)
            paragraphe.level = 0

# ============================================================
# AJOUT DONNEES/LIVRABLES
# ============================================================

def dessiner_documents_lot(slide, placeholder, documents_lot):
    """
    Dessine les Données d'entrée et Livrables dans un placeholder
    à partir d'une instance du modèle Pydantic DocumentsLot.
    """
    
    # 1. Récupérer les coordonnées de la zone réservée
    zone_x = placeholder.left
    zone_y = placeholder.top
    zone_largeur = placeholder.width
    
    # 2. Supprimer le placeholder vide
    element_xml = placeholder.element
    element_xml.getparent().remove(element_xml)
    
    pos_y_courante = zone_y
    decalage_icone = Cm(0.2)
    decalage_texte = Cm(1.2)
    bleu_titre = RGBColor(79, 113, 172)
    
    # 3. Préparer une liste pour boucler proprement sur vos deux catégories
    sections = []
    
    # On n'ajoute la section que si elle contient des documents
    if documents_lot.Donnees_entree:
        sections.append(("Données d'entrée", documents_lot.Donnees_entree))
        
    if documents_lot.Livrables:
        sections.append(("Livrables", documents_lot.Livrables))
        
    # 4. Boucle de dessin
    for titre_section, liste_documents in sections:
        
        # --- DESSIN DU TITRE DE LA SECTION ---
        titre_box = slide.shapes.add_textbox(zone_x, pos_y_courante, zone_largeur, Cm(1))
        tf = titre_box.text_frame
        tf.word_wrap = True 
        
        p = tf.paragraphs[0]
        p.text = titre_section

        p.font.bold = True
        p.font.size = Pt(16) 
        p.font.color.rgb = bleu_titre
        
        pos_y_courante += Cm(1.0)
        
        # --- DESSIN DES DOCUMENTS ---
        for doc in liste_documents:
            
            # A. Icône (on vérifie si le champ n'est pas vide)
            if doc.img_doc and doc.img_doc.strip() != "":
                try:
                    slide.shapes.add_picture(
                        doc.img_doc, 
                        zone_x + decalage_icone, 
                        pos_y_courante, 
                        height=Cm(0.8)
                    )
                except Exception as e:
                    print(f"⚠️ Impossible d'insérer l'icône '{doc.img_doc}': {e}")
                    
            # B. Texte du document
            element_box = slide.shapes.add_textbox(
                zone_x + decalage_texte, 
                pos_y_courante + Cm(0.1), 
                zone_largeur - decalage_texte, 
                Cm(0.8)
            )
            tf_elem = element_box.text_frame
            tf_elem.word_wrap = True # Pour les noms de docs très longs
            
            p_elem = tf_elem.paragraphs[0]
            p_elem.text = doc.text_doc
            p_elem.font.size = Pt(11)
            
            # On descend pour le prochain document
            pos_y_courante += Cm(0.9)
            
        # Marge d'espacement avant de passer aux Livrables (si existants)
        pos_y_courante += Cm(0.6)

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
    colonnes = {"LOTS":"nom", "Durée (Semaines)":"duree","Coût du lot":"cout","Facturation":"facturation"}
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
    ecrire_cellule(table.cell(derniere_ligne, 1), f"{tot_duree}", couleur_noir, gras=True)
    ecrire_cellule(table.cell(derniere_ligne, 2), f"{tot_cout} €", couleur_noir, gras=True)
    ecrire_cellule(table.cell(derniere_ligne, 3), f"{tot_fact} €", couleur_noir, gras=True)

# ============================================================
# AJUSTEMENT DU TEXTE
# ============================================================

def injecter_texte_auto_ajuste(placeholder, texte, taille_max=18, taille_min=7):
    """
    Calcule dynamiquement la meilleure taille de police pour que le texte 
    remplisse la zone réservée sans déborder, selon ses dimensions réelles.
    """
    if not texte:
        texte = ""
        
    texte = str(texte)
    
    # 1. Récupération des dimensions physiques de la zone en Points (Pt)
    w_utile = placeholder.width.pt
    h_utile = placeholder.height.pt
    
    
    taille_optimale = taille_min # Valeur par défaut si c'est vraiment trop long
    
    # 2. Simulation d'encombrement (de la plus grande à la plus petite police)
    for taille_test in range(taille_max, taille_min - 1, -1):
        
        # En moyenne, la largeur d'un caractère est d'environ 50 à 55% de sa hauteur
        largeur_char_moyenne = taille_test * 0.55
        
        # Interligne standard (1.15 à 1.2 fois la taille de la police)
        hauteur_ligne = taille_test * 1.15 
        
        # Combien de caractères rentrent sur une seule ligne ?
        chars_par_ligne = max(1, w_utile / largeur_char_moyenne)
        
        # On calcule le nombre de lignes nécessaires (en gérant les sauts de ligne existants \n)
        paragraphes = texte.split('\n')
        nb_lignes_simulees = 0
        
        for para in paragraphes:
            if len(para) == 0:
                nb_lignes_simulees += 1 # Ligne vide
            else:
                # Calcul des retours à la ligne automatiques (word wrap)
                # On ajoute une pénalité de 10% (* 1.1) car les mots ne se coupent pas parfaitement
                lignes_du_para = math.ceil((len(para) / chars_par_ligne) * 1.1)
                nb_lignes_simulees += lignes_du_para
                
        # Hauteur totale qu'occuperait le texte avec cette police
        hauteur_simulee = nb_lignes_simulees * hauteur_ligne
        
        # Si ça rentre dans la zone, on garde cette taille et on arrête de chercher !
        if hauteur_simulee <= h_utile:
            taille_optimale = taille_test
            break

    # 3. Injection du texte avec la taille trouvée
    tf = placeholder.text_frame
    tf.clear()
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = texte
    
    # --- LA CORRECTION DU BUG DE MARGE EST TOUJOURS LÀ ---
    pPr = p._p.get_or_add_pPr()
    pPr.set('marL', '0')
    pPr.set('indent', '0')
    
    # 4. Application de la police optimale
    for run in p.runs:
        run.font.size = Pt(taille_optimale)
        run.font.name = "Poppins Light" # Optionnel : forcer la police

# ============================================================
# CREATION DU GANTT
# ============================================================


# ============================================================
# OUTILS GÉNÉRIQUES
# ============================================================

def rgb(code_hex):
    """Convertit un code hexadécimal en couleur python-pptx."""
    return RGBColor.from_string(code_hex.replace("#", "").upper())


def ajouter_rectangle(
    slide,
    x,
    y,
    largeur,
    hauteur,
    couleur,
    couleur_trait=None,
    epaisseur_trait=0.5,
):
    """Ajoute un rectangle entièrement éditable."""

    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(largeur),
        Inches(hauteur),
    )

    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(couleur)

    if couleur_trait:
        shape.line.color.rgb = rgb(couleur_trait)
        shape.line.width = Pt(epaisseur_trait)
    else:
        shape.line.fill.background()

    return shape


def ajouter_texte(
    slide,
    texte,
    x,
    y,
    largeur,
    hauteur,
    taille=9,
    couleur="263447",
    gras=False,
    alignement=PP_ALIGN.LEFT,
    police="Poppins Light",
    marge=0.02,
):
    """Ajoute une zone de texte éditable avec retour à la ligne."""

    shape = slide.shapes.add_textbox(
        Inches(x),
        Inches(y),
        Inches(largeur),
        Inches(hauteur),
    )

    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE

    frame.margin_left = Inches(marge)
    frame.margin_right = Inches(marge)
    frame.margin_top = 0
    frame.margin_bottom = 0

    paragraph = frame.paragraphs[0]
    paragraph.alignment = alignement
    paragraph.space_before = Pt(0)
    paragraph.space_after = Pt(0)

    run = paragraph.add_run()
    run.text = str(texte)
    run.font.name = police
    run.font.size = Pt(taille)
    run.font.bold = gras
    run.font.color.rgb = rgb(couleur)

    return shape


def ajouter_jalon(
    slide,
    centre_x,
    centre_y,
    taille=0.16,
    couleur="F39A23",
    couleur_trait="FFFFFF",
):
    """Ajoute un jalon en forme de losange."""

    shape = slide.shapes.add_shape(
        MSO_SHAPE.DIAMOND,
        Inches(centre_x - taille / 2),
        Inches(centre_y - taille / 2),
        Inches(taille),
        Inches(taille),
    )

    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(couleur)
    shape.line.color.rgb = rgb(couleur_trait)
    shape.line.width = Pt(0.8)

    return shape


# ============================================================
# PRÉPARATION DES DONNÉES
# ============================================================

def valider_mois_semaines(mois_semaines):
    """Valide le dictionnaire ordonné des mois."""

    if not mois_semaines:
        raise ValueError("Le dictionnaire mois_semaines est vide.")

    for mois, nombre_semaines in mois_semaines.items():
        if not isinstance(nombre_semaines, int):
            raise TypeError(
                f"Le nombre de semaines du mois « {mois} » doit être entier."
            )

        if nombre_semaines < 1:
            raise ValueError(
                f"Le mois « {mois} » doit comporter au moins une semaine."
            )

    return sum(mois_semaines.values())


def calculer_periode_parent(tache):
    """
    Calcule automatiquement la période d'une tâche parente à partir
    de ses sous-tâches si debut ou duree ne sont pas renseignés.
    """

    sous_taches = tache.get("sous_taches", []) or []

    for sous_tache in sous_taches:
        calculer_periode_parent(sous_tache)

    if sous_taches:
        debuts = [item["debut"] for item in sous_taches]
        fins = [
            item["debut"] + item["duree"] - 1
            for item in sous_taches
        ]

        tache.setdefault("debut", min(debuts))

        if "duree" not in tache:
            tache["duree"] = max(fins) - tache["debut"] + 1

    if "debut" not in tache or "duree" not in tache:
        raise ValueError(
            f"La tâche « {tache.get('nom', 'sans nom')} » "
            "doit posséder debut et duree."
        )

    return tache


def aplatir_taches(taches, niveau=0):
    """
    Transforme récursivement l'arborescence en lignes successives.

    Chaque ligne possède :
    - niveau ;
    - est_parent ;
    - debut ;
    - duree ;
    - jalons ;
    - couleur.
    """

    lignes = []

    for tache_source in taches:
        tache = dict(tache_source)
        sous_taches = tache.pop("sous_tache", []) or []

        tache["niveau"] = niveau
        tache["est_parent"] = bool(sous_taches)
        tache.setdefault("jalon", [])

        lignes.append(tache)

        lignes.extend(
            aplatir_taches(
                sous_taches,
                niveau=niveau + 1,
            )
        )

    return lignes


def preparer_taches(taches:List[Lot], nombre_semaines_tot):
    """Calcule, aplatit et valide toutes les tâches."""

    taches_preparees = []

    for tache in taches:
        copie = copier_tache(tache)
        # calculer_periode_parent(copie)
        taches_preparees.append(copie)

    lignes = aplatir_taches(taches_preparees)
    for ligne in lignes:
        nom = ligne.get("nom", "sans nom")
        debut = ligne["debut"]
        duree = ligne["duree"]
        fin = debut + duree - 1

        if debut < 1:
            raise ValueError(
                f"La tâche « {nom} » commence avant la semaine 1."
            )

        if duree <= 0:
            raise ValueError(
                f"La durée de « {nom} » doit être positive."
            )

        if fin > nombre_semaines_tot:
            raise ValueError(
                f"La tâche « {nom} » se termine en semaine {fin}, "
                f"alors que le planning contient {nombre_semaines_tot} semaines."
            )

        for jalon in getattr(ligne,"jalon",[]):
            if not 1 <= jalon <= nombre_semaines_tot:
                raise ValueError(
                    f"Le jalon S{jalon} de « {nom} » "
                    "est hors du planning."
                )

    return lignes


def copier_tache(tache:Lot):
    """Copie récursivement une tâche et ses sous-tâches."""
    copie = dict(tache)
    
    copie["sous_tache"] = [
        copier_tache(item)
        for item in getattr(tache,"sous_tache",[])
    ]

    return copie


# ============================================================
# CONSTRUCTION DU GANTT
# ============================================================

Dico_mois={
  "1": { "mois": "Janvier", "id_semaine_debut_mois": 1 , "nb_semaines" : 4},
  "2": { "mois": "Janvier", "id_semaine_debut_mois": 1 , "nb_semaines" : 4},
  "3": { "mois": "Janvier", "id_semaine_debut_mois": 1 , "nb_semaines" : 4},
  "4": { "mois": "Janvier", "id_semaine_debut_mois": 1 , "nb_semaines" : 4},
  "5": { "mois": "Février", "id_semaine_debut_mois": 5 , "nb_semaines" : 4},
  "6": { "mois": "Février", "id_semaine_debut_mois": 5 , "nb_semaines" : 4},
  "7": { "mois": "Février", "id_semaine_debut_mois": 5 , "nb_semaines" : 4},
  "8": { "mois": "Février", "id_semaine_debut_mois": 5 , "nb_semaines" : 4},
  "9": { "mois": "Mars", "id_semaine_debut_mois": 9 , "nb_semaines" : 4},
  "10": { "mois": "Mars", "id_semaine_debut_mois": 9 , "nb_semaines" : 4},
  "11": { "mois": "Mars", "id_semaine_debut_mois": 9 , "nb_semaines" : 4},
  "12": { "mois": "Mars", "id_semaine_debut_mois": 9 , "nb_semaines" : 4},
  "13": { "mois": "Avril", "id_semaine_debut_mois": 13 , "nb_semaines" : 5},
  "15": { "mois": "Avril", "id_semaine_debut_mois": 13 , "nb_semaines" : 5},
  "15": { "mois": "Avril", "id_semaine_debut_mois": 13 , "nb_semaines" : 5},
  "16": { "mois": "Avril", "id_semaine_debut_mois": 13 , "nb_semaines" : 5},
  "17": { "mois": "Avril", "id_semaine_debut_mois": 13 , "nb_semaines" : 5},
  "18": { "mois": "Mai", "id_semaine_debut_mois": 18 , "nb_semaines" : 4},
  "19": { "mois": "Mai", "id_semaine_debut_mois": 18 , "nb_semaines" : 4},
  "20": { "mois": "Mai", "id_semaine_debut_mois": 18 , "nb_semaines" : 4},
  "21": { "mois": "Mai", "id_semaine_debut_mois": 18 , "nb_semaines" : 4},
  "22": { "mois": "Juin", "id_semaine_debut_mois": 22 , "nb_semaines" : 4},
  "23": { "mois": "Juin", "id_semaine_debut_mois": 22 , "nb_semaines" : 4},
  "24": { "mois": "Juin", "id_semaine_debut_mois": 22 , "nb_semaines" : 4},
  "25": { "mois": "Juin", "id_semaine_debut_mois": 22 , "nb_semaines" : 4},
  "26": { "mois": "Juillet", "id_semaine_debut_mois": 26 , "nb_semaines" : 5},
  "27": { "mois": "Juillet", "id_semaine_debut_mois": 26 , "nb_semaines" : 5},
  "28": { "mois": "Juillet", "id_semaine_debut_mois": 26 , "nb_semaines" : 5},
  "29": { "mois": "Juillet", "id_semaine_debut_mois": 26 , "nb_semaines" : 5},
  "30": { "mois": "Juillet", "id_semaine_debut_mois": 26 , "nb_semaines" : 5},
  "31": { "mois": "Août", "id_semaine_debut_mois": 31 , "nb_semaines" : 4},
  "32": { "mois": "Août", "id_semaine_debut_mois": 31 , "nb_semaines" : 4},
  "33": { "mois": "Août", "id_semaine_debut_mois": 31 , "nb_semaines" : 4},
  "34": { "mois": "Août", "id_semaine_debut_mois": 31 , "nb_semaines" : 4},
  "35": { "mois": "Septembre", "id_semaine_debut_mois": 35 , "nb_semaines" : 4},
  "36": { "mois": "Septembre", "id_semaine_debut_mois": 35 , "nb_semaines" : 4},
  "37": { "mois": "Septembre", "id_semaine_debut_mois": 35 , "nb_semaines" : 4},
  "38": { "mois": "Septembre", "id_semaine_debut_mois": 35 , "nb_semaines" : 4},
  "39": { "mois": "Octobre", "id_semaine_debut_mois": 39 , "nb_semaines" : 5},
  "40": { "mois": "Octobre", "id_semaine_debut_mois": 39 , "nb_semaines" : 5},
  "41": { "mois": "Octobre", "id_semaine_debut_mois": 39 , "nb_semaines" : 5},
  "42": { "mois": "Octobre", "id_semaine_debut_mois": 39 , "nb_semaines" : 5},
  "43": { "mois": "Octobre", "id_semaine_debut_mois": 39 , "nb_semaines" : 5},
  "44": { "mois": "Novembre", "id_semaine_debut_mois": 44 , "nb_semaines" : 4},
  "45": { "mois": "Novembre", "id_semaine_debut_mois": 44 , "nb_semaines" : 4},
  "46": { "mois": "Novembre", "id_semaine_debut_mois": 44 , "nb_semaines" : 4},
  "47": { "mois": "Novembre", "id_semaine_debut_mois": 44 , "nb_semaines" : 4},
  "48": { "mois": "Décembre", "id_semaine_debut_mois": 48 , "nb_semaines" : 5},
  "49": { "mois": "Décembre", "id_semaine_debut_mois": 48 , "nb_semaines" : 5},
  "50": { "mois": "Décembre", "id_semaine_debut_mois": 48 , "nb_semaines" : 5},
  "51": { "mois": "Décembre", "id_semaine_debut_mois": 48 , "nb_semaines" : 5},
  "52": { "mois": "Décembre", "id_semaine_debut_mois": 48 , "nb_semaines" : 5}
}

def ajouter_gantt(
    annee,
    prs,
    layout,
    lots,
    title,
    nombre_semaines_phase,
    nombre_semaines_tot,
    debut_gantt,
    x=0.60,
    y=0.30,
    largeur=12.10,
    hauteur=5.95,
    largeur_libelles=3,
):
    """
    Ajoute un Gantt hiérarchique entièrement éditable.

    Paramètres
    ----------
    slide :
        Diapositive python-pptx cible.

    taches :
        Liste de tâches éventuellement imbriquées avec sous_taches.

    mois_semaines :
        Dictionnaire ordonné :
        {
            "Janvier": 5,
            "Février": 4,
            "Mars": 4,
            "Avril": 5,
        }

    Les valeurs debut, duree et jalons utilisent une numérotation
    continue sur l'ensemble du planning.
    """

    # Palette
    BLEU = "29529E"
    BLEU_FONCE = "173B74"
    BLEU_MOYEN = "5377B9"
    ORANGE = "F39A23"
    TEXTE = "263447"
    SECONDAIRE = "697386"
    GRILLE = "D9DEE7"
    FOND_MOIS = "F5F7FA"
    FOND_PARENT = "EAF0F8"
    BLANC = "FFFFFF"

    slide = prs.slides.add_slide(layout)
    for placeholder in slide.placeholders:
               placeholder.text = title

    lignes = preparer_taches(lots, nombre_semaines_tot+nombre_semaines_phase)

    if not lignes:
        raise ValueError("La liste des tâches est vide.")

    # Géométrie générale
    hauteur_titre = 0.65
    hauteur_entete = 0.80

    grille_x = x + largeur_libelles
    largeur_grille = largeur - largeur_libelles
    largeur_semaine = largeur_grille / nombre_semaines_phase

    lignes_y = y + hauteur_titre + hauteur_entete
    hauteur_disponible = hauteur - hauteur_titre - hauteur_entete
    hauteur_ligne = hauteur_disponible / len(lignes)


    # Accent sous le titre
    ajouter_rectangle(
        slide,
        x,
        y + hauteur_titre - 0.04,
        0.42,
        0.04,
        ORANGE,
    )

    entete_y = y + hauteur_titre

    ajouter_texte(
        slide,
        "TÂCHES ET SOUS-TÂCHES",
        x,
        entete_y,
        largeur_libelles - 0.10,
        hauteur_entete,
        taille=9,
        couleur=SECONDAIRE,
        gras=True,
    )

    # --------------------------------------------------------
    # MOIS ET SEMAINES
    # --------------------------------------------------------

    annee_gantt = int(annee) + int((debut_gantt + nombre_semaines_tot) //52)
    semaine_courante = 0
    semaine_courante_id = (debut_gantt + nombre_semaines_tot) %52
    index_mois=0
    new_year_week=0
    while semaine_courante<nombre_semaines_phase:
        semaines_dans_mois=Dico_mois[f"{int(semaine_courante_id)}"]["nb_semaines"]-semaine_courante_id+Dico_mois[f"{int(semaine_courante_id)}"]["id_semaine_debut_mois"] 
        semaines_dans_mois = semaines_dans_mois - max(0,semaine_courante+semaines_dans_mois-nombre_semaines_phase)
        mois_x = grille_x + semaine_courante * largeur_semaine
        mois_largeur = semaines_dans_mois * largeur_semaine

        # Alternance des fonds mensuels
        if index_mois % 2 == 0:
            ajouter_rectangle(
                slide,
                mois_x,
                entete_y,
                mois_largeur,
                hauteur - hauteur_titre,
                FOND_MOIS,
            )

        # Libellé du mois
        ajouter_texte(
            slide,
            Dico_mois[f"{int(semaine_courante_id)}"]["mois"].upper(),
            mois_x,
            entete_y,
            mois_largeur,
            0.36,
            taille=9,
            couleur=SECONDAIRE,
            gras=True,
            alignement=PP_ALIGN.CENTER,
        )
        # Semaines locales du mois
        for semaine_locale in range(int(semaine_courante_id-1),int(semaines_dans_mois+semaine_courante_id-1)):
            
            semaine_x = (
                grille_x
                + (semaine_courante + semaine_locale-semaine_courante_id+1)
                * largeur_semaine
            )

            ajouter_texte(
                slide,
                f"{semaine_locale}",
                semaine_x,
                entete_y + 0.38,
                largeur_semaine,
                0.34,
                taille=8,
                couleur=SECONDAIRE,
                alignement=PP_ALIGN.CENTER,
            )

        # Limite de mois plus marquée
        ajouter_rectangle(
            slide,
            mois_x,
            entete_y,
            0.012,
            hauteur - hauteur_titre,
            BLEU_MOYEN,
        )
        if (semaine_courante_id+ semaines_dans_mois) // 52 ==1 :
            reste = (semaine_courante_id+ semaines_dans_mois) % 52
            new_year_week = semaine_courante+ semaines_dans_mois-reste+1
            
            print((semaine_courante_id+ semaines_dans_mois-reste)*largeur_semaine)
            ajouter_texte(
                            slide,
                            f"{annee_gantt}",
                            grille_x,
                            y + hauteur_titre - 0.3 ,
                            (semaine_courante+ semaines_dans_mois-reste+1)*largeur_semaine,
                            0.34,
                            taille=10,
                            couleur=SECONDAIRE,
                            alignement=PP_ALIGN.CENTER,
                            gras = True
                        )
            annee_gantt +=1
            
        index_mois += 1
        semaine_courante_id = (semaine_courante_id+ semaines_dans_mois) % 52
        semaine_courante += semaines_dans_mois

    #Ajout Dernière Annee
    if ((nombre_semaines_phase+debut_gantt)%2)!=0:
         ajouter_texte(
            slide,
            f"{annee_gantt}",
            grille_x+new_year_week*largeur_semaine,
            y + hauteur_titre - 0.3 ,
            (nombre_semaines_phase-new_year_week)*largeur_semaine,
            0.34,
            taille=10,
            couleur=SECONDAIRE,
            alignement=PP_ALIGN.CENTER,
            gras = True
        )


    # Bord droit du dernier mois
    ajouter_rectangle(
        slide,
        grille_x + largeur_grille,
        entete_y,
        0.012,
        hauteur - hauteur_titre,
        BLEU_MOYEN,
    )

    # --------------------------------------------------------
    # GRILLE HEBDOMADAIRE
    # --------------------------------------------------------

    for index in range(int(nombre_semaines_phase + 1)):
        ligne_x = grille_x + index * largeur_semaine

        ajouter_rectangle(
            slide,
            ligne_x,
            entete_y + 0.70,
            0.005,
            hauteur - hauteur_titre - 0.70,
            GRILLE,
        )

    for index in range(len(lignes) + 1):
        ligne_y = lignes_y + index * hauteur_ligne

        ajouter_rectangle(
            slide,
            x,
            ligne_y,
            largeur,
            0.005,
            GRILLE,
        )

    # --------------------------------------------------------
    # TÂCHES ET SOUS-TÂCHES
    # --------------------------------------------------------

    formes_taches = []

    for index, ligne in enumerate(lignes):
        ligne_y = lignes_y + index * hauteur_ligne

        niveau = ligne["niveau"]
        est_parent = ligne["est_parent"]

        couleur_barre = ligne.get(
            "couleur",
            BLEU_FONCE if niveau==0 else BLEU,
        )

        # Fond de ligne pour les parents
        if niveau==0:
            ajouter_rectangle(
                slide,
                x,
                ligne_y + 0.006,
                largeur,
                hauteur_ligne - 0.006,
                FOND_PARENT,
            )

            ajouter_rectangle(
                slide,
                x,
                ligne_y + hauteur_ligne * 0.22,
                0.04,
                hauteur_ligne * 0.56,
                ORANGE,
            )

        # Retrait hiérarchique
        retrait = min(niveau, 4) * 0.25
        prefixe = "" if niveau == 0 else "› "

        ajouter_texte(
            slide,
            prefixe + ligne["nom"],
            x + 0.12 + retrait,
            ligne_y + 0.01,
            largeur_libelles - 0.18 - retrait,
            hauteur_ligne - 0.02,
            taille=9,
            couleur=TEXTE if niveau==0 else SECONDAIRE,
            gras=niveau==0,
        )

        # Barre
        barre_x = (
            grille_x
            + (ligne["debut"]-nombre_semaines_tot) * largeur_semaine
            
        )

        barre_largeur = (
            ligne["duree"] * largeur_semaine
            
        )

        barre_hauteur = min(
            0.22,
            hauteur_ligne * (0.38 if niveau==0 else 0.52),
        )

        barre_y = (
            ligne_y
            + (hauteur_ligne - barre_hauteur) / 2
        )
        
        barre = ajouter_rectangle(
            slide,
            barre_x,
            barre_y,
            barre_largeur,
            barre_hauteur,
            couleur_barre,
        )
        formes_taches.append(barre)

        # Embouts distinctifs des tâches parentes
        if niveau==0:
            ajouter_rectangle(
                slide,
                barre_x,
                barre_y - 0.035,
                0.03,
                barre_hauteur + 0.07,
                ORANGE,
            )

            ajouter_rectangle(
                slide,
                barre_x + barre_largeur - 0.03,
                barre_y - 0.035,
                0.03,
                barre_hauteur + 0.07,
                ORANGE,
            )

        # Jalons
        for semaine_jalon in getattr(ligne,"jalon",[]):
            centre_x = (
                grille_x
                + semaine_jalon * largeur_semaine
            )

            centre_y = ligne_y + hauteur_ligne / 2

            jalon = ajouter_jalon(
                slide,
                centre_x,
                centre_y,
                taille=min(0.16, hauteur_ligne * 0.38),
                couleur=ORANGE,
                couleur_trait=BLANC,
            )

            formes_taches.append(jalon)

    return {
        # "lignes": lignes,
        # "formes": formes_taches,
        "nombre_semaines_tot": nombre_semaines_tot+nombre_semaines_phase,
        # "largeur_semaine": largeur_semaine,
    }

# ============================================================
# CONSTRUCTION DU POWERPOINT
# ============================================================

def main(payload:PresentationData):

    #Source du Template
    prs = Presentation("input/DEV_Template.pptx")

    # Ajout Introduction
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("1_Introduction"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx

    slide.placeholders[dico["0"]].text = payload.titre_presentation
    #slide.placeholders[dico["1"]].insert_picture(payload.logo_client)
    slide.placeholders[dico["3"]].text = payload.nom_projet
    slide.placeholders[dico["2"]].text = "DEV-"+payload.id_projet+"-"+payload.Annee

    #AJout Slide Présentation TAME
    slide=prs.slides.add_slide(prs.slide_layouts.get_by_name("2_Introduction"))
    slide=prs.slides.add_slide(prs.slide_layouts.get_by_name("3_Introduction"))
    slide=prs.slides.add_slide(prs.slide_layouts.get_by_name("4_Introduction"))

    #Ajout Transition
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Transition"))
    for placeholder in slide.placeholders:
        placeholder.text = "Besoin"

    #Ajout Besoin
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Besoin"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx

    injecter_texte_auto_ajuste(slide.placeholders[dico["0"]],payload.Besoin.Avancement)
    injecter_texte_auto_ajuste(slide.placeholders[dico["1"]],payload.Besoin.Besoin)
    injecter_texte_auto_ajuste(slide.placeholders[dico["2"]],payload.Besoin.Role_TAME)
    # slide.placeholders[dico["0"]].text_frame.paragraphs[0].text = payload.Besoin.Avancement
    
    # slide.placeholders[dico["1"]].text_frame.paragraphs[0].text = payload.Besoin.Besoin
    # slide.placeholders[dico["2"]].text_frame.paragraphs[0].text = payload.Besoin.Role_TAME

    #Ajout Données d'entrée
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Entrees"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx
    slide.placeholders[dico["0"]].text = "Données d'entrée"
    slide.placeholders[dico["1"]].text= payload.donnees_entree

    #Ajout les hypothèses
    for hyp in payload.hypotheses:
        slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("1_Hypotheses"))
        dico={}
        for index,placeholder in enumerate(slide.placeholders):
            dico[f"{index}"] = placeholder.placeholder_format.idx
        slide.placeholders[dico["0"]].text = hyp.Type_Hypothese
        remplir_placeholder_hypotheses(slide.placeholders[dico["1"]], hyp.List_Hypotheses)

    #Ajout SOmmaire Lot
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Sommaire_lots"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx  
    dessiner_diagramme_lots(slide, slide.placeholders[dico["0"]], payload.lots_list.lots)
    slide.placeholders[dico["1"]].text = payload.entreprise
    #AJout de chaque diapo Lot
    for lot in payload.lots_list.lots:
            slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Lot"))
            dico={}
            for index,placeholder in enumerate(slide.placeholders):
                dico[f"{index}"] = placeholder.placeholder_format.idx
            remplir_placeholder_hypotheses(slide.placeholders[dico["3"]], lot.details_lot)
            slide.placeholders[dico["0"]].text = lot.nom
            slide.shapes.add_picture(lot.image_lot,slide.placeholders[dico["1"]].left,slide.placeholders[dico["1"]].top,slide.placeholders[dico["1"]].width*0.85,slide.placeholders[dico["1"]].height*0.85)
            slide.placeholders[dico["1"]].element.getparent().remove(slide.placeholders[dico["1"]].element)
            dessiner_documents_lot(slide,slide.placeholders[dico["2"]],lot.documents)

    #Ajout Transition
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Transition"))
    for placeholder in slide.placeholders:
        placeholder.text = "Synthèse"

    #Ajout Synthèse
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Synthese_finance"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx
    slide.placeholders[dico["1"]].text = "Synthèse"
    dessiner_tableau_dynamique(slide,slide.placeholders[dico["0"]],payload.lots_list)

    #Ajout du Planning
    debut_gantt_init=45
    nombre_semaines_tot=1

    #TRi des lots par phase
    tri_lots_phases = {}
    for lot in payload.lots_list.lots:
        if not tri_lots_phases.get(lot.phase,{}):
            tri_lots_phases[lot.phase]={"lots":[lot],"nb_semaines":lot.duree+lot.debut}
        else:
            tri_lots_phases[lot.phase]["lots"].append(lot) 
            tri_lots_phases[lot.phase]["nb_semaines"] =lot.duree +lot.debut
    #Création d"une slide planning par phase
    
    for nom_phase,liste_lot in tri_lots_phases.items():

        donnee = ajouter_gantt(
                annee = payload.Annee,
                prs = prs,
                layout=prs.slide_layouts.get_by_name("Planning"),
                title = f"Planning - {nom_phase}",
                lots=liste_lot["lots"],
                nombre_semaines_tot=nombre_semaines_tot,
                nombre_semaines_phase=liste_lot["nb_semaines"]-nombre_semaines_tot,
                debut_gantt=debut_gantt_init,
        )
         #ID Semaine début de gantt par phase
        nombre_semaines_tot = donnee["nombre_semaines_tot"]
        print("==========")
        print(nombre_semaines_tot)

    #Ajout Transition
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Transition"))
    for placeholder in slide.placeholders:
        placeholder.text = "Annexes"

    #Ajout propriété intellectuelles
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Prop_int"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
            dico[f"{index}"] = placeholder.placeholder_format.idx  
    slide.placeholders[dico["1"]].text = "PROPRIETE INTELLECTUELLE"

    objectif="" # à ajouter dans le payload
    text =f"""Domaine de l'offre
\tLe DOMAINE couvert par cette offre est « {objectif} ».
Connaissances propres
\tChaque Partie reste propriétaire de ses Connaissances Propres ou antérieures. À ce titre, chaque Partie reste libre d'exploiter ses Connaissances Propres ou antérieures comme bon lui semble. Lorsqu'elle emploie pour l'exécution du projet ses Connaissances Propres ou antérieures, TRONICO concède à {payload.entreprise}, sans frais additionnel au prix de la Commande, une licence d'exploitation des droits afférents. Cette licence sur les Connaissances Propres ou antérieures est concédée pour permettre à {payload.entreprise} de jouir pleinement des droits dont elle dispose sur les Résultats conformément aux dispositions de l'article « Résultats » de la présente proposition. Cette licence est concédée uniquement pour les Connaissances Propres ou antérieures qui font parties des Résultats.

Résultats
\tLes droits de propriété intellectuelle attachés aux Résultats ainsi que les livrables associés sont la propriété de {payload.entreprise} après paiement des factures dues à TRONICO. TRONICO bénéficie d'une licence non-exclusive d'exploitation des Résultats pour satisfaire tous besoins de son choix ou toute demande d'un autre client en dehors du Domaine.
"""
    text_frame = slide.placeholders[dico["0"]].text_frame
    for i, ligne in enumerate(text.split('\n')):
        if not ligne.strip():
            continue # Ignore les lignes vides
            
        niveau = ligne.count('\t')
        texte_propre = ligne.strip()
        
        if len(text_frame.paragraphs) == 0 or (i == 0 and text_frame.paragraphs[0].text == ""):
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()
        if niveau == 1 :
            p.font.name = "Poppins Light"
        p.text = texte_propre
        p.level = niveau
        p.alignment = PP_ALIGN.JUSTIFY

    avance=""
    text = f"""Non-sollicitation
\t{payload.entreprise} s'interdit expressément, pendant la durée du projet défini dans la présente proposition et vingt-quatre (24) mois après son expiration, de solliciter en vue d'une embauche ou d'embaucher directement ou indirectement tout membre du personnel de TRONICO.  
\tEn cas d'infraction à la présente interdiction, {payload.entreprise} sera tenue de payer immédiatement à TRONICO, à titre de clause pénale, une indemnité forfaitaire d'un montant égal à six (6) mois du dernier salaire brut mensuel de la personne sollicitée ou embauchée, majorée de tous les frais de recrutement d'un remplaçant.

Validité
\tCette proposition est valide pour une durée de 1 mois.
\tTRONICO ne peut être tenue pour responsable de toute anomalie consécutive à une information qu'elle n'aurait pas reçue. Les informations prises en compte sont la présente offre technique, le document de référence, et d'éventuels documents remis au cours de la réunion de lancement d'affaire.

Garantie
\tLa période de garantie pour les défauts de conception ou de fabrication de matériel est d'un an à compter de la date de livraison. 
\tLa garantie ne s'applique pas aux cartes d'évaluation et POC et si {payload.entreprise} :
\t\tutilise mal les produits et l'équipement, 
\t\test négligent dans le stockage, l'entretien ou l'utilisation des produits et de l'équipement, 
\t\tmodifie ou fait modifier par des tiers les produits ou les équipements, 
\t\teffectue ou fait effectuer par des tiers des réparations ou des mises à niveau des produits, à moins que le vendeur n'y ait expressément consenti.

Conditions de paiement
\t[COMPLETER]% du montant global du projet facturés à la commande.
\tPaiement à [COMPLETER]
\tTronico étant agrémenté CIR, les lots de développement définis dans cette proposition peuvent donner droit à des crédits d'impôt après facturation.



"""
    #Ajout condictions générales de ventes
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Cond_vente"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
            dico[f"{index}"] = placeholder.placeholder_format.idx  
    slide.placeholders[dico["1"]].text = "CONDITIONS générales de l'étude"
    text_frame = slide.placeholders[dico["0"]].text_frame
    for i, ligne in enumerate(text.split('\n')):
            if not ligne.strip():
                continue # Ignore les lignes vides
                
            niveau = ligne.count('\t')
            texte_propre = ligne.strip()
            
            if len(text_frame.paragraphs) == 0 or (i == 0 and text_frame.paragraphs[0].text == ""):
                p = text_frame.paragraphs[0]
            else:
                p = text_frame.add_paragraph()
            if niveau == 1 :
                p.font.name = "Poppins Light"
            p.level = niveau
            p.alignment = PP_ALIGN.JUSTIFY

            morceaux = re.split(r'(\[[^\]]+\])', texte_propre)

            for morceau in morceaux:
                if not morceau:
                    continue
                run = p.add_run()
                run.text = morceau
                
                # Si le morceau est entouré de crochets, on le colore en rouge
                if morceau.startswith('[') and morceau.endswith(']'):
                    run.font.color.rgb = RGBColor(255, 0, 0)
                    run.font.bold = True
    

    #Ajout Conditions générales de vente
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("1_CGDV"))
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("2_CGDV"))

    #Sauvegarde
    prs.save('output/output.pptx')


#Zone de tests
if __name__ == "__main__" :

    #Exemple ICONEUS
    test = PresentationData(
            titre_presentation="PROPOSITION TECHNIQUE & FINANCIÈRE",
            logo_client = "img/Image2.png",
            nom_projet="ICONEUS - Multiplexer probe",
            Annee="23/07/2026",
            entreprise="ICONEUS",
            id_projet="000970_01",
            donnees_entree = "Cdc",
            Besoin =Besoin(
                Avancement= "ICONEUS à transmis un cahier des charges présenté aux équipes le 24 juin. Des échanges au travers d'un Tame-Carefichier questions / réponses ont ensuite permis de compléter la description du besoin.",
                Besoin="L'objectif est de concevoir et fabriquer des prototypes fonctionnels d'un multiplexeur 1=4 permettant l'interconnexion entre le générateur US et une sonde matricielle 1024 voies du système d'échographe ZEUS. ",
                Role_TAME ="ICONEUS sollicite Tronico Tame-Care pour l'accompagner dans les différentes étapes d'une conception (HW, Mécanique et firmware) et d'une industrialisation, conformes aux règles de développement et de fabrication d'un sous ensemble devant être intégré dans un dispositif médical."
            ), 
            hypotheses = [Hypothese(
                Type_Hypothese= "Hypothèses ÉlectroniqueS",
                List_Hypotheses = "Architecture électronique\n- L'électronique est constituée d'une carte multiplexage principale et de 6 cartes « interposers » identiques\n- Les cartes « interposers » assurent la liaison entre le connecteur DLP408 du générateur ultrason et la carte de multiplexage\n- La carte de multiplexage intègre le connecteur FX11LB-140P-SV(21) assurant l'interface avec la sonde\n\nChaine de multiplexage\n- Réalisation du multiplexage via des commutateurs analogiques pilotés individuellement\n- L'architecture permet la gestion des 1024 voies de la sonde conformément aux configurations reçues\n- Le temps maximum de commutation visé est de 5µs\n\nCommande et supervision\n- Un microcontrôleur assure l'interface de communication SPI avec le générateur ultrason\n- Le microcontrôleur pilote et synchronise les circuits de multiplexage\n- Acquisition des informations de 3 sondes de température\n\nAlimentation\n- L'ensemble des alimentations nécessaires au fonctionnement de la carte est fourni par le générateur ultrason\n- La puissance disponible sur les interfaces d'alimentation est supposée compatible avec les besoins de l'électronique proposée\n- Filtrage des alimentations\n\nSignaux ultrasonores\n- L'architecture est compatible avec des signaux ultrasonores jusqu'à ±100V\n- La conception est dimensionnée pour une fréquence de fonctionnement de 2MHz, avec une évolution future de 15MHz\n- Les voies sont conçues pour respecter une adaptation d'impédance de 50Ω."
            )],
            lots_list = SyntheseFinanciere(
                lots=[Lot(
                    phase = "PHASE 1 : PROTOTYPE A",
                    nom = "LOT1 = Spécification Technique du Besoin (SR)",
                    image_lot = "img/technique.png",
                    details_lot ="""Objectif : 
        - Consolider les données d'entrée afin d'affiner les spécifications du dispositif selon les besoins utilisateur, du fonctionnement technique et des performances revendiquées par Iconeus
        Activités 
        - Cahier des charges techniques (TRS)
        - Matrice de conformité (CM)
        - Initialisation de la liste des composants critiques (LCC)
        
        Hors périmètre = Analyse de risque système
        
        
        """,
                    documents = DocumentsLot(
                        Donnees_entree= [Document(img_doc ="img/doc_bleu.png" , text_doc ="Données techniques pour s'interfacer avec la sonde et le générateur US")],
                        Livrables = [Document(img_doc ="img/doc_orange.png" , text_doc ="CdC technique (TRS)")]
                    ),
                    # donnees_tableau={"LOTS":"Lot 0 : Réunion de lancement (KOR)", "DONNÉES D'ENTRÉE":"- Cahier des charges client", "ACTIVITÉS":"- Mise en place des outils de gestion projet - Réunion de lancement (KOM)", "LIVRABLES":"CR KOM", "DÉLAIS":"1 sem", "PRIX DU LOT":"1071", "FACTURATION":"78338"}
                    # )]
                    debut = 1,
                    duree = 2,
                    cout = 1000,
                    facturation = 5000,
                    jalon = [2],
                    sous_tache = [SubTache(
                        nom = "Tache n°1",
                        duree=1,
                        debut=1,
                        jalon = None,
                        couleur="5377B9"
                    )])
                ]
            ),
        )

    
    import json

    with open(
        "devis_betabeam_rack_balayage_v2.json",
        "r",
        encoding="utf-8"
    ) as fichier:
        donnees = json.load(fichier)

    test = PresentationData(**donnees)
    # Exemple BETABEAMS


    main(test)

    