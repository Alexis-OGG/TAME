
from ..tools.db_utils import get_champs,SUB_CATEGORIES
import concurrent.futures
from .Offre import Offre
from .AI import Agent_AI
from .RAG import Embeddings
from ..tools.API_Distrib import *
import re
from docling.datamodel.pipeline_options import (PdfPipelineOptions,HeadingHierarchyOptions)
from docling.document_converter import DocumentConverter, PdfFormatOption,HttpSource
from docling.datamodel.base_models import InputFormat
# from docling_core.types.doc.document import ImageRefMode
# from docling.chunking import HybridChunker

from seleniumbase import SB
# from selenium.webdriver.chrome.options import Options

from pathlib import Path
import requests
from pydantic import BaseModel
import time
import os 


OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"assets")

class Classifier(BaseModel):
    cateogry:str
    sub_category:str

class Component:


    def __init__(self,
                 mpn,
                 Temp_fonc="",
                 Description="",
                 Temp_stock="",
                 humidity="",
                 Floor_life="",
                 Rohs="",
                 Reach="",
                 boitier="",
                 Dimensions="",
                 fabricant="",
                 status="Unknown",
                 status_details="",
                 datasheet="",
                 category:tuple[str]=("Unknown","Unknown"),):
        #Variables modifiables
        self.mpn=mpn
        if datasheet.startswith("//"):
                    datasheet = "https:" + datasheet
        self.Fiche_Technique=datasheet
        self.Temp_fonc = Temp_fonc
        self.Description=Description
        self.Temp_stock=Temp_stock
        self.humidity=humidity
        self.Floor_life=Floor_life
        self.Rohs=Rohs
        self.Reach=Reach
        self.boitier=boitier
        self.Dimensions=Dimensions
        self.Fabricant=fabricant
        self.status=status
        self.Details_Distributeurs=status_details
        self.category=category

        self.offres=[] #Liste offre associé aux mpn entières

        #Variables IA
        self.md_datasheet=None
        self.champs={}
        # self.donnees_extraites = {}
        # self.liste_noms_champs_attendus=[]
     
    def __Create_md_modeles_docling(self,url):
        # Convertion en markdown de la datasheet
        debut_md = time.time()
        print("# Datasheet Conversion ...")
        #Paramètres modèles
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.enable_remote_services= False
        pipeline_options.artifacts_path = Path("C:/Users/alexis.auger/Documents/docling_models")
        pipeline_options.do_table_structure = True
        pipeline_options.do_chart_extraction = False
        pipeline_options.do_picture_description= False
        pipeline_options.generate_picture_images = False

        # chart_opts = ChartExtractionVlmEngineOptions.from_preset("granite_vision_v3_3")
        # chart_opts.engine_options.model_id = "ibm-granite/granite-vision-3.3-2b"
        # pipeline_options.chart_extraction_options = chart_opts
        # pipeline_options.picture_description_options = (
        #     granite_picture_description  
        # )
        # pipeline_options.picture_description_options.prompt = (
        #     "Describe the image in three sentences. Be consise and accurate on numbers."
        # )
        # pipeline_options.heading_hierarchy_options = HeadingHierarchyOptions(enabled=True,use_bookmarks=True)
        #fichier markdown
        global_doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options
                )
            }
        )
        try : 
            result = global_doc_converter.convert(HttpSource(url=url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36 Edg/156.0.0.0"}))
            result.document.save_as_markdown(os.path.join(OUT_DIR,"sortie.md"))
            self.md_datasheet=result.document
        except:
            # Contournement avec selelium
            with SB(uc=True, headless=True,external_pdf=True) as sb:
                dl_dir = Path(sb.get_downloads_folder())
                before = os.listdir(dl_dir)
                sb.goto(url)
                sb.sleep(3)
                
                new = [p for p in os.listdir(dl_dir) if p not in before]
                print(new)
                if new==[] : 
                     return {"Status":"Failed","content":"Aucun pdf trouvé"}
                file_pdf=os.path.join(dl_dir,new[0])
                result = global_doc_converter.convert(file_pdf)
                os.remove(file_pdf)
                self.md_datasheet=result.document 
        fin_md = time.time()
        print(f"# Datasheet Conversion Complete ({round(fin_md-debut_md)} secs)")
        return {"Status":"Success"}

    
        # sortie = os.path.join((os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"assets","md","Test_V2.md")
        # output_dir =os.path.join((os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),"assets","md")
        # image_counter = 1
        # for item, _ in result.document.iterate_items():

        #     if item.label in ["picture", "figure", "image"]:
        #         if getattr(item, "image", None) is not None and getattr(item.image, "pil_image", None) is not None:
        #             # Nom du fichier : image_1.png, image_2.png...
        #             img_filename = f"image_{image_counter}.png"
        #             img_path = os.path.join(output_dir ,img_filename)
                    
        #             # Sauvegarde sur le disque
        #             item.image.pil_image.save(img_path)
                    
        #             # IMPORTANT : On dit à Docling que l'URI de cette image est notre chemin local
        #             item.image.uri = str(img_path)
        #             image_counter += 1

        # # 5. EXPORT DU MARKDOWN AVEC LES LIENS VERS VOS IMAGES
        # # Le paramètre REFERENCED force Docling à écrire ![picture](datasheet_images/image_1.png) dans le MD
        # # md_text = result.document.export_to_markdown(image_mode=ImageRefMode.REFERENCED)
        
        
        # # result.document.save_as_markdown(sortie,image_mode=ImageRefMode.REFERENCED)
        # markdown = result.document.export_to_markdown(image_mode=ImageRefMode.REFERENCED)

    def update(self, **kwargs):
        for cle, valeur in kwargs.items():
            if hasattr(self, cle):
                if cle=="Fiche_Technique" and valeur.startswith("//"):
                    valeur = "https:" + valeur
                setattr(self, cle, valeur)
            else:
                print(f"L'attribut '{cle}' n'existe pas dans cette classe.")

    def find_category(self):
        if self.Description=="":
            return {"Status":"Failed","content":"Aucune Description du composant, à ajouter manuellement"}
        else:
            format = Classifier.model_json_schema()
            prompt = f"""You are a components classifier agent. Answer the question with the context.
                    CONTEXT :
                    Description (french or english) : {self.Description} 
                    Available categories and sub-category : {SUB_CATEGORIES}
                    QUESTION : What is the category and the sub-category ? 
                    RESPONSE :"""
            agent =Agent_AI(model="qwen3.5:4b",format=format)
            agent.add_messages(content=prompt)
            try :
                first = Classifier.model_validate_json(agent.query_stream(think=False))
                self.category=(first.cateogry,first.sub_category)
                return {"Status":"Success","content":f"Catégorie attribuée [{self.mpn}] : {self.category}"}
            except:
                return {"Status":"Failed","content":f"Catégorie no attribuée"}

    def fill_champs_category(self):
            champs = get_champs(self.category[0],self.category[1])
            #1ère Guardrail : Vérification des inputs
            print("==============GUARDRAILS n°1 : INPUTS EXISTENCE==============")
            if isinstance(champs,str):
                print("STATE : Failed")
                return{"Status":"Failed","content": f" Erreur : Champs non trouvés. La catégorie du composant n'est pas présent dans la base de données TAME."}
            if self.Fiche_Technique=="":
                print("STATE : Failed")
                return{"Status":"Failed","content": f" Erreur : Datasheet non trouvée. Mettre à jour le composant pour ajouter la datasheet."}
            print("STATE : Success")

            #Vérification 
            if self.md_datasheet == None:
                response = self.__Create_md_modeles_docling(self.Fiche_Technique)
                if response["Status"]=="Failed":
                    return{"Status":"Failed","content": f" Erreur : Accès à la datasheet non autorisé"}
            

            data = Embeddings()
            data.index_document(doc_id=self.mpn,text=self.md_datasheet)
            # sections = self.__get_list_section()
            # for section in sections:
            #     data.index_document(doc_id=section["infos"],text=section['text'])
            # data.index_document(doc_id=self.mpn,text=self.md_datasheet)
            for champ in champs:
                self.champs[champ["index"]] = (champ["name"],data.rag_query(f"{champ["description"]} ({champ["keywords"]})"))
            return{"Status":"Success","content": f"Remplissage des champs complets. Vérifier que tous les champs sont bien complétés"}
    
    def analyse_mpn(self,token_digykey,Actif=True,Rohs=True,Type_Research=False):
                results = {}
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    future_dk = executor.submit(query_digikey, self.mpn,token_digykey,Actif,Rohs,Type_Research)
                    future_ms = executor.submit(query_mouser, self.mpn,Actif,Rohs,Type_Research)
                    future_fn = executor.submit(query_farnell, self.mpn,Actif,Rohs,Type_Research)
                    future_fu = executor.submit(query_future_electronics, self.mpn,Actif,Rohs,Type_Research)
                    
                    #Attente des API
                    results["DigiKey"] = future_dk.result()
                    results["Mouser"] = future_ms.result()
                    results["Farnell"] = future_fn.result()
                    results["Future_Electronics"] = future_fu.result()
        
                valid_results = {dist: data for dist, data in results.items() if data and "Erreur" not in data}
                if not valid_results:
                    erreurs = {
                    distributeur: valeur.get("Erreur", "Réponse vide")
                    if isinstance(valeur, dict)
                    else "Réponse vide"
                    for distributeur, valeur in results.items()
                    }
            
                    return {
                        "Status": "Failed", "content" :f"Aucun distributeur n'a retourné de résultat valide : {erreurs}",
                    }
                # Regroupement de toutes les offres
                toutes_offres = []
                toutes_alternatives = set()
                for data in valid_results.values():
                    toutes_offres.extend(data.get("offres", []))
                    for alt in data.get("alternatives", []):
                                if alt:
                                    toutes_alternatives.add(alt)
                # for comp in list(toutes_alternatives):
                #     self.equivalent.append(Demande(comp))
                first_offer=False
                for offre in toutes_offres:
                    chargement = ""
    
                    ref_dist = re.sub(r'[:;$@}{#¤£&"|`^=+§*_]',"",offre["REF"])
                    fabricant = chargement if offre["fabricant"]==""else offre["fabricant"]
                    datasheet=chargement if offre["datasheet"]==""else offre["datasheet"]
                    status=normalize_status(offre["status"])
                    Temp_fonc = chargement if offre["Temp_fonc"]=="" else offre["Temp_fonc"]
                    Description = chargement if offre["Description"]=="" else offre["Description"]
                    Temp_Stock = chargement if offre["Temp_stock"]=="" else offre["Temp_stock"]
                    humidity = chargement if offre["humidity"]=="" else offre["humidity"]
                    Floor_life = chargement if offre["Floor_life"]=="" else offre["Floor_life"]
                    Rohs = chargement if offre["Rohs"]=="" else offre["Rohs"]
                    Reach = chargement if offre["Reach"]=="" or "Non" in offre["Reach"] else offre["Reach"]
                    boitier = chargement if offre["boitier"]=="" else offre["boitier"]
                    Dimensions = chargement if offre["Dimensions"]=="" else offre["Dimensions"]
                    
                    
                    if first_offer :
                        if status==("Obsolète" or "Non Recommandé") or self.status == "Autre" : self.status = status
                        if self.Fabricant==chargement: self.Fabricant = fabricant
                        if self.Fiche_Technique==chargement: self.Fiche_Technique = datasheet
                        if self.Temp_fonc==chargement: self.Temp_fonc = Temp_fonc
                        if self.Description==chargement: self.Description = Description
                        if self.Temp_stock==chargement:self.Temp_stock=Temp_Stock
                        if self.humidity==chargement:self.humidity=humidity
                        if self.Rohs==chargement:self.Rohs=Rohs
                        if self.Reach==chargement:self.Reach=Reach
                        if self.boitier==chargement: self.boitier=boitier
                        if self.Dimensions==chargement: self.Dimensions=Dimensions
                        if self.Floor_life==chargement: self.Floor_life=Floor_life
                    else:

                        self.update(mpn=ref_dist,Temp_fonc=Temp_fonc,Description=Description,Temp_stock=Temp_Stock,humidity=humidity,Floor_life=Floor_life,Rohs=Rohs,Reach=Reach,boitier=boitier,Dimensions=Dimensions,Fabricant=fabricant,Fiche_Technique=datasheet,status=status)
                        first_offer=True
        
                    packages = offre["Package"]
                    for pkg in packages:
                        self.offres.append(Offre(Distributeur= pkg["Distributeur"],Conditionnement= pkg["Conditionnement"],Stock= pkg["Stock_Disponible"],Prix_Unitaire= (" ".join([f"{p['Prix_Unitaire']} € (< {p['Quantite'] })" for p in pkg["Prix"]]) if pkg["Prix"] else "N/A") ,MOQ= pkg["MOQ"]))
                return {"Status": "Success"}
    
    def __str__(self):
        texte = f"""
            === COMPOSANT  ===
            MPN : {self.mpn}
            Status : {self.status}
            Description : {self.Description} 
            Fabricant : {self.Fabricant}
            Etat : {self.status}
            Datasheet : {self.Fiche_Technique}
            Category : {self.category}
            champs : {self.champs}
            == Techniques ==
            Dimension : {self.Dimensions}
            Boîtier : {self.boitier}
            Reach : {self.Reach}
            Rohs : {self.Rohs}
            Durée vie Stockage : {self.Floor_life}
            Humidité Stockage : {self.humidity}
            Température de Fonctionnement : {self.Temp_fonc}
            Température de Stockage : {self.Temp_stock}
        """
        for offre in self.offres:
            texte += offre.__str__()
        return(texte)


if __name__ =="__main__":
    debut = time.time()
    Composant = Component(mpn="M24M02-DWMN3TP/K")
    # Composant.update(category=("CIRCUITS_INTEGRES","CI_MEMOIRE"),Fiche_Technique="http://www.phoenixcontact.com/us/products/1115661/pdf")
    Composant.update(category=("PIEZO","BUZZER"),Fiche_Technique="https://www.sameskydevices.com/product/resource/css-73b16k-smt-tr.pdf")
    print(Composant.fill_champs_category())
    fin = time.time()
    print(f"Temps Query : {round(fin-debut)} s")


