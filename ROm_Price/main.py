from Tools.utils import ordre, price
from Tools.models.models import *
from Tools.Classe import ProjectComplexity
from mcp.server import MCPServer

mcp = MCPServer("ROMPrice_MCP")

@mcp.tool(
        name="Jobs_Estimation",
        title ="Estimation coût métier",
        description= "Estimation du coût journalier de chaque corps métier en fonction d'une note attribuée en entrée. "
)
def ROMPrice_Estimation(valeur:ProjectComplexity):
    #Initialisation Sommes totales
    valeur=valeur.to_array()
    Somme_projet_KNN = 0
    Somme_projet_RDM = 0
    Somme_projet_LR = 0
    Somme_projet_PLR = 0

    #Prediction modèles
    liste1 =RDM_predict(valeur)
    liste2 =KNN_predict(valeur)
    liste3 =LR_predict(valeur)
    liste4 =PLR_predict(valeur)
    response = ""
    response = "\t|\tRDM\t |\tKNN\t |\tLR\t |\tPLR\t |\n"
    response += "\t|MO(j)\tBudget(€)|MO(j)\tBudget(€)|MO(j)\tBudget(€)|MO(j)\tBudget(€)|\n"
    response += "-------\t| ------------\t | ------------\t | ------------\t | ------------\t |\n"
    for index,elem in enumerate(ordre) :
        response += f"{elem}\t|"

        #RDM
        prix = 0
        if round(liste1[0][index]) <=0 : liste1[0][index]= 0
        elif ordre[index]=="MO Proto":
            prix = liste1[0][index]*price[index]
        else :
            prix = liste1[0][index]*7*price[index]
        response += f"{round(liste1[0][index])}\t{round(prix)}\t |"
        Somme_projet_RDM += prix
        #KNN
        prix = 0
        if round(liste2[0][index]) <=0 : liste2[0][index]= 0
        elif ordre[index]=="MO Proto":
            prix = liste2[0][index]*price[index]
        else :
            prix = liste2[0][index]*7*price[index]
        response += f"{round(liste2[0][index])}\t{round(prix)}\t |"
        Somme_projet_KNN += prix
        #LR
        prix = 0
        if round(liste3[0][index]) <=0 : liste3[0][index]= 0
        elif ordre[index]=="MO Proto":
            prix = liste3[0][index]*price[index]
        else :
            prix = liste3[0][index]*7*price[index]
        response += f"{round(liste3[0][index])}\t{round(prix)}\t |"
        Somme_projet_LR += prix
        #PLR
        prix = 0
        if round(liste4[0][index]) <=0 : liste4[0][index]= 0
        elif ordre[index]=="MO Proto":
            prix = liste4[0][index]*price[index]
        else :
            prix = liste4[0][index]*7*price[index]
        response += f"{round(liste4[0][index])}\t{round(prix)}\t |"
        Somme_projet_PLR += prix
        response += "\n"
    response += "-------\t| ------------\t | ------------\t | ------------\t | ------------\t |\n"
    response += f"Total\t|\t{round(Somme_projet_RDM)}\t |\t{round(Somme_projet_KNN)}\t |\t{round(Somme_projet_LR)}\t |\t{round(Somme_projet_PLR)}\t |"
    # for index,elem in enumerate(liste1[0]):
    #     prix =0
    #     if round(elem) <=0 : elem = 0
    #     elif ordre[index]=="MO Proto":
    #         prix = elem*price[index]
    #     else :
    #         prix = elem*7*price[index]
    #     response += f"=={ordre[index]}==\n"
    #     response += f"MO : {round(elem)} ; Budget : {round(prix)} €\n"
    #     Somme_projet_RDM +=prix


    # for index,elem in enumerate(liste2[0]):
    #         prix=0
    #         if round(elem) <=0 : elem = 0
    #         elif ordre[index]=="MO Proto":
    #             prix = elem*price[index]
    #         else :
    #             prix = elem*7*price[index]
    #         response += f"=={ordre[index]}==\n"
    #         response += f"MO : {round(elem)} ; Budget : {round(prix)} €\n"
    #         Somme_projet_KNN +=prix

    # for index,elem in enumerate(liste3[0]):
    #             prix =0
    #             if round(elem) <=0 : elem = 0
    #             elif ordre[index]=="MO Proto":
    #                 prix = elem*price[index]
    #             else :
    #                 prix = elem*7*price[index]
    #             response += f"=={ordre[index]}==\n"
    #             response += f"MO : {round(elem)} ; Budget : {round(prix)} €\n"
    #             Somme_projet_LR +=prix
    
    # for index,elem in enumerate(liste4[0]):
    #             prix =0
    #             if round(elem) <=0 : elem = 0
    #             elif ordre[index]=="MO Proto":
    #                 prix = elem*price[index]
    #             else :
    #                 prix = elem*7*price[index]
    #             response += f"=={ordre[index]}==\n"
    #             response += f"MO : {round(elem)} ; Budget : {round(prix)} €\n"
    #             Somme_projet_PLR +=prix
    
    # response += "---------BILAN----------\n"
    # response += f"Prix_RDM : {round(Somme_projet_RDM)} € \nPrix_KNN : {round(Somme_projet_KNN)} € \nPrix_LR : {round(Somme_projet_LR)} €\nPrix_PLR : {round(Somme_projet_PLR)} €\n"
    return response

    


if __name__ == "__main__":

    #Données de test
    project_ROMIO = ProjectComplexity(
        reference_project = "ROMIO",
        classe_DM=4,
        criticite_patient=9,
        complexite_mecanique=9,
        complexite_electronique=8,
        complexite_logicielle=8,
        complexite_integration=8,
        contrainte_reglementaires=9,
        complexite_industrielle=8,
        complexite_moyens_essais=4,
        maturite_CdC=2,
        nb_cycles_dev=4,
    )

    projet_001359 = ProjectComplexity(
              reference_project="001359",
              classe_DM=1,
              criticite_patient=1,
              complexite_mecanique=2,
              complexite_electronique=8,
              complexite_logicielle=7,
              complexite_integration=8,
              contrainte_reglementaires=6,
              complexite_industrielle=6,
              maturite_CdC=6,
              complexite_moyens_essais=8,
              nb_cycles_dev=1,
              
         )
    
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
    

    
    print(ROMPrice_Estimation(project_ROMIO))


    