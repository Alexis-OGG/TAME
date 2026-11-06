from ollama import chat,generate,embeddings,show
from pydantic import BaseModel
import time
from ..db_utils import *
from typesafe_sdk import Choice, TypeSafeClient

import joblib

def obtenir_limite_contexte(nom_modele: str)->int|None:
    infos = show(nom_modele)
    
    # Ollama stocke cette info dans 'model_info' sous un nom qui dépend de l'architecture 
    # (ex: 'qwen2.context_length', 'llama.context_length')
    for cle, valeur in infos.get('model_info', {}).items():
        if 'context_length' in cle:
            return valeur
            
    return None

# -------------------------------------------------
#                   FIND COLUMN
# -------------------------------------------------
class Ref(BaseModel):
  sheet: str
  column: str
  line: int

def AI_query(message,model):
  messages = [{'role': 'user', 'content': message}]
  while True:
    response  = chat(
      model=model,
      # model='gemma3:1b',
      messages=messages,
      format=Ref.model_json_schema(),
      options= {
        "temperature": 0,
        'num_predict': 80
      },
      think=False,
    )
    print(response.message.content)
    column = Ref.model_validate_json(response.message.content)
    return column


# -------------------------------------------------
#                   FIND Category
# -------------------------------------------------
class Category(BaseModel):
  category: str

def AI_query_category_V2(description_mpn):
    state = {
      "request": f"Categorize a component :  {description_mpn} ",
    }
    questions = {
    "category": Choice(
        instructions=f"which component category ?",
        criteria=get_list_categories())
    }

    with TypeSafeClient(timeout=120) as client:
      result = client.system_one(state=state, questions=questions,model='tev1:0.8b')

    choix = result.choices["category"].choice      # the chosen category
  
    state = {
      "request": f"Categorize a component :  {description_mpn} ",
    }
    questions = {
    "category": Choice(
        instructions=f"Component  {description_mpn} : which Subcategory ?",
        criteria=get_list_subcategories(choix))
    }
    
    with TypeSafeClient(timeout=120) as client:
      result = client.system_one(state=state, questions=questions,model='tev1:4b')

    choix1 = result.choices["category"].choice

    # model = joblib.load("component_classifier.joblib")
    # prediction = model.predict([description_mpn])[0]
    return {"Status": "Success", "content" : (choix,choix1),"final":choix1}


def AI_query_category(description_mpn):
    state = {
      "request": f"Categorize a component :  {description_mpn} ",
    }
    questions = {
    "category": Choice(
        instructions=f"which component category ?",
        criteria=get_list_categories())
    }

    with TypeSafeClient(timeout=120) as client:
      result = client.system_one(state=state, questions=questions)

    choix = result.choices["category"].choice      # the chosen category
  
    state = {
      "request": f"Categorize a component :  {description_mpn} ",
    }
    questions = {
    "category": Choice(
        instructions=f"Component  {description_mpn} : which Subcategory ?",
        criteria=get_list_subcategories(choix))
    }
    
    with TypeSafeClient(timeout=120) as client:
      result = client.system_one(state=state, questions=questions)

    choix1 = result.choices["category"].choice

    # model = joblib.load("component_classifier.joblib")
    # prediction = model.predict([description_mpn])[0]
    return {"Status": "Success", "content" : f"{choix} -> {choix1}","final":choix1}


# -------------------------------------------------
#                   FIND MPN
# -------------------------------------------------

class MPN(BaseModel):
  mpn: list[str]

def AI_query_mpn(line:str,model:str):
  message= f"""You are an expert in electronic components. 
Analyze the following text and extract the Manufacturer Part Numbers (MPN). 
- If you find an MPN(s), return ONLY the MPN(s). 
- If no valid MPN is found, return the clean short component description.
- If no valid MPN and no valid description are found, return NOT_FOUND
Text: {line}"""
  
  messages = [{'role': 'system', 'content': 'You are a strict data extraction assistant. You output only the MPN or the description, nothing else.'},{'role': 'user', 'content': message}]
  response  = chat(
    model=model,
    # model='gemma3:1b',
    messages=messages,
    format=MPN.model_json_schema(),
    options= {
      "temperature": 0,
    },
    think=False,

  )

  column = MPN.model_validate_json(response.message.content)
  return column.mpn


