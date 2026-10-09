
from sqlalchemy import create_engine,select,delete
from sqlalchemy.orm import Session
from Ressources.create_db import Input_X
from Tools.Classe import ProjectComplexity
import json
engine = create_engine("sqlite:///Ressources/Project_db")
session = Session(engine)

def search_project(ref:str):
     try:
          query = select(Input_X).where(Input_X.project_name==ref)
          result = session.execute(query)
          project = result.one()[0]
          print("==INPUT==")
          print(json.dumps(project.__input__(),ensure_ascii=False,indent=2))
          print("==OUTPUT==")
          print(json.dumps(project.__output__(),ensure_ascii=False,indent=2))
     except :
          print("Projet Non trouvé")

def list_project():
     query = select(Input_X.id,Input_X.project_name)
     result = session.execute(query)
     projects = result.all()
     for project in projects:
          print(f"id= {project.id} \t Ref= {project.project_name}")

def add_project(data:ProjectComplexity,liste):
     try:
          item = Input_X(
          project_name = data.reference_project,
          classe_DM= data.classe_DM,
          criticite_patient= data.criticite_patient,
          complexite_mecanique= data.complexite_mecanique,
          complexite_electronique= data.complexite_electronique,
          complexite_logicielle= data.complexite_logicielle,
          complexite_integration= data.complexite_integration,
          contrainte_reglementaires= data.contrainte_reglementaires,
          complexite_industrielle= data.complexite_industrielle,
          maturite_CdC= data.maturite_CdC,
          complexite_moyens_essais= data.complexite_moyens_essais,
          nb_cycles_dev= data.nb_cycles_dev,
          PM=liste[0],
          AQD_achats=liste[1],
          HW= liste[2],
          SW= liste[3],
          Meca= liste[4],
          Test= liste[5],
          CAO= liste[6],
          Indus= liste[7],
          Peer= liste[8],
          V_and_V= liste[9],
          SDF= liste[10],
          Tech= liste[11],
     )
          session.add(item)
     except Exception as e:
          session.delete(item)
          return f"Erreur : {e}"
     session.commit()


def delete_project(ref:str):
     try:
          connection =engine.connect()
          query = delete(Input_X).where(Input_X.project_name==ref)
          result = connection.execute(query)
          if result.rowcount == 1:
               connection.commit()
               return f"Projet {ref} supprimé"
               
          else :
               return f"Le fichier a déjà été supprimé" 
     except Exception as e :
          return f"Projet non supprimé car non présent dans la base : {e}"

if __name__=="__main__":
     
     projet_000869 = ProjectComplexity(
          reference_project="000869",
          classe_DM=1,
          criticite_patient=6,
          complexite_mecanique=8,
          complexite_electronique=8,
          complexite_logicielle=5,
          complexite_integration=7,
          contrainte_reglementaires=6,
          complexite_industrielle=8,
          maturite_CdC=4,
          complexite_moyens_essais=7,
          nb_cycles_dev=3,
          
     )


     projet_000400 = ProjectComplexity(
               reference_project="000400",
               classe_DM=4,
               criticite_patient=7,
               complexite_mecanique=6,
               complexite_electronique=5,
               complexite_logicielle=3,
               complexite_integration=6,
               contrainte_reglementaires=5,
               complexite_industrielle=2,
               maturite_CdC=2,
               complexite_moyens_essais=5,
               nb_cycles_dev=1,
               
          )

     
     ordre = ["PM","AQD_achats","HW","SW","Meca","Test","CAO","Indus","Peer","V&V","SDF","Tech"]


     cout_MO = [33.5,0,43.25,43.25,0,11,61,0,0,0,0,0]
     list_project()
