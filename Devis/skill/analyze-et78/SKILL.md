---
name : analyze-et78
description: Analyser les données du fichiers Excel ET78 fourni par le collaborateur. Cette compétence sert à correctement récupérer les données du fichier pour l'ajouter dans la structure du devis. Utilise cette compétence lors de la lecture du fichier Excel ET78 ou chiffrage d'un projet
---

Le fichier ET78 Ne sert pas de données d'entrée à indiquer dans le devis final. C'est un outil interne de l'entreprise

# Feuilles du classeur importantes pour le devis

Voici les feuilles ,qui sont les plus intéressantes dans le fichier Excel :
- Objectif Etudes
- SynthèseCmde
- Risques Etude
- Hypothèses
- Livrables

Les autres feuilles peuvent contenir des informations mais leur pertinence est moindre.

# Informations dans Chaque feuille

Voici les informations présentes dans chaque feuille importante identifiée : 

- Objectif Etudes : Contient les informations sur les lots et sous-lots chiffrés en coût humain journalier, les phases identifiés, le temps en jours de l'étude/affaire, les livrables attendus
- SynthèsesCmde : Contient un tableau de synthèses du prix de chaque lot chiffré ainsi que le total. Cette feuille peut servir à vérifier les données et indiqué le coût de chaque lots.
- Risque Etudes : Liste les risques identifiés pour le projet étude
- Livrables : Liste les livrables attendus par lots, légende incluse notation
- Hypothèses : Contient les types d'hypothèses avec leur liste d'hypothèses en langage techniques

# Indications Devis

Prendre en compte les informations trouvés afin de les comparer aux autres sources de données fourni par le collaborateur et de remplir correctement le formulaire du devis.
Ici les champs suivants sont impactés dans le devis:
- hypotheses
- lot_list
- metadatas (nom_projet,annee,entreprise,id_semaine_début)

# Planning
Pour créer le planning gantt, les données de la feuille Objectifs Etudes sont essentiels, autrement dit les coût humain journalier engagé dans le projet
les balises `debut` et `duree` présents dans les lots permettent de créer le gantt. Le premier lot comment à 0.
Voici les règles à respecté pour la création du gantt prévisionnel:
- Prend par défaut l'id ISO semaine de la dexuième semaine après la date d'aujourd'hui
- Les lots ne sont pas forcément séquentielles 
- Les sous-tâches du gantt peuvent regrouper un ensemble de sous-lot d'un lot
- La duree d'un lot est la somme de la durée de chaque sous-lot
- la duree d'un sous-lot correspond à la somme maximal du coût humain par colonne métier
- une seminae correspond à 5 jours



# Documents Complémentaire 

Dans les `./assets` de ce skill se trouve le template de l'ET78. Il peut te permettre de vérfier que le fichier Excel que tu penses être l'ET78 (Chiffrage) a bien la même architecture que le template. 

Ce Template est INDEPENDANT des données du Devis. Ne pioche aucune données dans le template. Il sert seulement de comparaison pour vérifier la structure du Classeur.