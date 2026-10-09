from sqlalchemy import select,create_engine
from sqlalchemy.orm import Session
from Ressources.create_db import Input_X
from Tools.Classe import ProjectComplexity

#Données d'entraînements : 19 projets stockés
project_001088 = ProjectComplexity(
    reference_project="001088",
    classe_DM=3,
    criticite_patient=10,
    complexite_mecanique=8,
    complexite_electronique=10,
    complexite_logicielle=8,
    complexite_integration=8,
    contrainte_reglementaires=8,
    complexite_industrielle=10,
    maturite_CdC=4,
    nb_cycles_dev=3,
    complexite_moyens_essais=4
    # ia=False,
    # robotique=False,
    # imagerie=False,
    # cloud=False,
    # cybersecurite=True,
    # sterilisation=False,
    # application_mobile=False,
    # phase_poc= True, 
    # phase_proto_a= True ,
    # phase_proto_q= True ,
    # phase_indus= True,
)

project_000213 = ProjectComplexity(
    reference_project="000213",
    classe_DM=4,
    criticite_patient=10,
    complexite_mecanique=8,
    complexite_electronique=6,
    complexite_logicielle=6,
    complexite_integration=8,
    contrainte_reglementaires=8,
    complexite_industrielle=10,
    complexite_moyens_essais=6,
    maturite_CdC=4,
    nb_cycles_dev=3,
    # ia=False,
    # robotique=True,
    # imagerie=False,
    # cloud=False,
    # cybersecurite=True,
    # sterilisation=True,
    # application_mobile=False,
)

project_001998 = ProjectComplexity(
    reference_project="001998",
    classe_DM=4, #
    criticite_patient=8,#
    complexite_mecanique=6,
    complexite_electronique=6,
    complexite_logicielle=6,
    complexite_integration=6,#
    contrainte_reglementaires=8, #
    complexite_industrielle=10,
    complexite_moyens_essais=2,
    maturite_CdC=8, #
    nb_cycles_dev=2,
    # ia=False,
    # robotique=True,
    # imagerie=True,
    # cloud=True,
    # cybersecurite=True,
    # sterilisation=False,
    # application_mobile=True,
)

project_001991 = ProjectComplexity(
    reference_project="001991",
    classe_DM=3, 
    criticite_patient=6,
    complexite_mecanique=8,
    complexite_electronique=6,
    complexite_logicielle=4,
    complexite_integration=8,
    contrainte_reglementaires=8, 
    complexite_industrielle=2,
    complexite_moyens_essais=4,
    maturite_CdC=6, 
    nb_cycles_dev=1,
    # ia=False,
    # robotique=False,
    # imagerie=True,
    # cloud=False,
    # cybersecurite=True,
    # sterilisation=False,
    # application_mobile=False,
)

project_001779 = ProjectComplexity(
    reference_project="001779",
    classe_DM=3, #
    criticite_patient=4,
    complexite_mecanique=8,
    complexite_electronique=6,
    complexite_logicielle=6,
    complexite_integration=6,
    contrainte_reglementaires=6, 
    complexite_industrielle=2,#
    complexite_moyens_essais=2,
    maturite_CdC=8,# 
    nb_cycles_dev=2,#
    # ia=False,
    # robotique=True,
    # imagerie=True,
    # cloud=False,
    # cybersecurite=False,
    # sterilisation=False,
    # application_mobile=False,
)

project_001504 = ProjectComplexity(
    reference_project="001504",
    classe_DM=3, #
    criticite_patient=6,
    complexite_mecanique=10,
    complexite_electronique=8,
    complexite_logicielle=8,#
    complexite_integration=10,
    contrainte_reglementaires=10, #
    complexite_industrielle=2,
    complexite_moyens_essais=6,
    maturite_CdC=8,
    nb_cycles_dev=3,#
    # ia=True,
    # robotique=False,
    # imagerie=False,
    # cloud=False,
    # cybersecurite=True,
    # sterilisation=False,
    # application_mobile=True,
)

