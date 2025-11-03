# 🧹 Guide de Maintenance Évolutive - eBook Scene Packer v2

**Date** : 2025-11-01  
**Objectif** : Maintenir le projet toujours propre, cohérent et aligné avec la réalité

---

## 🎯 Principes Fondamentaux

### Règle d'Or
> **La documentation DOIT toujours refléter l'état actuel du code.**  
> **Tout fichier/documentation obsolète DOIT être supprimé ou mis à jour immédiatement.**

---

## 📋 Processus de Maintenance

### Quotidien (Automatique)

**Avant chaque commit** :
```bash
# Exécuter vérifications de base
./scripts/verify-consistency.sh

# S'assurer que :
# - DEVBOOK.md à jour si étape complétée
# - todolist.md à jour
# - Pas de code mort ajouté
# - Documentation cohérente
```

### Hebdomadaire (Manuel ou CI)

**Tous les lundis matin** :
```bash
# Audit complet de la documentation
./scripts/audit-documentation.sh

# Nettoyage automatique du code
./scripts/cleanup-code.sh

# Vérification de cohérence
./scripts/verify-consistency.sh
```

**Actions manuelles** :
- [ ] Vérifier et supprimer TODOs obsolètes
- [ ] Mettre à jour sections "À compléter" devenues complètes
- [ ] Vérifier liens entre documents

### Mensuel

**Premier lundi du mois** :
- [ ] Review complète de toute la documentation
- [ ] Supprimer fichiers/documentation obsolète (> 3 mois)
- [ ] Archiver PRDs deprecated dans `docs/PRDs/archive/`
- [ ] Mettre à jour roadmap si nécessaire
- [ ] Vérifier métriques de propreté (score > 90%)

---

## 🛠️ Scripts Disponibles

### 1. `scripts/audit-documentation.sh`

**Fonction** : Détecte les problèmes dans la documentation

**Vérifie** :
- Sections "À compléter" ou TODOs
- PRDs deprecated (> 1 mois)
- Fichiers très anciens (> 6 mois) marqués comme actifs
- Cohérence DEVBOOK ↔ Code (basique)
- Liens Markdown brisés

**Utilisation** :
```bash
./scripts/audit-documentation.sh
```

**Sortie** :
- ✅ Aucun problème
- ⚠️  Avertissements (à vérifier)
- ❌ Erreurs (action requise)

### 2. `scripts/cleanup-code.sh`

**Fonction** : Nettoie automatiquement le code

**Actions** :
- Supprime imports non utilisés (Python avec ruff)
- Détecte code mort (vulture)
- Signale console.log de debug
- Liste TODOs/FIXMEs restants

**Utilisation** :
```bash
./scripts/cleanup-code.sh
```

**Note** : Certaines actions nécessitent vérification manuelle.

### 3. `scripts/verify-consistency.sh`

**Fonction** : Vérifie cohérence entre documentation et code

**Vérifie** :
- DEVBOOK ↔ Code (phases terminées = code présent)
- PRDs ↔ Fonctionnalités (PRD approuvé = code existant)
- todolist ↔ DEVBOOK (étapes synchronisées)

**Utilisation** :
```bash
./scripts/verify-consistency.sh
```

**Sortie** :
- ✅ Cohérence vérifiée
- ❌ Erreurs de cohérence (action requise)

---

## 🚨 Alertes et Actions Correctives

### Alerte 1 : Documentation Obsolète

**Détection** :
- Fichier non modifié > 3 mois
- Référencé comme "actif" mais ancien

**Action** :
1. Vérifier si fonctionnalité toujours active
2. Si inactive : Marquer "Deprecated" ou supprimer
3. Mettre à jour références dans autres documents

### Alerte 2 : Code Mort

**Détection** :
- Fonctions non appelées
- Composants non utilisés
- Imports non utilisés

**Action** :
1. Vérifier si vraiment non utilisé
2. Si non utilisé : **Supprimer immédiatement**
3. Mettre à jour tests si nécessaire

### Alerte 3 : Liens Brisés

**Détection** :
- Liens Markdown pointant vers fichiers inexistants

**Action** :
1. Corriger lien si fichier déplacé
2. Supprimer référence si fichier supprimé
3. Mettre à jour document source

### Alerte 4 : Incohérence Documentation ↔ Code

**Détection** :
- Phase marquée "✅ Terminée" mais code absent
- PRD approuvé mais fonctionnalité non implémentée

