# 📎 Guide d'Attachement des Règles et Docs Cursor

**Date** : 2025-11-01  
**Objectif** : Définir quelles règles Cursor et docs doivent être attachées aux prompts

---

## 🎯 Règles Cursor à Attacher

### ✅ Toujours Attacher (Always Apply)

Ces règles sont déjà configurées avec `alwaysApply: true` dans leur en-tête :

1. **`.cursor/rules/project-v2.mdc`** ✅
   - Règles générales projet v2
   - Architecture et conventions
   - **Toujours actif**

2. **`.cursor/rules/tdd-methodology.mdc`** ✅
   - Méthodologie TDD stricte
   - Cycle Red-Green-Refactor
   - **Toujours actif**

3. **`.cursor/rules/documentation-standards.mdc`** ✅
   - Standards de documentation
   - Formats PRD, DEVBOOK, TodoList
   - **Toujours actif**

4. **`.cursor/rules/testing-requirements.mdc`** ✅
   - Exigences de tests
   - Types de tests et coverage
   - **Toujours actif**

5. **`.cursor/rules/mcp-tools-usage.mdc`** ✅
   - Utilisation MCP Tools
   - Règles et exemples
   - **Toujours actif**

6. **`.cursor/rules/definition-of-done.mdc`** ⚠️ **CRITIQUE**
   - Règles strictes Definition of Done
   - **JAMAIS continuer si étape/phase non complétée à 100%**
   - Tests et coverage ≥90% obligatoires
   - **Toujours actif**

7. **`.cursor/rules/maintenance-evolutive.mdc`** ✅
   - Maintenance évolutive et nettoyage continu
   - Suppression documentation obsolète
   - Cohérence documentation ↔ code
   - **Toujours actif**

8. **`.cursor/rules/git-workflow.mdc`** ✅
   - Standards Git/GitHub workflow
   - Conventional Commits
   - GitHub Flow strategy
   - Semantic Versioning
   - **Toujours actif** (nouveau)

9. **`.cursor/rules/ui-ux-modern-2025.mdc`** ⭐ **NOUVEAU**
   - Règles complètes/totales/intégrales Design UX/UI Moderne 2025
   - Polices, onglets, bordures, icônes, espacements, couleurs
   - Accessibilité WCAG 2.2 AA
   - React 19 + TypeScript strict
   - Meilleures pratiques 2025 (vérifié Context7 MCP + recherche web)
   - **Toujours actif** (`alwaysApply: true`)

### 📋 Règles par Domaine Métier

**⚠️ CRITIQUE** : Ces règles doivent être attachées selon le contexte de développement :

9. **`.cursor/rules/templates-nfo.mdc`** ⚠️
   - Règles strictes Templates NFO
   - Conformité ASCII ≤ 80 colonnes
   - Template source : Règle eBOOK [2022]
   - **Quand** : Développement Étape 7 (Templates), génération NFO

10. **`.cursor/rules/rules-scene.mdc`** ⚠️
    - Intégration scenerules.org
    - Parsing règle eBOOK [2022] complète
    - Validation stricte contre règle
    - **Quand** : Développement Étape 3 (Règles), services RuleParser, RuleValidation, ScenerulesDownload

11. **`.cursor/rules/groups-scene.mdc`** ⚠️
    - Validation format Groups Scene
    - Regex format strict
    - Autocomplete groupes
    - **Quand** : Développement Étape 1 (Groupe), validation groupes

12. **`.cursor/rules/releases-packaging.mdc`** ⚠️
    - Conformité Releases packagées
    - Validation contre règle
    - Structure release conforme
    - **Quand** : Développement packaging, validation releases, Étape 8

13. **`.cursor/rules/users-roles-permissions.mdc`** ⚠️
    - Gestion Users, Roles, Permissions
    - Matrice READ/WRITE/MOD/DELETE
    - Logique permissions automatique
    - **Quand** : Développement PRD-005 (Users), PRD-006 (Roles), système permissions