project_001363 = ProjectComplexity(
    reference_project="001363",
    classe_DM=2, #
    criticite_patient=2,
    complexite_mecanique=8,
    complexite_electronique=8,
    complexite_logicielle=4,#
    complexite_integration=8,
    contrainte_reglementaires=4, #
    complexite_industrielle=6,
    complexite_moyens_essais=6,
    maturite_CdC=4,#
    nb_cycles_dev=3,#
# ia=False,
# robotique=False,
# imagerie=False,
# cloud=False,
# cybersecurite=True,
# sterilisation=False,
# application_mobile=True,
)

project_001294 = ProjectComplexity(
    reference_project="001294",
    classe_DM=2,
    criticite_patient=2,
    complexite_mecanique=4,
    complexite_electronique=8,
    complexite_logicielle=6,
    complexite_integration=8,
    contrainte_reglementaires=4,
    complexite_industrielle=2,
    complexite_moyens_essais=2,
    maturite_CdC=8,
    nb_cycles_dev=1
# ia=False,
# robotique=False,
# imagerie=False,
# cloud=False,
# cybersecurite=True,
# sterilisation=False,
# application_mobile=False,
)

project_001602 = ProjectComplexity(
    reference_project="001602",
    classe_DM=2,
    criticite_patient=4,
    complexite_mecanique=6,
    complexite_electronique=8,
    complexite_logicielle=8,
    complexite_integration=8,
    contrainte_reglementaires=10,
    complexite_industrielle=6,
    complexite_moyens_essais=8,
    maturite_CdC=4,
    nb_cycles_dev=2
# ia=False,
# robotique=False,
# imagerie=False,
# cloud=False,
# cybersecurite=True,
# sterilisation=True,
# application_mobile=False,
)

project_000773 = ProjectComplexity(
    reference_project="000773",
    classe_DM=2,
    criticite_patient=8,
    complexite_mecanique=4,
    complexite_electronique=6,
    complexite_logicielle=4,
    complexite_integration=6,
    contrainte_reglementaires=8,
    complexite_industrielle=6,
    complexite_moyens_essais=8,
    maturite_CdC=8,
    nb_cycles_dev=2
# ia=False,
# robotique=True,
# imagerie=False,
# cloud=False,
# cybersecurite=True,
# sterilisation=True,
# application_mobile=False,
)

project_000323 = ProjectComplexity(
    reference_project="000323",
classe_DM=4,
criticite_patient=2,
complexite_mecanique=2,
complexite_electronique=2,
complexite_logicielle=2,
complexite_integration=2,
contrainte_reglementaires=2,
complexite_industrielle=2,
complexite_moyens_essais=10,
maturite_CdC=10,
nb_cycles_dev=1
)

project_001484 = ProjectComplexity(
    reference_project="001484",
    classe_DM=4,
    criticite_patient=8,
    complexite_mecanique=4,
    complexite_electronique=6,
    complexite_logicielle=6,
    complexite_integration=6,
    contrainte_reglementaires=4,
    complexite_industrielle=2,
    complexite_moyens_essais=2,
    maturite_CdC=8,
    nb_cycles_dev=2
)

project_001782 = ProjectComplexity(
    reference_project="001782",
    classe_DM=4,
    criticite_patient=8,
    complexite_mecanique=6,
    complexite_electronique=8,
    complexite_logicielle=8,
    complexite_integration=6,
    contrainte_reglementaires=2,
    complexite_industrielle=8,
    complexite_moyens_essais=2,
    maturite_CdC=10,
    nb_cycles_dev=1
)

projet_002032=ProjectComplexity(
    reference_project="002032",
    classe_DM=3,
    criticite_patient=8,
    complexite_mecanique=8,
    complexite_electronique=10,
    complexite_logicielle=2,
    complexite_integration=10,
    contrainte_reglementaires=10,
    complexite_industrielle=8,
    maturite_CdC=8,
    complexite_moyens_essais=2,
    nb_cycles_dev=2
)

projet_001934=ProjectComplexity(
    reference_project="001934",
        classe_DM=1,
        criticite_patient=2,
        complexite_mecanique=2,
        complexite_electronique=2,
        complexite_logicielle=6,
        complexite_integration=2,
        contrainte_reglementaires=6,
        complexite_industrielle=4,
        maturite_CdC=10,
        complexite_moyens_essais=2,
        nb_cycles_dev=1,
)
    
