from pptx.util import Pt
import math
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

if __name__ == "__main__" :
    pass