14. **`.cursor/rules/configurations-api-destinations.mdc`** ⚠️
    - Configurations système
    - APIs externes (chiffrement Fernet)
    - Destinations FTP/SSH (chiffrement)
    - **Quand** : Développement PRD-007 (Configurations), gestion credentials

### 📋 Règles Globales (Optionnel - Déjà dans global.mdc)

Le fichier `.cursor/rules/global.mdc` contient déjà les règles générales ReactJS/Flask/MySQL et est toujours actif.

---

## 📚 Documentation à Référencer dans Prompts

### Essentiel (Toujours Mentionner)

1. **`docs/cdc.md`** - Cahier des charges
   - Vision, objectifs, fonctionnalités
   - **Quand** : Planification, compréhension requirements

2. **`docs/DEVBOOK.md`** - Suivi phases/étapes
   - État actuel du projet
   - **Quand** : Suivi progression, mise à jour statuts

3. **`docs/MCP_TOOLS_GUIDE.md`** - Guide MCP Tools ⭐
   - Utilisation MCP Tools
   - **Quand** : Tests E2E, recherche documentation, analyse

### Référence selon Contexte

4. **`docs/todolist.md`** - TodoList détaillée
   - **Quand** : Planification tâches, découpage

5. **`docs/PRDs/`** - Product Requirement Documents
   - **Quand** : Implémentation fonctionnalité spécifique

6. **`docs/BACKLOG_AGILE.md`** - Backlog Agile
   - **Quand** : Priorisation, User Stories

7. **`docs/TEST_PLAN.md`** - Plan de tests
   - **Quand** : Écriture tests, stratégie TDD

8. **`docs/RISKS_REGISTER.md`** - Registre risques
   - **Quand** : Identification risques, mitigation

9. **`docs/DEPLOYMENT_PLAN.md`** - Plan déploiement
   - **Quand** : Préparation déploiement

---

## 🔧 Configuration Recommandée pour Prompts

### Prompt Général de Développement

**Attacher** :
- Toutes les règles Cursor (déjà auto via `alwaysApply`)
- `docs/cdc.md` - Pour contexte projet
- `docs/DEVBOOK.md` - Pour état actuel
- `docs/MCP_TOOLS_GUIDE.md` - Pour utilisation MCP Tools
- `.cursor/rules/definition-of-done.mdc` ⚠️ **CRITIQUE**

**Exemple** :
```
@.cursor/rules/project-v2.mdc
@.cursor/rules/tdd-methodology.mdc
@.cursor/rules/definition-of-done.mdc
@.cursor/rules/mcp-tools-usage.mdc
@.cursor/rules/ui-ux-modern-2025.mdc  ⭐ Design UX/UI Moderne 2025
@docs/cdc.md
@docs/DEVBOOK.md
@docs/MCP_TOOLS_GUIDE.md
@docs/DESIGN_SYSTEM_UI_UX.md  ⭐ Design System complet
```

### Prompt pour Développement Frontend (React Components)

**Attacher** :
- Toutes les règles Cursor
- `docs/DESIGN_SYSTEM_UI_UX.md` ⭐ - Design System complet
- `.cursor/rules/ui-ux-modern-2025.mdc` ⭐ **CRITIQUE** - Règles complètes Design UX/UI Moderne 2025
- `.cursor/rules/design-system-ui-ux.mdc` - Règles Design System
- `.cursor/rules/ui-components-design.mdc` - Règles composants UI

**Exemple** :
```
@.cursor/rules/ui-ux-modern-2025.mdc  ⭐ NOUVEAU - Design UX/UI Moderne 2025
@.cursor/rules/design-system-ui-ux.mdc
@.cursor/rules/ui-components-design.mdc
@.cursor/rules/frontend-components.mdc
@docs/DESIGN_SYSTEM_UI_UX.md
@docs/PRDs/PRD-001-Interface-Admin.md
```

