
#Import modules
from classes import *
from generate_table import dessiner_tableau_dynamique
from generate_gantt import ajouter_gantt,largeur_libelles
from lots_handling import dessiner_documents_lot, dessiner_diagramme_lots,resolve_asset_path
from feed_hypothesis import Ajouter_texte
# from text_handling import Ajouter_texte
import sys
#Import librairies
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import re
import json
import argparse
from pathlib import Path

# ============================================================
# CONSTRUCTION DU POWERPOINT
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_DIR / "assets"



def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-json",
        type=Path,
        required=True,
        help="Chemin du JSON PresentationData validé"
    )

    parser.add_argument(
        "--img1",
        type=Path,
        required=False,
        help="Chemin de la première image"
    )

    parser.add_argument(
        "--img2",
        type=Path,
        required=False,
        help="Chemin de la deuxième image"
    )

    parser.add_argument(
        "--img3",
        type=Path,
        required=False,
        help="Chemin de la troisième image"
    )

    parser.add_argument(
        "--img4",
        type=Path,
        required=False,
        help="Chemin de la quatrième image"
    )

    parser.add_argument(
        "--img5",
        type=Path,
        required=False,
        help="Chemin de la cinquième image"
    )

    parser.add_argument(
        "--img6",
        type=Path,
        required=False,
        help="Chemin de la sixième image"
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Chemin du PowerPoint généré"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    with args.input_json.open("r", encoding="utf-8") as f:
        data = json.load(f)
        payload = PresentationData(**data)
    out = args.output

    #Images générés
    image1 = args.img1
    image2 = args.img2
    image3 = args.img3
    image4 = args.img4
    image5 = args.img5
    image6 = args.img6
    #Source du Template
    SCRIPT_DIR = Path(__file__).resolve().parent
    SKILL_DIR = SCRIPT_DIR.parent

    template_path = SKILL_DIR / "assets" / "DEV_Template.pptx"

    prs = Presentation(template_path)
    # prs = Presentation("assets/DEV_Template.pptx")

    # Ajout Introduction
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("1_Introduction"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx

    slide.placeholders[dico["0"]].text = payload.titre_presentation
    #slide.placeholders[dico["1"]].insert_picture(payload.logo_client)
    slide.placeholders[dico["4"]].insert_picture(str(image1))
    slide.placeholders[dico["3"]].text = payload.nom_projet
    slide.placeholders[dico["2"]].text = payload.nom_fichier

    #AJout Slide Présentation TAME
    slide=prs.slides.add_slide(prs.slide_layouts.get_by_name("2_Introduction"))
    slide=prs.slides.add_slide(prs.slide_layouts.get_by_name("3_Introduction"))
    slide=prs.slides.add_slide(prs.slide_layouts.get_by_name("4_Introduction"))

    #Ajout Transition
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Transition"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx
    slide.placeholders[dico["0"]].text ="Besoin"
    slide.placeholders[dico["1"]].insert_picture(str(image2))

    #Ajout Besoin
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Besoin"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx

    Ajouter_texte(slide.placeholders[dico["2"]],payload.Besoin.Avancement)
    Ajouter_texte(slide.placeholders[dico["3"]],payload.Besoin.Besoin)
    Ajouter_texte(slide.placeholders[dico["0"]],payload.Besoin.Role_TAME)
    slide.placeholders[dico["1"]].insert_picture(str(image4))
    # slide.placeholders[dico["0"]].text_frame.paragraphs[0].text = payload.Besoin.Avancement
    
    # slide.placeholders[dico["1"]].text_frame.paragraphs[0].text = payload.Besoin.Besoin
    # slide.placeholders[dico["2"]].text_frame.paragraphs[0].text = payload.Besoin.Role_TAME

    #Ajout Données d'entrée
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Entrees"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx
    slide.placeholders[dico["0"]].text = "Données d'entrée"
    Ajouter_texte(slide.placeholders[dico["1"]], payload.donnees_entree)
    slide.placeholders[dico["2"]].insert_picture(str(image5))
    #Ajout les hypothèses
    for hyp in payload.hypotheses:
        slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("1_Hypotheses"))
        dico={}
        for index,placeholder in enumerate(slide.placeholders):
            dico[f"{index}"] = placeholder.placeholder_format.idx
        slide.placeholders[dico["0"]].text = hyp.Type_Hypothese
        Ajouter_texte(slide.placeholders[dico["1"]], hyp.List_Hypotheses,nb_colonnes=2)
        slide.placeholders[dico["2"]].insert_picture(str(image5))

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
            Ajouter_texte(slide.placeholders[dico["3"]], lot.details_lot)
            slide.placeholders[dico["0"]].text = lot.nom
            image_path = resolve_asset_path(lot.image_lot)
            slide.shapes.add_picture(image_path,slide.placeholders[dico["4"]].left,slide.placeholders[dico["4"]].top,slide.placeholders[dico["4"]].width*0.85,slide.placeholders[dico["4"]].height*0.85)
            slide.placeholders[dico["4"]].element.getparent().remove(slide.placeholders[dico["4"]].element)
            dessiner_documents_lot(slide,slide.placeholders[dico["2"]],lot.documents)
            slide.placeholders[dico["1"]].insert_picture(str(image6))

    #Ajout Transition
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Transition"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx
    slide.placeholders[dico["0"]].text ="Synthèse"
    slide.placeholders[dico["1"]].insert_picture(str(image3))

    #Ajout Synthèse
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Synthese_finance"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx
    slide.placeholders[dico["1"]].text = "Synthèse"
    dessiner_tableau_dynamique(slide,slide.placeholders[dico["0"]],payload.lots_list)

    #Ajout du Planning
    if payload.id_semaine_debut :
        debut_gantt_init= payload.id_semaine_debut
        largeur=largeur_libelles(payload.lots_list.lots)
        #TRi des lots par phase
        tri_lots_phases = {}
        for lot in payload.lots_list.lots:
            if not tri_lots_phases.get(lot.phase,{}):
                tri_lots_phases[lot.phase]={"lots":[lot],"nb_semaines":lot.duree+lot.debut,"debut":lot.debut}
            else:
                tri_lots_phases[lot.phase]["lots"].append(lot) 
                tri_lots_phases[lot.phase]["nb_semaines"] =lot.duree +lot.debut
        #Création d"une slide planning par phase
        
        for nom_phase,liste_lot in tri_lots_phases.items():

            ajouter_gantt(
                    annee = payload.Annee,
                    prs = prs,
                    layout=prs.slide_layouts.get_by_name("Planning"),
                    title = f"Planning - {nom_phase}",
                    lots=liste_lot["lots"],
                    nombre_semaines_tot=liste_lot["debut"],
                    nombre_semaines_phase=liste_lot["nb_semaines"]-liste_lot["debut"],
                    debut_gantt=debut_gantt_init,
                    largeur_libelles=largeur
            )


    #Ajout Transition
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Transition"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
        dico[f"{index}"] = placeholder.placeholder_format.idx
    slide.placeholders[dico["0"]].text ="Annexes"
    slide.placeholders[dico["1"]].insert_picture(str(image2))

    #Ajout propriété intellectuelles
    slide = prs.slides.add_slide(prs.slide_layouts.get_by_name("Prop_int"))
    dico={}
    for index,placeholder in enumerate(slide.placeholders):
            dico[f"{index}"] = placeholder.placeholder_format.idx  
    slide.placeholders[dico["1"]].text = "PROPRIETE INTELLECTUELLE"

    text =f"""Domaine de l'offre
\tLe DOMAINE couvert par cette offre est « [COMPLETER] ».
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
    prs.save(out)


if __name__=="__main__":
    main()