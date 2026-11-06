---
name: show-gantt-planning
description: Génère un Gantt Prévisionnel du projet à partir des données du devis. Cette compétence est à utilisé OBLIGATOIREMENT lors de la révision avec le collaborateur du devis en cours. Cela permet de vérifier visuellement que le planning est validé.
---

# Condition préalable obligatoire

Le skill `show-gantt-planning` peut être exposé par le catalogue de skills sans que son emplacement physique soit déductible de son nom.

## 1. Résolution stricte et persistante du répertoire

Utiliser exclusivement le mécanisme de chargement ou de matérialisation des skills fourni par l'environnement afin d'obtenir le répertoire physique exécutable du skill `show-gantt-planning`.

Ne jamais déduire ou supposer ce chemin à partir du nom logique du skill. Ne pas supposer qu'il se trouve dans `/home/oai/skills/...` et ne pas effectuer de recherche récursive avec `find`.

**Attention, règle stateless :** les variables d'environnement définies avec `export` ne persistent pas entre les exécutions. Une fois le chemin physique obtenu, le mémoriser et l'injecter manuellement sous forme de chaîne de caractères, par exemple `SKILL_DIR="/chemin/absolu/resolu"`, au début de chaque bloc Bash exécuté.

Si le mécanisme de chargement ou de matérialisation ne retourne aucun chemin physique exécutable, arrêter immédiatement l'exécution et indiquer précisément que le skill est exposé dans le catalogue, mais que ses ressources exécutables n'ont pas été matérialisées dans le conteneur. Ne jamais remplacer le chemin manquant par un chemin supposé.

## 2. Validation obligatoire du JSON 

Le JSON planning doit respecter le modèle `PresentationData` défini dans le script `classes.py` du répertoire du skill.

# Exécution obligatoire

Après validation interne d'une proposition révisable avec le collaborateur, effectué les tâches suivantes afin de proposer un gantt prévisionnel :

## 1. Écrire le JSON planning

Écrire exactement le JSON planning dans :

```text
/mnt/data/devis_gantt.json
```

Le fichier doit contenir uniquement du JSON valide, sans bloc Markdown, sans balises HTML et sans commentaires.


## 2. Vérification et exécution en un seul bloc

Pour éviter toute perte de contexte, exécuter les vérifications des ressources et la génération dans un seul et même bloc Bash.

Exécuter le bloc suivant avec `container.exec`, en remplaçant `<CHEMIN_PHYSIQUE_RESOLU>` par le chemin absolu obtenu à l'étape 1.


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

# A. Vérification des ressources communes
test -s /mnt/data/devis_gantt.json || {
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

test -f "$SKILL_DIR/assets/DEV_Template.pptx" || {
  echo "Erreur: Template introuvable"
  exit 1
}

cd /mnt/data

# D. Exécution du générateur pour une autre génération
python "$SKILL_DIR/scripts/main.py" \
  --input-json /mnt/data/devis_gantt.json \
  --output /mnt/data/planning.pptx

# E. Vérification post-génération
test -s /mnt/data/planning.pptx || {
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
- ne pas créer de générateur PowerPoint alternatif ;
- ne pas continuer avec une version simplifiée de la présentation.

## 5. Retour du fichier

Si l'exécution réussit, retourner au collaborateur le fichier suivant :

```text
/mnt/data/planning.pptx
```
