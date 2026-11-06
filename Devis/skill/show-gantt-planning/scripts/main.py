
#Import modules
from classes import *

from generate_gantt import ajouter_gantt,largeur_libelles
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

    #Source du Template
    SCRIPT_DIR = Path(__file__).resolve().parent
    SKILL_DIR = SCRIPT_DIR.parent

    template_path = SKILL_DIR / "assets" / "DEV_Template.pptx"

    prs = Presentation(template_path)


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

    #Sauvegarde
    prs.save(out)


if __name__=="__main__":
    main()