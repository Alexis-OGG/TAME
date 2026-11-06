from pydantic import BaseModel, Field,model_validator,field_validator
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

class OrigineDocument(str, Enum):
    CLIENT = "client"
    TAME_CARE = "tame-care"
    CO_CONSTRUIT = "co-construit"
    NON_SPECIFIE = "non-specifie"


class ResponsabiliteDocument(str, Enum):
    RESPONSABLE = "R"
    APPROBATEUR = "A"
    CONTRIBUTEUR = "C"
    INFORME = "I"
    NON_SPECIFIE = "NS"

class Besoin(BaseModel):

    Avancement: str = Field(
        description="""
        Etat simplifié de l'avancement du client (discussions et documents clients fournis). Une phrase longue (2 lignes max)

        """
    )

    Besoin: str = Field(
        description="""
        Description complète des objectifs de TAME-Care pour répondre au besoin. Préciser les grosses étapes très simplement.(2 lignes max)
        """
    )

    Role_TAME: str = Field(
        description="""
        Rôle  de TAME-CARE, Explique pourquoi le client a fait appel à TAME-CARE. Résumé en une ou deux phrases. (2 lignes max)
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

        FORMAT :

        Sous-ensemble 1
            Hypothèse 1
            Hypothèse 2
            Hypothèse 3

        Sous-ensemble 2
            Hypothèse 1
            Hypothèse 2

        RÈGLES :
        - chaque ligne comporte une balise de fin "\n" ;
        - chaque hypothèse commence par une tabulation "\t" ;
        - ne jamais générer un paragraphe continu ;
        - ne jamais concaténer plusieurs hypothèses sur la même ligne.
        """
    )
    @field_validator("List_Hypotheses")
    def validate_tabs(cls, value):

        lignes = value.splitlines()

        if not any(ligne.startswith("\t") for ligne in lignes):
            raise ValueError(
                "Les hypothèses doivent contenir au moins une ligne tabulée."
            )

        return value

class SubTache(BaseModel):
    nom : str = Field(description="Nom de la sous tâche. Identifiable dans la feuille 'Objectgifs Etudes' avec un * ")
    duree : float = Field(description="duree de la sous tâche")
    debut : float = Field(ge=0,description="Début de la sous tâche en id de la semaine depuis T0.")
    jalon : Optional[List[float]] = Field(description="Id de la semaine du Jalon de la sous tâche")
    couleur : str = Field (description= """
        Couleur barre gantt.
        Liste dispo:
        -5377B9 : Autres
        -8EA8D4 : tache validation/test
    """)

class Document(BaseModel):
    img_doc: imageDoc = Field(
        description="""
        Chemin vers l'icône correct pour décrire le document.

        règles  : 
        - img/doc_bleu.png : si client = Responsable et Apporbateur  &  si TAME-CARE = Consulte/Contribue et Informé
        - img/doc_orange.png : si client = Apporbateur, Consulte/Contribue et Informé & si TAME-CARE = Responsable
        - img/doc_gris.png : si Non spécifié et non chiffré

        """
    )

    text_doc: str = Field(
        description="""
        Nom ou description du document.  3-4 mots maximum. Privilégié format Acronyme universel que le client peut comprendre

        Exemple :
        Cdc 
        """
    )
    responsabilite_client: ResponsabiliteDocument
    responsabilite_tame: ResponsabiliteDocument
    @model_validator(mode="after")
    def calculer_icone(self):
        if (
            self.responsabilite_client
            in {
                ResponsabiliteDocument.RESPONSABLE,
                ResponsabiliteDocument.APPROBATEUR,
            }
            and self.responsabilite_tame
            in {
                ResponsabiliteDocument.CONTRIBUTEUR,
                ResponsabiliteDocument.INFORME,
            }
        ):
            self.img_doc = imageDoc.BLEU

        elif (
            self.responsabilite_tame
            == ResponsabiliteDocument.RESPONSABLE
        ):
            self.img_doc = imageDoc.ORANGE

        else:
            self.img_doc = imageDoc.GRIS

        return self

class DocumentsLot(BaseModel):

    Donnees_entree: List[Document] = Field(
        default_factory=list,
        description="""
        Liste des documents utilisés en entrée du lot. Ne pas dépasser 5. Prends les plus importants. Chaque donnée d'entrée est indiqué par 3-mots maximum. Préconise l'utilisation d'acronymes

        Exemple :
        - Cahier des charges
        - Plans mécaniques
        - Données d'interface
        """
    )

    Livrables: List[Document] = Field(
        default_factory=list,
        description="""
        Liste des documents souvent produits par TAME-Care. Ne pas dépasser 5. Prends les plus importants

        Exemple :
        - TRS
        - Dossier de conception
        - Matrice de conformité
        """
    )


class Lot(BaseModel):
    phase: str = Field(
        description="""
        Phase auquel appartient le lot. Liste des type de phases : POC, Prototype A, Prototype Q, Industrialisation, Clôture Projet
        Exemple : Phase 2 : Prototype A
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

    Inclure sections:
        - Objectif
        - Activités
        - Hors périmètre

    Texte formaté obligatoire.

    FORMAT :

    Objectif
        objectif 1
        objectif 2

    Activités
        activité 1
        activité 2

    Hors périmètre
        hors périmètre 1
        hors périmètre 2

    RÈGLES :
    - chaque fin de ligne comporte une balise de fin "\n" ;
    - conserver les titres de section ;
    - chaque sous-élément commence par une tabulation "\t" ;
    - chaque élément est sur une ligne distincte ;
    - ne jamais écrire :
        Objectif : texte...
        Activités : texte...
    
    """
    )

    documents: DocumentsLot = Field(
        description="Documents (Données d'entrée et Livrables avec icônes) associés au lot.  "
    )

    debut:float=Field(ge=0.0,description="Début du lot (en semaines) par rapport à l'id de la semaine du début du projet. Commence ABSOLUMENT à 0 pour le premier lot. Source : Planning ou Gantt")

    duree : float = Field(description="""
        Nombres de semaines estimer pour réaliser ce lot. Prends en compte les semaines de fermeture
    """)

    jalon:Optional[List[float]] = Field(description="Id de la semaine du Jalon")

    cout : float = Field(description="""
            Coût du Lot
        """)

    facturation : float = Field(description="""
                facturation du Lot
    """)

    sous_tache: List[SubTache]

class SyntheseFinanciere(BaseModel):
    # config_tableau: ConfigurationTableau
    lots: List[Lot]


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

    id_semaine_debut: Optional[int] = Field(ge=1,
            le=52,
                description="""
                numéro de la semaine de début du projet (voir planning)
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

    nom_fichier: str = Field(
        description="""
        nom du fichier du projet interne. Ex : DEV-00484-2026

        """
    )

    donnees_entree:str = Field(description="""
        Documents CLIENT qui contiennent les données d'entrée qui ont permit la création du devis. Ne pas mettre l'ET78. Souvent il s'agis des documents client et des discussions avec le client.
        
        FORMAT : Liste (sans tirer seuelement retour à la ligne)
        Exemple : cachier des charges techniques (CdCT) \n échanges techniques client
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