projet_000239= ProjectComplexity(
    reference_project="000239",
    classe_DM=2,
    criticite_patient=8,
    complexite_mecanique=8,
    complexite_electronique=8,
    complexite_logicielle=8,
    complexite_integration=8,
    contrainte_reglementaires=8,
    complexite_industrielle=4,
    maturite_CdC=6,
    complexite_moyens_essais=2,
    nb_cycles_dev=1,
)

project_001024 = ProjectComplexity(
    reference_project="001024",
    classe_DM=3,
    criticite_patient=10,
    complexite_mecanique=6,
    complexite_electronique=8,
    complexite_logicielle=6,
    complexite_integration=8,
    contrainte_reglementaires=10,
    complexite_industrielle=2,
    maturite_CdC=8,
    complexite_moyens_essais=2,
    nb_cycles_dev=1, 
)

projet_000970 = ProjectComplexity(
    reference_project="000970",
    classe_DM=2,
    criticite_patient=6,
    complexite_mecanique=4,
    complexite_electronique=8,
    complexite_logicielle=6,
    complexite_integration=10,
    contrainte_reglementaires=6,
    complexite_industrielle=2,
    maturite_CdC=8,
    complexite_moyens_essais=2,
    nb_cycles_dev=2,
)
#---------------------------------------------------------------------------
projet_001961 = ProjectComplexity(
    reference_project="001961",
    classe_DM=2,
    criticite_patient=6,
    complexite_mecanique=1,
    complexite_electronique=6,
    complexite_logicielle=6,
    complexite_integration=6,
    contrainte_reglementaires=1,
    complexite_industrielle=2,
    maturite_CdC=6,
    complexite_moyens_essais=1,
    nb_cycles_dev=1,
)

projet_251106 = ProjectComplexity(
          reference_project="251106",
          classe_DM=4,
          criticite_patient=8,
          complexite_mecanique=6,
          complexite_electronique=8,
          complexite_logicielle=8,
          complexite_integration=9,
          contrainte_reglementaires=9,
          complexite_industrielle=7,
          maturite_CdC=3,
          complexite_moyens_essais=8,
          nb_cycles_dev=3,
          
     )

projet_250414 = ProjectComplexity(
          reference_project="250414",
          classe_DM=4,
          criticite_patient=9,
          complexite_mecanique=4,
          complexite_electronique=7,
          complexite_logicielle=9,
          complexite_integration=8,
          contrainte_reglementaires=9,
          complexite_industrielle=6,
          maturite_CdC=5,
          complexite_moyens_essais=5,
          nb_cycles_dev=3,
          
     )
