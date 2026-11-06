---
name: create-devis-pptx
description: Génère une présentation PowerPoint à partir d'une instance JSON validée de PresentationData. Utilise ce skill lorsque tu dois générer le PPTX du devis.
---

# Condition préalable obligatoire

Le skill `create-devis-pptx` peut être exposé par le catalogue de skills sans que son emplacement physique soit déductible de son nom.

## 1. Résolution stricte et persistante du répertoire

Utiliser exclusivement le mécanisme de chargement ou de matérialisation des skills fourni par l'environnement afin d'obtenir le répertoire physique exécutable du skill `create-devis-pptx`.

Ne jamais déduire ou supposer ce chemin à partir du nom logique du skill. Ne pas supposer qu'il se trouve dans `/home/oai/skills/...` et ne pas effectuer de recherche récursive avec `find`.

**Attention, règle stateless :** les variables d'environnement définies avec `export` ne persistent pas entre les exécutions. Une fois le chemin physique obtenu, le mémoriser et l'injecter manuellement sous forme de chaîne de caractères, par exemple `SKILL_DIR="/chemin/absolu/resolu"`, au début de chaque bloc Bash exécuté.

Si le mécanisme de chargement ou de matérialisation ne retourne aucun chemin physique exécutable, arrêter immédiatement l'exécution et indiquer précisément que le skill est exposé dans le catalogue, mais que ses ressources exécutables n'ont pas été matérialisées dans le conteneur. Ne jamais remplacer le chemin manquant par un chemin supposé.

## 2. Validation obligatoire du JSON

Ne pas générer la présentation tant que le collaborateur n'a pas explicitement validé le JSON final.

Le JSON validé doit respecter le modèle `PresentationData` défini dans le script `classes.py` du répertoire du skill.

# Exécution obligatoire

Après validation explicite du JSON par le collaborateur, réaliser les actions suivantes.

## 1. Écrire le JSON validé

Écrire exactement le JSON validé dans :

```text
/mnt/data/devis_valide.json
```

Le fichier doit contenir uniquement du JSON valide, sans bloc Markdown, sans balises HTML et sans commentaires.

## 2. Génération d'une image d'illustration

Si et seulement si l'utilisateur génère le devis pour la première fois, générer 1 image et la découper en 6 images dans :

```text
/mnt/data/img/
```

Sinon, passer à l'étape 3 et utiliser le mode « autre génération ».

Dimensions attendues :

- 1re image : 8 cm de hauteur sur 34 cm de largeur ;
- 2e et 3e images : 14 cm de hauteur sur 34 cm de largeur ;
- 4e, 5e et 6e images : 19 cm de hauteur sur 9 cm de largeur.

Chaque image doit illustrer un sujet étroitement lié au projet ou au devis.

Nommer chaque image selon le format `img{n°}.png`, par exemple `img1.png`.

## 3. Vérification et exécution en un seul bloc

Pour éviter toute perte de contexte, exécuter les vérifications des ressources et la génération dans un seul et même bloc Bash.

Exécuter le bloc suivant avec `container.exec`, en remplaçant `<CHEMIN_PHYSIQUE_RESOLU>` par le chemin absolu obtenu à l'étape 1.

Définir `PREMIERE_GENERATION=1` pour une première génération et `PREMIERE_GENERATION=0` pour une autre génération. Un seul des deux modes doit être exécuté.

```bash
#!/bin/bash
set -e

# 1. AUTO-DÉCOUVERTE DYNAMIQUE DU CHEMIN
echo "Recherche du répertoire du skill..."
SKILL_DIR=$(ls -d /home/oai/skills/appCatalog/*/create-devis-pptx 2>/dev/null | head -n 1)

if [ -z "$SKILL_DIR" ]; then
  echo "Erreur: Impossible de localiser dynamiquement le répertoire physique du skill."
  exit 1
fi
echo "Skill trouvé dans : $SKILL_DIR"

# 2. DÉFINITION DU MODE DE GÉNÉRATION (L'IA peut modifier 1 en 0 pour une regénération)
PREMIERE_GENERATION=1

# A. Vérification des ressources communes
test -s /mnt/data/devis_valide.json || {
  echo "Erreur: JSON invalide ou introuvable"
  exit 1
}

test -n "$SKILL_DIR" || {
  echo "Erreur: SKILL_DIR non défini"
  exit 1
}

test -f "$SKILL_DIR/SKILL.md" || {
  echo "Erreur: SKILL.md introuvable"
  exit 1
}

test -f "$SKILL_DIR/scripts/main.py" || {
  echo "Erreur: main.py introuvable"
  exit 1
}

test -f "$SKILL_DIR/scripts/classes.py" || {
  echo "Erreur: classes.py introuvable"
  exit 1
}

test -f "$SKILL_DIR/assets/DEV_Template.pptx" || {
  echo "Erreur: Template introuvable"
  exit 1
}

test -d "$SKILL_DIR/assets/img" || {
  echo "Erreur: Dossier img introuvable"
  exit 1
}

cd /mnt/data

if [ "$PREMIERE_GENERATION" -eq 1 ]; then
  # B. Vérification des images de la première génération
  test -d /mnt/data/img || {
    echo "Erreur: Dossier /mnt/data/img introuvable"
    exit 1
  }

  for numero in 1 2 3 4 5 6; do
    test -s "/mnt/data/img/img${numero}.png" || {
      echo "Erreur: /mnt/data/img/img${numero}.png introuvable ou vide"
      exit 1
    }
  done

  # C. Exécution du générateur pour la première génération
  python "$SKILL_DIR/scripts/main.py" \
    --input-json /mnt/data/devis_valide.json \
    --img1 /mnt/data/img/img1.png \
    --img2 /mnt/data/img/img2.png \
    --img3 /mnt/data/img/img3.png \
    --img4 /mnt/data/img/img4.png \
    --img5 /mnt/data/img/img5.png \
    --img6 /mnt/data/img/img6.png \
    --output /mnt/data/devis.pptx
else
  # D. Exécution du générateur pour une autre génération
  python "$SKILL_DIR/scripts/main.py" \
    --input-json /mnt/data/devis_valide.json \
    --output /mnt/data/devis.pptx
fi

# E. Vérification post-génération
test -s /mnt/data/devis.pptx || {
  echo "Erreur: Le fichier PowerPoint n'a pas été généré correctement"
  exit 1
}

echo "Génération réussie avec succès."
```

## 4. Contraintes strictes en cas d'erreur

Si l'exécution du bloc précédent échoue avec un code de sortie différent de `0` :

- arrêter immédiatement l'exécution ;
- indiquer précisément la ressource manquante ou l'erreur renvoyée par le script ;
- ne pas reconstruire les scripts à partir des ressources ;
- ne pas recopier manuellement le contenu de `main.py` ;
- ne pas extraire les images du modèle PowerPoint ;
- ne pas créer de générateur PowerPoint alternatif ;
- ne pas continuer avec une version simplifiée de la présentation.

## 5. Retour du fichier

Si l'exécution réussit, retourner au collaborateur le fichier suivant :

```text
/mnt/data/devis.pptx
```
