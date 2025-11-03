# 📋 Analyse Couverture Règles par Répertoire/Domaine

**Date** : 2025-11-01  
**Objectif** : Vérifier que chaque domaine du projet a ses règles spécifiques

---

## 🎯 Vue d'Ensemble

Cet document analyse la couverture des règles Cursor pour chaque domaine/repertoire du projet et identifie les manques.

---

## 📊 État Actuel des Règles

### ✅ Règles Existant (14 fichiers)

| Règle | Domaine | Statut | Couverture |
|-------|---------|--------|------------|
| `templates-nfo.mdc` | Templates NFO | ✅ | COMPLET |
| `rules-scene.mdc` | Rules Scene | ✅ | COMPLET |
| `groups-scene.mdc` | Groups Scene | ✅ | COMPLET |
| `releases-packaging.mdc` | Releases & Packaging | ✅ | COMPLET |
| `users-roles-permissions.mdc` | Users, Roles, Permissions | ✅ | COMPLET |
| `configurations-api-destinations.mdc` | Configurations, APIs, Destinations | ✅ | COMPLET |
| `definition-of-done.mdc` | Definition of Done | ✅ | COMPLET |
| `tdd-methodology.mdc` | TDD | ✅ | COMPLET |
| `testing-requirements.mdc` | Tests | ✅ | COMPLET |
| `documentation-standards.mdc` | Documentation | ✅ | COMPLET |
| `mcp-tools-usage.mdc` | MCP Tools | ✅ | COMPLET |
| `git-workflow.mdc` | Git/GitHub | ✅ | COMPLET |
| `maintenance-evolutive.mdc` | Maintenance | ✅ | COMPLET |
| `project-v2.mdc` | Projet général | ✅ | COMPLET |

---

## 🔍 Analyse par Répertoire/Domaine

### 1. `/web/models/` - Modèles ORM

**Règle** : ❌ MANQUANTE

**Domaine** : Modèles SQLAlchemy (User, Role, Permission, Group, Release, Job, Rule, etc.)

**Règles Nécessaires** :
- ✅ Structure modèles (colonnes, types, contraintes)
- ✅ Relations (many-to-many, one-to-many)
- ✅ Indexes et performance
- ✅ Validation des champs
- ✅ Méthodes utilitaires (`to_dict()`, `from_dict()`, etc.)
- ✅ Contraintes base de données (UNIQUE, FOREIGN KEY, etc.)

**Action** : Créer `.cursor/rules/models-orm.mdc`

---

### 2. `/web/services/` - Services Métier

**Règle** : ❌ MANQUANTE

**Domaine** : Services métier (PackagingService, MetadataService, RuleService, etc.)

**Règles Nécessaires** :
- ✅ Architecture services (séparation logique)
- ✅ Interfaces claires (méthodes publiques)
- ✅ Gestion erreurs (exceptions spécifiques)
- ✅ Logging (traçabilité)
- ✅ Tests (mock dependencies)
- ✅ Services critiques : `RuleParserService`, `RuleValidationService`, `ScenerulesDownloadService`

**Action** : Créer `.cursor/rules/services-architecture.mdc`

---

### 3. `/web/blueprints/` - Blueprints Flask

**Règle** : ❌ MANQUANTE

**Domaine** : Endpoints API Flask (auth, dashboard, wizard, releases, rules, users, roles, config)

**Règles Nécessaires** :
- ✅ Structure blueprints modulaires
- ✅ Routes RESTful
- ✅ Validation inputs (Marshmallow schemas)
- ✅ Gestion erreurs (formats standardisés)
- ✅ Authentification JWT
- ✅ Permissions granulaires (READ/WRITE/MOD/DELETE)
- ✅ Pagination, filtrage, tri

**Action** : Créer `.cursor/rules/blueprints-api.mdc`

---

### 4. `/web/utils/` - Utilitaires

**Règle** : ❌ MANQUANTE

**Domaine** : Utilitaires (crypto, validators, helpers)

