from pydantic import BaseModel, Field

#Classe à fournir au Model IA pour remplir formulaire
class ProjectComplexity(BaseModel):
    reference_project : str = Field(description="Référence de projet (Ex: 001359)")
    classe_DM: int = Field(
        ge=1,
        le=5,
        description="""
        Classe du duspositif médical (DM)

        1 = Pas un DM
        2 = DM Div I
        3 = DM div IIA
        4 = DM DIV IIb
        5 = DM DIV III

        """
    )

    criticite_patient: int = Field(
        ge=1,
        le=10,
        description="""
        Gravité de la conséquence potentielle d'une défaillance.

        1 = inconfort
        4 = usage perturbé
        6 = blessure légère réversible
        8 = blessure grave
        10 = handicap permanent ou décès

        Exemple :
        dispositif ophtalmique invasif = 5
        """
    )

    complexite_mecanique: int = Field(
        ge=1,
        le=10,
        description="""
            Complexité mécanique pure. Complexité des liaisons, degré de liberté de mouvement, intéractions avec l'extérieur, complexité des géométries

        """
    )

    complexite_electronique: int = Field(
            ge=1,
            le=10,
            description="""
            Complexité électronique pure. Complexité des PCB, nombres de fonctions, contraintes de fonctionnement, intéraction avec l'extérieur

            """
        )

    complexite_logicielle: int = Field(
        ge=1,
        le=10,
        description="""
        Complexité du logiciel embarqué et applicatif.

        1 = logiciel simple
        4 = logique métier basique
        6 = IHM avancée
        8 = temps réel et interfaces multiples
        10 = logiciel critique temps réel multicouches
        """
    )

    complexite_integration: int = Field(
        ge=1,
        le=10,
        description="""
        Nombre et diversité des sous-systèmes à interfacer.

        1 = système autonome
        4 = quelques interfaces
        6 = plusieurs sous-systèmes
        8 = architecture distribuée
        10 = intégration complexe multi-fournisseurs

        Exemple :
        robot + cloud + PACS + OCT = 5
        """
    )

    contrainte_reglementaires: int = Field(
        ge=1,
        le=10,
        description="""
        Difficulté réglementaire globale.

        1 = hors médical
        4 = accessoire médical
        6 = DM simple
        7 = DM critique
        10 = DM invasif avec logiciel critique ou IA

        Exemple :
        robot d'injection ophtalmique = 5
        """
    )

    complexite_industrielle: int = Field(
        ge=1,
        le=10,
        description="""
        Difficulté de fabrication et d'industrialisation.

        Critères :
        - calibration
        - stérilité
        - précision mécanique
        - assemblage complexe

        1 = assemblage simple
        10 = production critique haute précision
        """
    )

    maturite_CdC: int = Field(
        ge=1,
        le=10,
        description="""
        Niveau d'avancement du Cdc et du besoin. Cette variable est corrélée avec la nécessité de réaliser une phase de spécifiation.
        """
    )

    complexite_moyens_essais : int = Field(
        ge=1,
        le=10,
        description="""

        Moyens d'essais du produit

        1 = peu ou pas de banc spécifique
        4 = adaptation de banc existant
        6 = banc dédié simple
        8 = plusieurs bancs dédiés
        10 = moyens d'essais complexes et spécifiques

        Cette varaible est corrélé à TAME-Test

        """
    )

    nb_cycles_dev : int = Field(
        ge=1,
        le=4,
        description="""

        nombre de cycles de dévelopement nécessaire (Poc, Proto A, Proto Q, indus)

        """
    )

    def to_array(self):
        return [dist  for elem,dist in self if elem!="reference_project" ]