**Action** :
1. Mettre à jour documentation OU
2. Implémenter code manquant
3. Vérifier après correction

---

## 📊 Métriques de Propreté

### Objectifs Cibles

- **0** fichier documentation obsolète (> 3 mois)
- **0** lien brisé dans documentation
- **< 5** TODOs/FIXMEs non documentés
- **0%** code mort (fonctions non appelées)
- **100%** cohérence DEVBOOK ↔ Code

### Score de Propreté

**Calcul** (à automatiser dans script) :
```
Score = 100 - (Erreurs × 10) - (Avertissements × 2)
```

**Seuil minimum** : 90%

---

## ✅ Checklist Avant Commit

### Documentation
- [ ] DEVBOOK.md à jour (si étape complétée)
- [ ] todolist.md à jour (tâches complétées)
- [ ] PRDs à jour (si fonctionnalité modifiée)
- [ ] Pas de sections "À compléter" ajoutées
- [ ] Liens vérifiés (pas de liens brisés)

### Code
- [ ] Pas de code commenté inutile
- [ ] Pas d'imports non utilisés
- [ ] Pas de console.log/print de debug
- [ ] Pas de TODOs/FIXMEs non documentés
- [ ] Code mort supprimé

### Tests
- [ ] Tests obsolètes supprimés
- [ ] Tests à jour après modification

---

## 🔄 Processus de Suppression

### Étape 1 : Identifier Fichier Obsolète

**Critères** :
- Fichier non référencé depuis > 3 mois
- Fonctionnalité abandonnée
- Documentation remplacée
- Phase/étape annulée

### Étape 2 : Vérifier Dépendances

```bash
# Chercher toutes les références
grep -r "nom-du-fichier" docs/ --include="*.md"
```

**Si références existent** :
- Mettre à jour références
- OU archiver fichier au lieu de supprimer

### Étape 3 : Supprimer ou Archiver

```bash
# Si références existent encore :
mv docs/fichier-obsolète.md docs/archive/fichier-obsolète.md

# Si aucune référence :
rm docs/fichier-obsolète.md

# Mettre à jour index/README si nécessaire
```

---

## 🔗 Intégration CI/CD (Recommandé)

### GitHub Actions Workflow

Créer `.github/workflows/maintenance-check.yml` :

```yaml
name: Maintenance Check

on:
  schedule:
    - cron: '0 9 * * 1'  # Tous les lundis 9h
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Audit Documentation
        run: ./scripts/audit-documentation.sh
        continue-on-error: true
      
      - name: Verify Consistency
        run: ./scripts/verify-consistency.sh
        continue-on-error: true
      
      - name: Cleanup Code (Check)
        run: ./scripts/cleanup-code.sh
        continue-on-error: true
      
      - name: Create Issue if Problems
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            // Créer issue pour maintenance requise
```

---

## 📚 Règles Cursor Associées

Cette maintenance est régie par la règle Cursor :
- **`.cursor/rules/maintenance-evolutive.mdc`** (alwaysApply: true)

**Voir aussi** :
- **Definition of Done** : `.cursor/rules/definition-of-done.mdc`
- **Standards Documentation** : `.cursor/rules/documentation-standards.mdc`

---

## 🎯 Exemples Concrets

### Exemple 1 : Phase Complétée

**Avant** :
```markdown
# Phase 1 : Infrastructure Core ⏳ Non commencée
```

**Après** :
```markdown
# Phase 1 : Infrastructure Core ✅ Terminée (2025-11-01)
```

**Actions** :
1. ✅ Marquer dans DEVBOOK.md
2. ✅ Marquer dans todolist.md
3. ✅ Vérifier que code existe
4. ✅ Exécuter `verify-consistency.sh`

### Exemple 2 : PRD Obsolète

**Détection** :
```bash
./scripts/audit-documentation.sh
# → PRD deprecated trouvé
```

**Action** :
1. Vérifier si vraiment obsolète
2. Si obsolète depuis > 1 mois :
   ```bash
   mv docs/PRDs/PRD-XXX.md docs/PRDs/archive/
   ```
3. Mettre à jour `docs/PRDs/README.md`

### Exemple 3 : Code Mort

**Détection** :
```bash
./scripts/cleanup-code.sh
# → Code mort détecté
```

**Action** :
1. Vérifier utilisation
2. Si non utilisé : Supprimer
3. Mettre à jour tests si nécessaire

---

**Dernière mise à jour** : 2025-11-01  
**Version** : 1.0.0