**Règles Nécessaires** :
- ✅ Chiffrement Fernet (credentials)
- ✅ Validateurs (formats, regex)
- ✅ Helpers réutilisables
- ✅ Pas de logique métier dans utils

**Action** : Créer `.cursor/rules/utils-helpers.mdc`

---

### 5. **Jobs** - Gestion Jobs

**Règle** : ❌ MANQUANTE

**Domaine** : Jobs de packaging (statuts, logs, progression)

**Règles Nécessaires** :
- ✅ Statuts jobs (`draft`, `running`, `completed`, `failed`, `cancelled`)
- ✅ Logs structurés (timestamps, niveau, message)
- ✅ Progression tracking (pourcentage, étape)
- ✅ Jobs asynchrones (celery ou threading)
- ✅ Cleanup jobs obsolètes
- ✅ Persistance état job (reprise après crash)

**Action** : Créer `.cursor/rules/jobs-management.mdc`

---

### 6. **Metadata Extraction** - Extraction Métadonnées

**Règle** : ❌ MANQUANTE

**Domaine** : Extraction métadonnées fichiers (Étape 5)

**Règles Nécessaires** :
- ✅ MediaInfo pour tous types
- ✅ Métadonnées EPUB/PDF/MOBI (auteur, titre, ISBN, etc.)
- ✅ Extraction maximale possible
- ✅ Format standardisé (JSON)
- ✅ Barre progression extraction
- ✅ Gestion erreurs extraction

**Action** : Créer `.cursor/rules/metadata-extraction.mdc`

---

### 7. **Enrichissement APIs** - APIs Externes

**Règle** : ❌ MANQUANTE

**Domaine** : Enrichissement métadonnées via APIs externes (Étape 6)

**Règles Nécessaires** :
- ✅ APIs configurables par type release
- ✅ Ordre priorité si plusieurs sources
- ✅ Validation manuelle obligatoire
- ✅ Prévisualisation résultats APIs
- ✅ Traçabilité sources
- ✅ Gestion rate limiting
- ✅ Gestion erreurs APIs (timeout, erreurs HTTP)

**Action** : Créer `.cursor/rules/enrichment-apis.mdc`

---

### 8. **Wizard** - Navigation et État

**Règle** : ❌ MANQUANTE

**Domaine** : Wizard 9 étapes (navigation, état, persistance)

**Règles Nécessaires** :
- ✅ Navigation entre étapes (Previous/Next)
- ✅ Validation avant passage étape suivante
- ✅ Sauvegarde progression (localStorage + backend draft)
- ✅ Reprise wizard (restauration état)
- ✅ Indicateur progression (Étape X/9)
- ✅ État wizard (WizardContext React)

**Action** : Créer `.cursor/rules/wizard-navigation.mdc`

---

### 9. **Dashboard** - Dashboard

**Règle** : ❌ MANQUANTE

**Domaine** : Dashboard avec statistiques et navigation

**Règles Nécessaires** :
- ✅ Statistiques (nombre releases, jobs, utilisateurs)
- ✅ Jobs drafts (liste, reprise)
- ✅ Navigation rapide
- ✅ Informations utilisateur connecté
- ✅ Thème jour/nuit (toggle)

**Action** : Créer `.cursor/rules/dashboard.mdc`

---

### 10. **File Upload** - Upload Fichiers

**Règle** : ❌ MANQUANTE

**Domaine** : Upload fichiers (local, distant, Étape 4)

**Règles Nécessaires** :
- ✅ Upload local (drag & drop, sélecteur)
- ✅ URL distante (HTTP/HTTPS/FTP)
- ✅ Validation format fichier (selon type release)
- ✅ Validation taille (max 20GB)
- ✅ Barre progression upload/téléchargement
- ✅ Gestion erreurs upload

**Action** : Créer `.cursor/rules/file-upload.mdc`

---

### 11. **Frontend Components** - Composants React

**Règle** : ❌ MANQUANTE

**Domaine** : Composants React (structure, réutilisabilité)

