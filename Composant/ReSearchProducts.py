#Modules Outils
from tools.build_liste_comp import analyse_liste
from tools.export_excel import exporter_excel
from tools.classlist import ResultAllProduct,ErreurMsg
from ressources.create_ressources import ComponentType,FamilyType

#Librairies
from dotenv import load_dotenv
from sqlalchemy import select,create_engine
from sqlalchemy.orm import Session,aliased

from docling.datamodel.pipeline_options import (PdfPipelineOptions)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from pathlib import Path
import os
from curl_cffi import requests

from mcp.server import MCPServer
from typing import Annotated
from pydantic import Field


mcp = MCPServer("BOM_Tools")
load_dotenv()
import os

global_doc_converter = None

def charger_modeles_docling():
    global global_doc_converter
    if global_doc_converter is None:
      pipeline_options = PdfPipelineOptions()
      pipeline_options.do_ocr = False
      pipeline_options.artifacts_path = Path("./docling_models")
      pipeline_options.do_table_structure = True
      
      global_doc_converter = DocumentConverter(
          format_options={
              InputFormat.PDF: PdfFormatOption(
                  pipeline_options=pipeline_options
              )
          }
      )
    return global_doc_converter
@mcp.tool(
  name="Analyse_BOM",
  title="Analyseur de BOM",
  description="Analyse une liste de composants et renvoie les informations importantes: disponibilité, aspects techniques, prix, normes,",
  structured_output=True,
    
)
def Analyse_BOM(
  liste :Annotated[list[str],Field(description="""Liste de composants; Exemlple : ["3039","CR2477N","C0603C103K4RACTU"]""")]
  )-> dict[str,ResultAllProduct]|ErreurMsg:
  try:
    resultats = analyse_liste(liste,True,True)
    
    return resultats
  except Exception as e:
    return ErreurMsg(erreur_message= f"Analyse de BOM échoué : {e}")

@mcp.tool(
  name= "Read_page_Datasheet",
  title = "Lire Page datasheet",
  description="Lire une page d'une datasheet d'un composant à partir de l'url de la fich technique et du numéro de la page à lire."
)
def lire_datasheet(reference:str,url:str,numero_page:int):
  pdf_filepath=f"files/{reference}.pdf"
  if not(os.path.isfile(pdf_filepath)):
    try : 
      response = requests.get(url, impersonate="chrome110", timeout=15)
      if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "")
    
        if "application/pdf" in content_type.lower() or "application/octet-stream" in content_type.lower():
              with open(pdf_filepath, "wb") as file:
                  file.write(response.content)
        else:
                  return f"Erreur : Le pare-feu bloque toujours. Type reçu : {content_type[:50]}..."
      else:
          return f"Erreur lors du téléchargement du fichier : Code HTTP {response.status_code}"
    except Exception as e:
          return f"Erreur lors du téléchargement du fichier : {str(e)}"
  try:
      result = charger_modeles_docling().convert(pdf_filepath,page_range=(numero_page, numero_page))
      markdown_text = result.document.export_to_markdown()
      return markdown_text
  except Exception as e:
      return f"Erreur lors de la lecture du fichier PDF : {str(e)}"

@mcp.resource("users://list/{family}/{sub_family}")
def get_champs_sub_family(family: str,sub_family:str) -> str:
  engine = create_engine("sqlite:///Components_db")
  session = Session(engine)
  
  #Case sub_family
  family_alias = aliased(FamilyType)
  stmt = select(ComponentType.champs1,ComponentType.champs2,ComponentType.champs3,ComponentType.champs4,ComponentType.champs5,ComponentType.champs6,ComponentType.champs7,ComponentType.champs8,ComponentType.champs9,ComponentType.champs10).join(family_alias,ComponentType.family_id == family_alias.id).where(family_alias.name == family).where(ComponentType.name == sub_family)
  query= session.execute(stmt).one()
  if query!=[]:
    response = ""
    for i in range(10):
        response += f"Champs{i+1} = {getattr(query,f"champs{i+1}")}\n"
    return response
  else :
      return f"Mauvais Arguments"
      
@mcp.resource("users://list/{family}")
def get_sub_families(family: str) -> str:
  engine = create_engine("sqlite:///Components_db")
  session = Session(engine)
  #Case sub_families
  if family :
    family_alias = aliased(FamilyType)
    stmt = select(ComponentType.name).join(family_alias,ComponentType.family_id == family_alias.id).where(family_alias.name == family)
    query= session.execute(stmt).all()
    response = ""
    for item in query:
        response += f"{item.name}\n"
    return(response)
  else :
    return "Mauvais Arguments"