projet_001058 = ProjectComplexity(
          reference_project="001058",
          classe_DM=3,
          criticite_patient=4,
          complexite_mecanique=2,
          complexite_electronique=8,
          complexite_logicielle=7,
          complexite_integration=8,
          contrainte_reglementaires=6,
          complexite_industrielle=4,
          maturite_CdC=7,
          complexite_moyens_essais=1,
          nb_cycles_dev=1,
          
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

projet_000693 = ProjectComplexity(
               reference_project="000693",
               classe_DM=2,
               criticite_patient=4,
               complexite_mecanique=7,
               complexite_electronique=6,
               complexite_logicielle=7,
               complexite_integration=6,
               contrainte_reglementaires=6,
               complexite_industrielle=7,
               maturite_CdC=8,
               complexite_moyens_essais=7,
               nb_cycles_dev=2,
               
          )

projet_001168 = ProjectComplexity(
                   reference_project="001168",
                   classe_DM=2,
                   criticite_patient=5,
                   complexite_mecanique=4,
                   complexite_electronique=4,
                   complexite_logicielle=3,
                   complexite_integration=4,
                   contrainte_reglementaires=5,
                   complexite_industrielle=5,
                   maturite_CdC=2,
                   complexite_moyens_essais=4,
                   nb_cycles_dev=4,
                   
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

#Données D'entraînements
X :list[ProjectComplexity]= [project_001088,project_000213,project_001998,project_001991,project_001779,project_001504,project_001363,project_001294,project_001602,project_000773,project_000323,project_001484,project_001782,projet_002032,projet_001934,projet_000239,project_001024,projet_000970,projet_251106,projet_001961,projet_250414,projet_001058,projet_001359,projet_000693,projet_001168,projet_000400]

Y_WP = [
    [104.18,12.7,169.25,161.75,159.25,8,40,3,25.3,101,0,7],#001088 74
    [138.82,53.8,62.75,127.75,260,15,41,19,23.7,125.5,0,12], #000213 313
    [61.49,20.355,106.5,120,182.40,0,27.50,0,19.6,14,0,3],#001998,0
    [31.37,9.615,40.4,26.4,160.5,4,11.4,0,9,17.9,0,9],#001991,0
    [35.3375,10.7375,77.75,104,15,0,14,0,0,3,0,2], #001779,10
    [111.99,29.8625,164,186.25,206.85,19.5,38,6,6,80.5,0,19.5],#001504,84
    [62.98,34.76,140,14,130,19.55,67,17.5,14,64,0,24], #001363,25
    [44.805,0,80.75,82.25,19.75,0,31,2,10.7,3,0,10], #001294,16
    [99.9125,42.96,115,124,62.7,56,21.5,6,20.75,121.5,0,2], #001602,877
    [69.22,18.456,84.2,10.2,29.5,36.7,33.7,5,6.8,48.7,0,5], #000773,462
    [29.875,11.52,0,0,0,132,3,0,10.5,0,0,0], #000323
    [26.4,5.8,79.5,52,20.5,0,10,0,0,14,0,0], #001484
    [55.705,13.482,84.05,136.95,85.95,0,36.5,0,9.5,0,0,2.5], #001782
    [89.68,35.04,149.5,0,235.5,0,0,0,9.5,67,0,0], #02032
    [11.77,4.475,0,30,0,0,0,0,9,29.5,0,0], #01934
    [49.86,12.695,70.5,202,59,18,0,0,6,34.9,2,0], #00239
    [31.2125,16.84,68,56.5,36.5,0,14.5,0,4.25,14,0,1], #01024
    [28.037,3.384,45.2,75.1,26,0,22,0,4.25,16,0,1] ,#0970
    [244.62585034013605, 0.0, 306.1224489795918, 214.96598639455783, 442.17687074829934, 24.489795918367346, 0.0, 16.3265306122449, 0.0, 193.1972789115646, 0.0, 0.0], #251106
    [13.2,3,32,43,2,0,11,0,0,0,0,0], #001961
    [24.857142857142858, 0.0, 257.1428571428571, 108.57142857142857, 135.7142857142857, 20.0, 0.0, 200.0, 0.0, 44.285714285714285, 0.0, 0.0] #250414,
    [7.27,0,25.2,44.5,0,0,0,0,0,3,0,0], #001058
    [55.1,25,108,175.5,0,0,42.5,0,0,30,0,2.5], #001359,
    [85.8,0,98.9,35.3,184,25.4,0,0,0,56.6,0,0] ,#000693
    [93.9,2.3,125.6,125.6,163.2,27.2,0,16.3,0,68,0,0],#001168 -> NE PAS L'INCLURE
    [33.5,0,43.25,43.25,0,11,61,0,0,0,0,0],#000400
]



engine = create_engine("sqlite:///Ressources/Project_db")

with Session(engine) as session:
    for index, data in enumerate(X):    
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
            PM=Y_WP[index][0],
            AQD_achats=Y_WP[index][1],
            HW= Y_WP[index][2],
            SW= Y_WP[index][3],
            Meca= Y_WP[index][4],
            Test= Y_WP[index][5],
            CAO= Y_WP[index][6],
            Indus= Y_WP[index][7],
            Peer= Y_WP[index][8],
            V_and_V= Y_WP[index][9],
            SDF= Y_WP[index][10],
            Tech= Y_WP[index][11],
        )
        session.add(item)
    session.commit()