**Règles Nécessaires** :
- ✅ Structure modulaire (common, wizard, releases, rules)
- ✅ TypeScript strict
- ✅ Props typées
- ✅ Composants réutilisables
- ✅ Hooks custom
- ✅ Context API pour état global
- ✅ Responsive (Bootstrap 5)

**Action** : Créer `.cursor/rules/frontend-components.mdc`

---

## ✅ Domaines Couverts

### Templates NFO
- ✅ Règle : `templates-nfo.mdc`
- ✅ Conformité ASCII ≤ 80 colonnes
- ✅ Template source : Règle eBOOK [2022]
- ✅ Placeholders, conditionnelles, fonctions

### Rules Scene
- ✅ Règle : `rules-scene.mdc`
- ✅ Intégration scenerules.org
- ✅ Parsing complet règle eBOOK [2022]
- ✅ Validation stricte

### Groups Scene
- ✅ Règle : `groups-scene.mdc`
- ✅ Format strict (regex)
- ✅ Autocomplete

### Releases & Packaging
- ✅ Règle : `releases-packaging.mdc`
- ✅ Conformité règle Scene
- ✅ Validation stricte

### Users, Roles, Permissions
- ✅ Règle : `users-roles-permissions.mdc`
- ✅ Matrice permissions
- ✅ Logique automatique

### Configurations, APIs, Destinations
- ✅ Règle : `configurations-api-destinations.mdc`
- ✅ Chiffrement Fernet
- ✅ Test connexion

---

## 🚨 Domaines Manquants

| Domaine | Priorité | Action |
|---------|----------|--------|
| **Models ORM** | ⚠️ CRITIQUE | Créer `models-orm.mdc` |
| **Services Architecture** | ⚠️ CRITIQUE | Créer `services-architecture.mdc` |
| **Blueprints API** | ⚠️ CRITIQUE | Créer `blueprints-api.mdc` |
| **Jobs Management** | ⚠️ CRITIQUE | Créer `jobs-management.mdc` |
| **Metadata Extraction** | ⚠️ CRITIQUE | Créer `metadata-extraction.mdc` |
| **Enrichissement APIs** | ⚠️ CRITIQUE | Créer `enrichment-apis.mdc` |
| **Wizard Navigation** | ⚠️ CRITIQUE | Créer `wizard-navigation.mdc` |
| **Dashboard** | ⚠️ CRITIQUE | Créer `dashboard.mdc` |
| **File Upload** | ⚠️ CRITIQUE | Créer `file-upload.mdc` |
| **Frontend Components** | ⚠️ CRITIQUE | Créer `frontend-components.mdc` |
| **Utils Helpers** | ⚠️ IMPORTANT | Créer `utils-helpers.mdc` |

---

## 📋 Plan d'Action

### Phase 1 : Règles Critiques Backend
1. ✅ `models-orm.mdc` - Modèles SQLAlchemy
2. ✅ `services-architecture.mdc` - Services métier
3. ✅ `blueprints-api.mdc` - Endpoints API

### Phase 2 : Règles Critiques Fonctionnelles
4. ✅ `jobs-management.mdc` - Gestion jobs
5. ✅ `metadata-extraction.mdc` - Extraction métadonnées
6. ✅ `enrichment-apis.mdc` - APIs externes
7. ✅ `wizard-navigation.mdc` - Navigation wizard

### Phase 3 : Règles Critiques Frontend
8. ✅ `dashboard.mdc` - Dashboard
9. ✅ `file-upload.mdc` - Upload fichiers
10. ✅ `frontend-components.mdc` - Composants React

### Phase 4 : Règles Complémentaires
11. ✅ `utils-helpers.mdc` - Utilitaires

---

## 🎯 Objectif Final

**100% de couverture** : Chaque domaine/repertoire du projet doit avoir ses règles spécifiques pour garantir :
- ✅ Respect de la logique métier
- ✅ Cohérence architecture
- ✅ Conformité standards Scene
- ✅ Qualité code

---

**Dernière mise à jour** : 2025-11-01

