from classes import *

from pptx.dml.color import RGBColor
from pptx.util import Pt,Inches
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
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

        if debut < 0:
            raise ValueError(
                f"La tâche « {nom} » commence avant la semaine 1."
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
  "52": { "mois": "Décembre", "id_semaine_debut_mois": 48 , "nb_semaines" : 5},
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
    largeur_semaine = largeur_grille / round(nombre_semaines_phase+0.49)

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
    semaine_courante_id = round((debut_gantt + nombre_semaines_tot) %52,ndigits=2)
    index_mois=0
    new_year_week=0

    while semaine_courante<nombre_semaines_phase:
        
        semaines_dans_mois=Dico_mois[f"{int(semaine_courante_id)}"]["nb_semaines"]-semaine_courante_id+Dico_mois[f"{int(semaine_courante_id)}"]["id_semaine_debut_mois"] 
        semaines_dans_mois = round(semaines_dans_mois - max(0,semaine_courante+semaines_dans_mois-nombre_semaines_phase),ndigits=2)
        # print(f"title : {title} tot : {nombre_semaines_phase} , act : {semaine_courante}, nm_sem : {semaines_dans_mois},sem_cour : {semaine_courante_id }")
        mois_x = grille_x + round(semaine_courante+0.49) * largeur_semaine
        mois_largeur = round(semaines_dans_mois+0.49) * largeur_semaine

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
        for semaine_locale in range(int(semaine_courante_id),round(semaines_dans_mois+semaine_courante_id)):
            # print(round((semaine_courante + semaine_locale-int(semaine_courante_id))+0.49))
            semaine_x = (
                grille_x
                + round((semaine_courante + semaine_locale-int(semaine_courante_id))+0.49)
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

            ajouter_texte(
                            slide,
                            f"{annee_gantt}",
                            grille_x+new_year_week*largeur_semaine,
                            y + hauteur_titre - 0.3 ,
                            round(semaine_courante+ semaines_dans_mois+0.49)*largeur_semaine,
                            0.34,
                            taille=10,
                            couleur=SECONDAIRE,
                            alignement=PP_ALIGN.CENTER,
                            gras = True
                        )
            new_year_week = round(semaine_courante+ semaines_dans_mois+0.49)
            annee_gantt +=1
            
        index_mois += 1
        semaine_courante_id = (semaine_courante_id+ semaines_dans_mois) % 52
        semaine_courante += semaines_dans_mois

    #Ajout Dernière Annee
    
    if (round(nombre_semaines_phase+debut_gantt+0.49)%52)!=0:
        #  print(new_year_week)
         ajouter_texte(
            slide,
            f"{annee_gantt}",
            grille_x+new_year_week*largeur_semaine,
            y + hauteur_titre - 0.3 ,
            round(nombre_semaines_phase-new_year_week+0.49)*largeur_semaine,
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

        #Vacances
        
        (ligne["debut"]-nombre_semaines_tot)
        # Barre
        barre_x = (
            grille_x
            + ((ligne["debut"]-int(nombre_semaines_tot))) * largeur_semaine
            
        )

        barre_largeur = (
            (ligne["duree"]) * largeur_semaine
            
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


if __name__ == "__main__" :
    pass