@mcp.resource("users://list}")
def get_families() -> str:
  engine = create_engine("sqlite:///Components_db")
  session = Session(engine)
  stmt = select(FamilyType.name)
  query= session.execute(stmt).all()
  response = ""
  for item in query:
    response += f"{item.name}\n"
  return(response)

@mcp.tool(
    name="Export_data",
    title="Exportez Analyse BOM",
    description="Export au foramt excel l'analyse de la BOM",
  )
def export_data_BOM(analyse:dict[str,ResultAllProduct]):
  return exporter_excel(analyse)














#     test =  Analyse_BOM([
#   "CR2477N",
#   "C0603C103K4RACTU"
# ])
#     print(json.dumps(test, indent=2, ensure_ascii=False))
    # print(test)
    #     bruh = exporter_excel({PIC32CM6408PL10028-E/SS 
    # test = query_digikey_sub("BAS116T,115",get_digikey_token())
    
    # url ="https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8942/490_Chip_Multilayer_CAT2021_MLCC.pdf" 
    

    # test1=query_farnell("Capacitor 22uF 10V 0805",True,True,True)
    # test1=analyse_liste(["GRM21BR61A226ME51"],False,False)
    # test1=query_farnell("GRM21BR61A226ME51",False,False,False)

    # print(json.dumps(test1, indent=2, ensure_ascii=False))
    # result = analyse_liste([  "GRM21BR61A226ME51"])
    # liste1 = [
    #   "3039",
    #   "CR2477N",
    #   "C0603C103K4RACTU",
    #   "06033C104KAT2A",
    #   "GRM32ER71A476KE15L",
    #   "GRM32ER71A476KE15L",
    #   "BAS116T,115",
    #   "BAS116TT1G",
    #   "SMT-1324-TW-1V-R",
    #   "SDR08540M3-01",
    #   "MMBT3906LT1G",
    #   "MMBT3904LT1G",
    #   "IRLML2502TRPBF",
    #   "CRCW0603470RFKEA",
    #   "CRCW0603100KFKEA",
    #   "CRCW0603470KFKEA",
    #   "CRCW06031K00FKEA",
    #   "CRCW060320K0FKEA",
    #   "RC0603FR-0720KL",
    #   "CRCW0603330RJNEA",
    #   "CRCW060330K0FKEA",
    #   "CRCW06030000Z0EA",
    #   "CRCW06030000Z0EA",
    #   "CRCW0603560KFKEA",
    #   "CRCW060320K0FKEA",
    #   "RC0603FR-0720KL",
    #   "SKRNPME010",
    #   "RFD21733",
    #   "MAX6778XK+",
    #   "1355PCB001 IND 02",
    #   "1355C1001 IND 02",
    #   "PAN 511 REMO 019 IND 00",
    #   "1355ET001 IND 02",
    #   "BRADY THT-38-727-10",
    #   "BRADY R-6002",
    #   "1355ET002 IND 01",
    #   "BRADY THT-38-727-10",
    #   "BRADY R-6002"
    # ]
    #     liste2=[
    #   "C0603C103K4RACTU",
    #   "06033C104KAT2A",
    #   "C1210C476M4PACTU",
    #   "C1210C476M4PACTU",
    #   "HSMD-C190",
    #   "SMBJ5.0CA",
    #   "HSMG-C190",
    #   "5749767-1",
    #   "5206052-3",
    #   "MMBT3904LT1G",
    #   "MMBT3906LT1G",
    #   "CRCW06032OKOFKEA",
    #   "RC0603FR-0720KL",
    #   "CRCW06032OKOFKEA",
    #   "RC0603FR-0720KL",
    #   "CRCW0603110RFKEA",
    #   "CRCW0603470RFKEA",
    #   "RC0603FR-0747KL",
    #   "CRCW060347K0FKEA",
    #   "RC0603FR-07330RL",
    #   "CRCW06030000Z0EA",
    #   "CRCW06030000Z0EA",
    #   "CRG1206ZR",
    #   "7914J-1-000E",
    #   "RFD21733",
    #   "MC74HC03ADG",
    #   "1357PCB001 IND 02",
    #   "1357C1001 IND 02",
    #   "PAN 511 INTE 020 IND 00",
    #   "1357ET001 IND 02",
    #   "BRADY THT-1-719-10",
    #   "BRADY R-6002"
    # ]
    #     resultats = analyse_liste(liste2,True,True)
    #resultats = analyse_liste(get_excel_column_data(file_path="./1357LC001_02.xlsx",column_name=),True,True)







