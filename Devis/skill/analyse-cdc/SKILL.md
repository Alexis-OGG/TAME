---
name: analyse-cdc
description: Analyse les informations du cahier des charges afin d'identifier les informations pertinentes dans la création du devis (JSON). Appelle Cette compétence lors de l'analyse du cahier des charges pour la qualification du projet
---

Si le Cahier des charges est fourni par le collaborateur. Il DOIT être indiqué danse les données d'entrées dans le devis

# Informations Importantes

Les données à identifiées ci-dessous ne vont pas toutes servir dans le devis. Mais elle aide pour amener du contexte et vérifier que le devis est conforme au besoin et l'attente du client


## 1. Méta-données & Contexte
* Nom de l'entreprise : [Nom du client]
* Secteur médical cible : [ex: Dispositif implantable, Diagnostic in-vitro, Équipement hospitalier, Wearable santé]
* Année : [ex: 2027]
* Interlocuteurs :
  * Décideur (Budget) : [Nom & Fonction]
  * Référent Technique/Ingénierie : [Nom & Fonction]
  * Responsable Qualité/Réglementaire : [Nom & Fonction]

## 2. État d'Avancement
* Stade de développement actuel : 
  * [ ] Idée / Preuve de concept (POC) sur breadboard
  * [ ] Schématique existante
  * [ ] Routage (PCB layout) réalisé
  * [ ] Prototype fonctionnel (V1) à optimiser/industrialiser
  * [ ] Refonte d'une carte obsolète
* Existant technique : [Lister les fichiers disponibles : Fichiers Gerbers, BOM provisoire, Code source firmware (C/C++), CAO mécanique du boîtier]

Cela permet de vérifier les phases du projet restant à traiter et de comparer avec les autres sources de données les phases identifiées

## 3. Expression du Besoin (Matériel & Logiciel)
* Description du dispositif : [À quoi sert l'appareil ?]
* Fonctionnalités matérielles (Hardware) critiques :
  * *Capteurs/Acquisition :* [ex: ECG, SpO2, Température, Pression]
  * *Connectivité :* [ex: BLE, Wi-Fi, LoRa, Filaire USB/Ethernet]
  * *Alimentation :* [ex: Sur secteur médical, Batterie Li-Ion, Autonomie visée]
  * *IHM (Interface Homme-Machine) :* [ex: Écran tactile, LEDs, Boutons d'urgence]
* Avancement du Besoin 
* Fonctionnalités logicielles (Firmware/Software) :
  * *Traitement :* [ex: Filtrage de signaux, algorithmes spécifiques]
  * *Stockage/Transmission :* [ex: Enregistrement sur SD, Envoi vers cloud sécurisé]

## 4. Normes, Sécurité & Contraintes Médicales
* Classification du dispositif médical (MDR) : [Classe I, IIa, IIb, ou III]
* Normes requises pour le développement :
  * [ ] ISO 13485 (Système de management de la qualité)
  * [ ] IEC 60601-1 (Sécurité de base et performances essentielles)
  * [ ] IEC 60601-1-2 (Compatibilité Électromagnétique - CEM)
  * [ ] IEC 62304 (Processus de cycle de vie des logiciels médicaux)
  * [ ] Autre : [ex: ISO 10993 pour la biocompatibilité si en contact avec le patient]
* Sécurité des données :
  * Exigences RGPD ou HIPAA (chiffrement des données de santé).
* Contraintes d'environnement :
  * [ex: Stérilisation (Autoclave, Oxyde d'éthylène), Étanchéité (IP67/IP68), Température de fonctionnement]

## 5. Livrables & Déploiement
* Livrables de conception (Dossier de fabrication) :
  * Schémas électroniques (fichiers sources).
  * Fichiers de fabrication (Gerbers, ODB++, Pick & Place).
  * Nomenclature détaillée (BOM) avec gestion de l'obsolescence.
* Livrables physiques :
  * Nombre de prototypes (V1 / V2) : [X] cartes assemblées.
  * Bancs de test (Test Jigs) pour la production.
* Livrables logiciels & documentaires :
  * Code source du firmware commenté.
  * Dossier de conception (nécessaire pour le marquage CE/FDA).

## 6. Risques & Dépendances
* Risques supply chain : [ex: Pénurie sur le microcontrôleur choisi, proposer des alternatives (second source)]
* Risques réglementaires : [ex: Retards potentiels lors des tests CEM/Sécurité en laboratoire externe]
* Dépendances : [ex: Intégration dans le boîtier mécanique développé par un autre prestataire]
* Délais impératifs : [ex: Dépôt du dossier FDA prévu pour Mars 2027]


