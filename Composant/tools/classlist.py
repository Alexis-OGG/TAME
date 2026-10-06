from pydantic import Field,BaseModel
from typing import Optional
class StatutGlobal(BaseModel):
    Consensus: str = Field(
        description="Statut global déduit pour le composant (ex: Actif, Obsolète, NRND)."
    )
    Alerte_Conflit: bool = Field(
        description="Vrai si les distributeurs se contredisent sur le statut, Faux sinon."
    )
    Details_Distributeurs: dict = Field(
        description="Détail des statuts renvoyés par chaque distributeur (ex: {'Mouser': 'Actif', 'Digikey': 'Obsolète'})."
    )
class Price(BaseModel):
    Quantite:str  = Field(description="Quantité")
    Prix_Unitaire:str  = Field(description="Prix unitaire")
class Offres(BaseModel):
    Distributeur: str  = Field(description="nom du distributeur (ex : Mouser)")
    Conditionnement:str  = Field(description="conditionnement du composant")
    Stock:int  = Field(description="Stock disponible total")
    MOQ: float = Field(description="quantité min achat")
    Prix_Unitaire: str =Field(description="Grille Prix")
class ParametersClass(BaseModel):
    Nom:str  = Field(description="Label du paramètre")
    Value:str  = Field(description="Valeur de se label")
class Tech(BaseModel):
    
    # REF:str  = Field(description="Ref du composant")
    # Description :str = Field(description="Liste des paramètre techniques") #list[ParametersClass]|
    # Package : list[PackageClass] = Field(description="Stock disponible en fonciton de son conditionnement")
    Rohs:str  = Field(description="statut Rohs")
    Reach:str  = Field(description="statut Reach")
    Temp_fonc:str  = Field(description="Température de fonctionnement")
    Temp_stock:str  = Field(description="Température de stockage")
    humidity:str  = Field(description="Humidité")
    Floor_life:str  = Field(description="Durée de vie après ouverture")
    boitier: str  = Field(description="dimensions du produit")
    Dimensions:str  = Field(description="dimensions du produit")
class main(BaseModel):
        # REF_FAB: str  = Field(description="ref du composant cherché")
        Fabricant: str  = Field(description="Fabricant du composant")
        Fiche_Technique : str  = Field(description="url de la fich technique")
        Equivalents_Suggeres: list[str]  = Field(description="liste de composants équivalents")
        Statut_Global: StatutGlobal = Field(description="Informations globales sur le statut ")
        Offres_Disponibles: list[Offres] = Field(description="liste des offres composants : stock en fonction conditionnement")

class ResultFabProduct(BaseModel):
    techniques : list[Tech]
    offres : list[Offres]

class ResultAllProduct(BaseModel):
     main : main
     liste_products : dict[str,ResultFabProduct]
     
class ErreurMsg(BaseModel):
    erreur_message: Optional[str] = None