if __name__=="__main__":
  
    debut = time.time()
    

   

    descriptions = [
    "RES SMD 100K OHM 1% 1/10W 0603",
    "POTENTIOMETRE 10K OHM AJUSTABLE 3 TOURS",
    "THERMISTANCE NTC 10K 1% 3950K",
    "COND CERAMIQUE 100NF 50V X7R 0603",
    "COND TANTALE 47UF 16V 10% SMD",
    "COND ALU 220UF 35V RADIAL",
    "DIODE SCHOTTKY 40V 1A SOD123",
    "DIODE ZENER 5V1 500MW SMD",
    "DIODE TVS 24V BIDIRECTIONNELLE SMB",
    "SELF DE PUISSANCE 10UH 3A SMD",
    "FERRITE BEAD 600 OHM 100MHZ 0805",
    "TRANSFO ETHERNET 1 PORT 10/100 BASE-T",
    "ALIMENTATION AC/DC 230VAC 24VDC 60W",
    "CHARGEUR BATTERIE LI-ION 1 CELL 1A",
    "REGULATEUR LDO 3V3 500MA SOT23-5",
    "MCU ARM CORTEX-M4 32BIT 512KB FLASH",
    "EEPROM I2C 256KBIT SOIC8",
    "DRIVER MOTEUR DC DOUBLE PONT H 1.2A",
    "MOSFET N CHANNEL 60V 5A SOT223",
    "TRANSISTOR NPN 40V 600MA SOT23",
    "CONNECTEUR USB TYPE C FEMELLE CMS 16P",
    "BORNIER A VIS 3 POSITIONS PAS 5.08MM",
    "BOITIER ABS IP65 120X80X55MM",
    "VENTILATEUR 24VDC 40X40X10MM",
    "BOUTON POUSSOIR MOMENTANE NO ROUGE",
    "RELAIS 12VDC SPDT 10A 250VAC",
    "BATTERIE LI-ION 3.7V 2600MAH",
    "CABLE USB A VERS USB C 1M NOIR",
    "OPTOCOUPLEUR 5KV DIP4",
    "CAPTEUR DE COURANT HALL 20A ANALOGIQUE"
]
    categories = [
      "RES",
      "POT",
      "THERMISTANCE",
      "COND_CERAM",
      "COND_TANT",
      "COND_ALUM",
      "DIODE_SCHOTTKY",
      "DIODE_ZENER",
      "DIODE_TRANSIL",
      "SELF_MODE_COMMUN",
      "FERRITES",
      "TRANSFO_ETHERNET",
      "ALIM",
      "CHARGEUR",
      "CI_REGUL",
      "CI_MICRO",
      "CI_MEMOIRE",
      "CI_DRIVER",
      "TRANSISTOR_MOS",
      "TRANSISTOR_BIP",
      "CONNECT_USB",
      "BORNIER",
      "BOITIER",
      "VENTILATEUR",
      "BOUTON_POUSSOIR",
      "RELAIS",
      "BATTERIE",
      "CABLE",
      "OPTOCOUPLEUR",
      "CAPTEUR_COURANT"
    ]



    
    
    taille=len(descriptions)
    nb_true = 0
    for index,desc in enumerate(descriptions):
       response= AI_query_category_V2(desc)
       if response["Status"]=="Success":
          if response["final"]==categories[index]:
             nb_true+=1
          print(f"INFOS : {categories[index]} | {response["content"]} " )
          print(f"{index+1}/{taille} : {response["final"]==categories[index]}")
          
    print("----------")
    print(f"TOTAL : {nb_true}/{taille}")
    print("----------")



    fin = time.time()

    print(f"Temps Query : {round(fin-debut)} s")