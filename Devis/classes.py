from pydantic import BaseModel, Field
from typing import List,Dict,Optional
from enum import Enum
class imageLot(str, Enum):
    TECHNIQUE: str= "img/technique.png"
    DESIGN: str= "img/design.png"
    USINE: str= "img/usine.png"
    IDEE: str= "img/idee.png"

class imageDoc(str, Enum):
    BLEU: str= "img/doc_bleu.png"
    ORANGE: str= "img/doc_orange.png"
    GRIS: str= "img/doc_gris.png"


class PresentationData(BaseModel):

    titre_presentation: str = Field(
        description="""
        Titre principal affiché sur la page de garde.

        Placeholder PPT :
        TITLE_PRESENTATION
        """
    )

    logo_client: str = Field(
        description="""
        Logo du client.

        Fournir idéalement :
        - un chemin d'image
        - une URL
        - format base64

        Eviter les Base64 dans les prompts.
        """
    )

    nom_projet: str = Field(
        description="""
        Nom officiel du projet.
        """
    )

    Annee: str = Field(
        description="""
        Annee

        Format :
        AAAA
        """
    )

    entreprise: str = Field(
        description="""
        Nom du client.

        Placeholder PPT :
        CUSTOMER_NAME
        """
    )

    id_projet: str = Field(
        description="""
        Référence projet interne ou client.

        """
    )

    donnees_entree:str = Field(description="""
        Documents CLIENT qui contiennent les données d'entrée qui ont permit la création du devis. Ne pas mettre l'ET78. Souvent il s'agis des documents client et des discussions avec le client.
        
        FORMAT : Liste 
        Exemple : -cachier des charges techniques (CdCT)
    """
    )

    Besoin: Besoin 

    hypotheses: List[Hypothese] = Field(
        default_factory=list,
        description="""
        Ensemble des hypothèses techniques utilisées dans le projet. Rassemnlez les hypothèses le plus possible les hypothèses ensembles. Les principales hypotèhes doivent concerner l'électronique, la mécanique, et le logiciel.
        """
    )

    lots_list: SyntheseFinanciere = Field(
        default_factory=list,
        description="""
        Ensemble des lots du projet. 
        """
    )
    #Ne pas Inclure la réunion de lancement dans les lots

class Besoin(BaseModel):

    Avancement: str = Field(
        description="""
        Etat simplifié de l'avancement du client (discussions et documents clients fournis)

        """
    )

    Besoin: str = Field(
        description="""
        Description complète des objectifs de TAME-Care pour répondre au besoin. Préciser les grosses étapes très simplement.
        """
    )

    Role_TAME: str = Field(
        description="""
        Rôle  de TAME-CARE, Explique pourquoi le client a fait appel à TAME-CARE. Résumé en une ou deux phrases. 
        """
    )

class Hypothese(BaseModel):

    Type_Hypothese: str = Field(
        description="""
        Catégorie de l'hypothèse. 

        Exemple :
        Hypothèses électroniques
        Hypothèses mécaniques
        Hypothèses logiciel
        """
    )

    List_Hypotheses: str = Field(
        description="""
        Texte complet décrivant les hypothèses techniques.Les hypothèses sont présentes dans le fichier ET78 et tu peux vérifier qu'elles couvrent l'entièreté du Cdc.

        Conserver le format paragraphe ou liste.
        """
    )

class SubTache(BaseModel):
    nom : str = Field(description="Nom de la sous tâche. Identifiable dans la feuille 'Objectgifs Etudes' avec un * ")
    duree : float = Field(description="duree de la sous tâche")
    debut : float = Field(description="Début de la sous tâche en id de la semaine depuis T0")
    jalon : Optional[List[float]] = Field(description="Id de la semaine du Jalon de la sous tâche")
    couleur : str = Field (description= """
        Couleur barre gantt.
        Liste dispo:
        -5377B9 : Autres
        -8EA8D4 : tache validation/test
    """)

