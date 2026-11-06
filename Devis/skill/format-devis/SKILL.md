---
name : format-devis
description : Comparer la mise en forme textuel du devis JSON en cours avec d'autres devis exemples de projet précédant. Utilise cette compétence pour vérifier que les formulations, la densité, la qualité du texte et des informations du devis sont conformes à la manière de faire de l'entreprise.
---

# Skill : Contrôle de Conformité et Comparaison Stylistique des Devis

Objectif : Analyser un devis généré et le comparer systématiquement aux devis historiques (JSON) pour garantir l'uniformité stylistique, le mimétisme des tournures de phrases, et le respect strict des règles métier internes.

## 1. Prérequis (Inputs)
*   Le devis en cours (format JSON généré à partir de PresentationData).
*   Les devis de référence (fichiers JSON historiques validés servant de base d'apprentissage pour le style -> stockés dans `./assets` du skill).

## 2. Étape 1 : Vérification Structurelle Stricte (Garde-fous métiers)
L'IA doit d'abord vérifier que le devis respecte les contraintes imposées par les descriptions des champs :
*   Données d'entrée (donnees_entree) : Vérifier que le fichier "ET78" n'est pas inclus dans la liste.
*   Hypothèses (hypotheses) : S'assurer qu'elles couvrent l'entièreté du cahier des charges et qu'elles sont regroupées (idéalement : électronique, mécanique, logiciel).
*   Lots (lots_list) : 
    *   Vérifier que la réunion de lancement n'est pas incluse dans les lots.
    *   S'assurer que le champ debut du premier lot commence ABSOLUMENT à 0.
    *   Vérifier que la échanges clients ne sont pas inclus dans les documents (données d'entrée)
*   Images (logo_client) : Vérifier qu'il n'y a pas de format Base64 dans les prompts.
*   Documents (DocumentsLot) : Vérifier que les listes ne dépassent pas 5 documents chacune et privilégient les acronymes.

## 3. Étape 2 : Comparaison et Calibrage des Tournures de Phrases (Stylistique)
Cette étape est cruciale. L'IA doit extraire les "patterns" rédactionnels des exemples historiques et forcer le brouillon à s'y conformer.

*   Critère A - Mimétisme des formulations :
    *   Extraire les verbes d'action et la structure syntaxique utilisés dans les descriptions de lots des historiques.
    *   Action : Comparer ligne par ligne les tournures du brouillon avec celles des exemples. Si le brouillon utilise un style descriptif (ex: "Nous allons faire des tests") alors que l'historique utilise un style formel et nominal (ex: "Réalisation des campagnes d'essais"), l'IA doit réécrire la phrase.
*   Critère B - Le Besoin (Besoin) : 
    *   Le champ Role_TAME explique-t-il clairement en une ou deux phrases pourquoi le client a fait appel à TAME-CARE, en utilisant le même niveau de vulgarisation que les exemples ?
    *   Le Besoin décrit-il les grosses étapes aussi simplement que dans les JSON de référence ?
*   Critère C - Détails des Lots (details_lot) : 
    *   La description inclut-elle bien "Objectif", "Activités", et "Hors périmètre" ?
    *   La densité technique et la longueur des puces doivent être identiques à la moyenne observée dans les devis de référence.

# Contrôles bloquants

La validation échoue si au moins une des situations suivantes est détectée :

## Hypothèses
- `List_Hypotheses` est un paragraphe continu ;
- aucune liste à puces n’est présente ;
- les hypothèses ne sont pas regroupées par domaine ;
- une hypothèse n’est rattachable à aucune source ;
- un point à confirmer est présenté comme une hypothèse validée.

## Lots
- une section Objectif, Activités ou Hors périmètre est absente ;
- les sections ne contiennent pas de listes ;
- une activité n’apparaît pas dans l’ET78 ou dans une source explicite ;
- une réunion de lancement est créée comme lot autonome ;
- le premier lot ne commence pas à zéro.

## Documents
Pour chaque donnée d’entrée et chaque livrable :
- identifier le document source ;
- identifier le responsable de production ;
- identifier l’approbateur ;
- identifier le lot de création ;
- vérifier la couleur calculée.


Règles :
- un document TAME-CARE réutilisé comme entrée reste orange ;
- un document co-construit sans responsabilité dominante est gris ;
- la présence dans `Donnees_entree` n’implique jamais la couleur bleue ;
- l’ET78 ne doit jamais apparaître dans les données client.

## Rapport de contrôle

Retourner un rapport structuré :

- Statut global : CONFORME ou NON CONFORME
- Erreurs bloquantes
- Avertissements
- Corrections appliquées
- Matrice documentaire :
  document | origine | client | TAME-CARE | couleur | justification

Le devis ne peut être transmis au skill de génération que si le statut
global est CONFORME.Les exemples historiques servent uniquement à calibrer le style.
Ils ne peuvent jamais remplacer, contredire ou assouplir les règles
structurelles de la classe PresentationData.