### Prompt pour Implémentation Fonctionnalité

**Attacher** :
- Toutes les règles Cursor
- `docs/cdc.md`
- `docs/PRDs/PRD-XXX-Nom-Fonctionnalite.md` (PRD spécifique)
- `docs/TEST_PLAN.md`

**Exemple** :
```
@.cursor/rules/project-v2.mdc
@.cursor/rules/tdd-methodology.mdc
@docs/cdc.md
@docs/PRDs/PRD-002-Nouvelle-Release.md
@docs/TEST_PLAN.md
```

### Prompt pour Tests E2E

**Attacher** :
- Toutes les règles Cursor
- `docs/MCP_TOOLS_GUIDE.md` ⭐ (Important pour Playwright MCP)
- `docs/TEST_PLAN.md`

**Exemple** :
```
@.cursor/rules/tdd-methodology.mdc
@.cursor/rules/testing-requirements.mdc
@.cursor/rules/mcp-tools-usage.mdc
@docs/MCP_TOOLS_GUIDE.md
@docs/TEST_PLAN.md
```

### Prompt pour Recherche Documentation

**Attacher** :
- `docs/MCP_TOOLS_GUIDE.md` ⭐

**Exemple** :
```
@docs/MCP_TOOLS_GUIDE.md
```

---

## ✅ Checklist Attachement

### Avant Prompt de Développement
- [ ] Règles Cursor actives (vérifier `alwaysApply: true`)
- [ ] `docs/cdc.md` attaché pour contexte
- [ ] `docs/DEVBOOK.md` attaché pour état actuel
- [ ] `docs/MCP_TOOLS_GUIDE.md` attaché si MCP Tools nécessaires

### Avant Prompt de Test
- [ ] `docs/MCP_TOOLS_GUIDE.md` attaché ⭐
- [ ] `docs/TEST_PLAN.md` attaché
- [ ] `.cursor/rules/tdd-methodology.mdc` vérifié

### Avant Prompt d'Implémentation
- [ ] PRD correspondant attaché
- [ ] `docs/cdc.md` attaché
- [ ] Règles Cursor actives

---

## 🔗 Résumé

### Règles Cursor (Auto-Actives)
- ✅ `project-v2.mdc` (alwaysApply)
- ✅ `tdd-methodology.mdc` (alwaysApply)
- ✅ `documentation-standards.mdc` (alwaysApply)
- ✅ `testing-requirements.mdc` (alwaysApply)
- ✅ `mcp-tools-usage.mdc` (alwaysApply)
- ⚠️ `definition-of-done.mdc` (alwaysApply) **CRITIQUE**
- ⭐ `ui-ux-modern-2025.mdc` **NOUVEAU** (alwaysApply) - Design UX/UI Moderne 2025 complet/total/intégral
  - 1 308 lignes de règles complètes
  - Vérifié Context7 MCP (React 19 + TypeScript)
  - Vérifié recherche web (tendances 2025)
  - Meilleures pratiques 2025 intégrées
- ✅ `maintenance-evolutive.mdc` (alwaysApply)
- ✅ `git-workflow.mdc` (alwaysApply)
- ✅ `global.mdc` (alwaysApply)

### Docs Essentiels à Mentionner
1. **`docs/MCP_TOOLS_GUIDE.md`** ⭐ - Très important pour MCP Tools
2. **`docs/DESIGN_SYSTEM_UI_UX.md`** ⭐ - Design System complet
3. **`docs/cdc.md`** - Contexte projet
4. **`docs/DEVBOOK.md`** - État actuel

### Docs selon Contexte
- `docs/todolist.md` - Planification
- `docs/PRDs/PRD-XXX.md` - Fonctionnalité spécifique
- `docs/TEST_PLAN.md` - Tests
- `docs/BACKLOG_AGILE.md` - Priorisation

---

**Dernière mise à jour** : 2025-11-01  
**Version** : 1.0.0

