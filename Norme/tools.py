from docling.datamodel.pipeline_options import (PdfPipelineOptions,HeadingHierarchyOptions)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
import re
from pathlib import Path
import time

def Create_md_modeles_docling(name,source):
    #Paramètres modèles
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.enable_remote_services= False
    pipeline_options.artifacts_path = Path("./docling_models")
    pipeline_options.do_table_structure = True
    pipeline_options.do_chart_extraction = False
    pipeline_options.heading_hierarchy_options = HeadingHierarchyOptions(enabled=True,use_bookmarks=True)
    #fichier markdown
    global_doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options
            )
        }
    )
    result = global_doc_converter.convert(source)
    result.document.save_as_markdown(f"./Ressources/md/{name}.md")


def get_sommainre(name:str,chemin_md:str):
    fichier= Path(chemin_md)
    if not fichier.exists():
        return f"Erreur : le fichier {chemin_md} n'existe pas"
    sommaire=[]
    pattern_titre = re.compile(r'^(#{1,6})\s+(.+)$')
    with open(fichier,"r",encoding="utf-8") as f:
        for num_ligne,ligne in enumerate(f,start=1):
            ligne_propre = ligne.strip()
            match= pattern_titre.match(ligne_propre)
            if match :
                titre = match.group(2)
                niveau = len(match.group(1))
                indentation = "  " * (niveau - 1)
                sommaire.append(f"{indentation}- {titre} (Ligne {num_ligne})") #
        if not sommaire:
            return "Aucun titre (balise #) n'a été trouvé dans ce document."

    with open(Path(f"./Ressources/sommaire/{name}.txt"),"w",encoding="utf-8") as som:
        som.write("\n".join(sommaire))





# debut = time.time()
# # Create_md_modeles_docling("NF_EN_60601-1-2_12",Path("./Ressources/NF EN 60601-1-2_12 2016_Appareils électromédicaux_sécurité performances_perturbations éléctromagnétiques.pdf"))
# fin = time.time()

# print(f"temps total export (secondes) = {round(fin-debut)}")

# debut = time.time()
# get_sommainre("NF_EN_60601-1-2_12","./Ressources/md/NF_EN_60601-1-2_12.md")
# fin = time.time()

# print(f"temps total sommaire (secondes) = {round(fin-debut)}")


def creat_db():
    pass