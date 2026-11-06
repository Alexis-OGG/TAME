from pptx.enum.text import MSO_AUTO_SIZE,PP_ALIGN
from pptx.util import Pt
from PIL import ImageFont, ImageDraw, Image
import os

#Style de bases
tailles_base = {
    0: {'taille_pt': 14, 'space_after_pt': 6, 'line_spacing': 0.9},
    1: {'taille_pt': 12, 'space_after_pt': 4, 'line_spacing': 0.9},
    2: {'taille_pt': 11, 'space_after_pt': 4, 'line_spacing': 0.9},
    3: {'taille_pt': 11, 'space_after_pt': 4, 'line_spacing': 0.9},
    4: {'taille_pt': 11, 'space_after_pt': 4, 'line_spacing': 0.9},
    5: {'taille_pt': 11, 'space_after_pt': 4, 'line_spacing': 0.9}
}

def calculer_reduction_proporionnelle(contenu, largeur_max_pt, hauteur_max_pt,nb_colonnes,chemin_police=os.path.join(os.path.dirname(os.path.dirname(__file__)),"assets","poppins-light.ttf")):
    # Définition des tailles par défaut selon vos niveaux
    hauteur_max_pt = hauteur_max_pt*nb_colonnes
    largeur_max_pt =(largeur_max_pt - (14 * (nb_colonnes - 1))) / nb_colonnes
    
    
    reduction_pt = 0
    image_virtuelle = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(image_virtuelle)
    
    # Pré-calculer les niveaux pour chaque ligne
    lignes_analysees = []
    for ligne in contenu.split('\n'):
        if not ligne.strip():
            continue
        niveau = ligne.count('\t')
        texte_propre = ligne.strip().removeprefix("-").strip()
        lignes_analysees.append((niveau, texte_propre))
    
    # Boucle de réduction : on enlève 1 point à toutes les polices jusqu'à ce que ça rentre
    while True:
        hauteur_totale = 0
        
        for niveau, texte in lignes_analysees:
            # Calcul de la taille actuelle pour ce niveau
            taille_actuelle = max(5, tailles_base.get(niveau, {}).get("taille_pt",11) - reduction_pt)
            
            font = ImageFont.truetype(chemin_police, taille_actuelle)
            
            # Simulation du retour à la ligne automatique (Word Wrap)
            lignes_visuelles = 1
            mots = texte.split(' ')
            ligne_en_cours = ""
            largeur_effective_ligne_pt = largeur_max_pt - (niveau * 18)
            largeur_effective_ligne_pt = max(50, largeur_effective_ligne_pt)
            for mot in mots:
                test_ligne = f"{ligne_en_cours} {mot}".strip()
                if draw.textlength(test_ligne, font=font) <= largeur_effective_ligne_pt:
                    ligne_en_cours = test_ligne
                else:
                    lignes_visuelles += 1
                    ligne_en_cours = mot
                    
            # Calcul de la hauteur de ce paragraphe (bbox[3] - bbox[1] = hauteur d'un caractère)
            bbox = font.getbbox("A")
            hauteur_ligne = (bbox[3] - bbox[1]) * 1.2 # Facteur 1.2 pour l'interligne standard
            hauteur_totale += lignes_visuelles * hauteur_ligne
            
            # Ajout de l'espacement après paragraphe (ex: 6 pt d'espace visuel)
            hauteur_totale += 6 

        # Vérification si le texte complet rentre dans la boîte
        if hauteur_totale <= hauteur_max_pt:
            return reduction_pt
            
        # Sécurité : si on a réduit toutes les polices au minimum de 5 pt et que ça dépasse toujours
        if reduction_pt >= 11: 
            return reduction_pt
            
        reduction_pt += 1

# ============================================================
# REMPLISSAGE HYPOTHESES
# ============================================================

def Ajouter_texte(placeholder, contenu: str,nb_colonnes:int=1) -> None:
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
    text_frame.word_wrap = True
    text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    
    
    # 1. On vide le texte par défaut du template de manière "douce" 
    # pour conserver les propriétés XML (marges, couleurs)
    for p in text_frame.paragraphs:
        p.text = ""

    index_paragraphe = 0

    largeur_boite_pt = placeholder.width.pt
    hauteur_boite_pt = placeholder.height.pt

    # B. Calculer combien de points il faut enlever à toutes les polices
    reduction = calculer_reduction_proporionnelle(contenu, largeur_boite_pt, hauteur_boite_pt,nb_colonnes)
    for ligne in contenu.split('\n'):
        if not ligne.strip():
            continue 

        niveau = ligne.count('\t')
        
        texte_propre = ligne.strip()
        if texte_propre.startswith("-"):
            texte_propre = texte_propre.removeprefix("-").strip()

        # 2. Recyclage des paragraphes existants ou création de nouveaux
        if index_paragraphe < len(text_frame.paragraphs):
            paragraphe = text_frame.paragraphs[index_paragraphe]
        else:
            paragraphe = text_frame.add_paragraph()

        # 3. RÈGLE D'OR : Le texte en premier, le niveau ensuite.
        # Aucune autre modification (pas de police, pas d'alignement).
        paragraphe.text = texte_propre
        paragraphe.level = niveau
        paragraphe.font.size= Pt(float(tailles_base.get(niveau, {}).get("taille_pt",11))) - Pt(float(reduction))
        paragraphe.line_spacing = tailles_base.get(niveau, {}).get("line_spacing",0.9) - reduction/10
        index_paragraphe += 1

if __name__ == "__main__" :
    pass