class Lot(BaseModel):
    phase: str = Field(
        description="""
        Phase auquel appartient le lot.
        Exemple : Phase 1 : Prototype
        """
    )
    
    nom: str = Field(
        description="""
        Nom complet du lot.
        Exemple : LOT1 : Spécification Technique du Besoin (SR)
        """
    )

    image_lot: imageLot = Field(
        description="""
        Image illustrant le lot.

        liste disponibles :
        - img/technique.png
        - img/design.png
        - img/usine.png
        - img/idee.png
        """
    )

    details_lot: str = Field(
        description="""
        Description détaillée du contenu du lot. Conserver le format paragraphe ou liste.
        Inclure :
        - Objectif
        - Activités
        - Hors périmètre
        """
    )

    documents: DocumentsLot = Field(
        description="Documents (Données d'entrée et Livrables avec icônes) associés au lot.  "
    )

    # donnees_tableau: Dict[str, str] = Field(
    #     description="""
    #     Dictionnaire des valeurs de ce lot pour le tableau de synthèse.
    #     Les clés doivent correspondre EXACTEMENT aux noms définis dans ConfigurationTableau.colonnes.
    #     Valeur = Contenu de la cellule.
    #     Exemple : {"LOTS": "LOT 1", "ACTIVITÉS": "Développement", "PRIX": "5000 €"}
    #     """
    # )
    debut:float=Field(description="Début du lot en id de la semaine depuis T0")

    duree : float = Field(description="""
        Nombres de semaines estimer pour réaliser ce lot
    """)

    jalon:Optional[List[float]] = Field(description="Id de la semaine du Jalon")

    cout : float = Field(description="""
            Coût du Lot
        """)

    facturation : float = Field(description="""
                facturation du Lot
    """)

    sous_tache: Optional[List[SubTache]]



# class ConfigurationTableau(BaseModel):
#     colonnes: List[str] = Field(
#         description="""
#         Liste dynamique des noms de colonnes pour le tableau de synthèse. 
#         À définir selon le contexte du devis.
#         Exemple : ["LOTS", "DONNÉES D'ENTRÉE", "ACTIVITÉS", "LIVRABLES", "DÉLAIS", "PRIX", "FACTURATION"]
#         """
#     )
#     totaux: Dict[str, str] = Field(
#         description="""
#         Dictionnaire contenant les valeurs de la dernière ligne (Totaux).
#         Clé = Nom exact de la colonne, Valeur = Montant ou Texte à afficher.
#         Exemple : {"LIVRABLES": "TOTAL :", "PRIX": "15 000 €", "FACTURATION": "15 000 €"}
#         Laisser vide si le tableau ne nécessite pas de totaux.
#         """
#     )

class SyntheseFinanciere(BaseModel):
    # config_tableau: ConfigurationTableau
    lots: List[Lot]

class Graph(BaseModel):

    image_graph: str = Field(
        description="""
        Image représentant le graphique.

        Exemple :
        /img/performance.png
        """
    )

    texte_graph: str = Field(
        description="""
        Légende ou résumé associé au graphique.
        """
    )

class DocumentsLot(BaseModel):

    Donnees_entree: List[Document] = Field(
        default_factory=list,
        description="""
        Liste des documents clients utilisés en entrée du lot. Ne pas dépasser 5. Prends les plus importants. Chaque donnée d'entrée est indiqué par 3-mots maximum. Préconise l'utilisation d'acronymes

        Exemple :
        - Cahier des charges
        - Plans mécaniques
        - Données d'interface
        """
    )

    Livrables: List[Document] = Field(
        default_factory=list,
        description="""
        Liste des documents produits par TAME-Care. Ne pas dépasser 5. Prends les plus importants

        Exemple :
        - TRS
        - Dossier de conception
        - Matrice de conformité
        """
    )

class Document(BaseModel):
    img_doc: imageDoc = Field(
        description="""
        Chemin vers l'icône correct pour décrire le document.

        règles  : 
        - img/doc_bleu.png : si client = Apporbateur et Responsable & TAME = Consulte/Contribue et Informé
        - img/doc_orange.png : si client = Apporbateur, Consulte/Contribue et Informé & TAME = Responsable
        - img/doc_orange.png : si Non spécifié et non chiffré

        """
    )

    text_doc: str = Field(
        description="""
        Nom ou description du document. Privilégié format Acronyme universel.

        Exemple :
        Cdc 
        """
    )

