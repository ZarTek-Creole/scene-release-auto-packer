# 📋 Règles Cursor par Domaine Métier - eBook Scene Packer v2

**Date** : 2025-11-01  
**Objectif** : Référence complète des règles Cursor spécifiques à chaque domaine du projet

---

## 🎯 Vue d'Ensemble

Ce document liste toutes les règles Cursor spécifiques à chaque domaine métier du projet, permettant un respect optimal de la logique et des objectifs pour chaque aspect du système.

---

## 📁 Règles par Domaine

### 1. Templates NFO
**Fichier** : `.cursor/rules/templates-nfo.mdc`

**Domaine** : Templates NFO, génération NFO, prévisualisation

**Règles principales** :
- ✅ Format ASCII ≤ 80 colonnes obligatoire
- ✅ Template source : Règle eBOOK [2022] (priorité)
- ✅ Placeholders : `{{variable}}`, conditionnelles `{% if %}`
- ✅ Validation largeur avant sauvegarde
- ✅ NFO Viewer monospace UTF-8

**Quand utiliser** :
- Développement Étape 7 (Templates)
- Génération NFO lors packaging
- Validation templates

**Références** :
- `docs/PRDs/PRD-002-Nouvelle-Release.md` (Étape 7)
- `docs/SCENERULES_INTEGRATION.md`
- `docs/DATABASE_ERD.md` (table `templates`)

---

### 2. Rules Scene
**Fichier** : `.cursor/rules/rules-scene.mdc`

**Domaine** : Rules Scene, intégration scenerules.org, validation

**Règles principales** :
- ⚠️ **CRITIQUE** : Connaissance TOTALE et INTÉGRALE scenerules.org
- ✅ Règle eBOOK [2022] PRIORITÉ ABSOLUE
- ✅ Parsing complet (formats, template, contraintes)
- ✅ Validation stricte contre règle
- ✅ Services : `RuleParserService`, `RuleValidationService`, `ScenerulesDownloadService`

**Quand utiliser** :
- Développement Étape 3 (Sélection Règle)
- Services backend parsing/validation
- Téléchargement scenerules.org

**Références** :
- `docs/SCENERULES_INTEGRATION.md` ⭐
- `docs/PRDs/PRD-002-Nouvelle-Release.md` (Étape 3)
- `docs/PRDs/PRD-004-Rules.md`
- [scenerules.org](https://scenerules.org/)

---

### 3. Groups Scene
**Fichier** : `.cursor/rules/groups-scene.mdc`

**Domaine** : Groups Scene, validation format

**Règles principales** :
- ✅ Format strict : Majuscules + chiffres uniquement
- ✅ Regex : `^[A-Z0-9]{2,100}$`
- ✅ Normalisation automatique (uppercase)
- ✅ Autocomplete groupes existants
- ✅ Validation temps réel UI

**Quand utiliser** :
- Développement Étape 1 (Groupe)
- Validation format groupes
- Autocomplete UI

**Références** :
- `docs/PRDs/PRD-002-Nouvelle-Release.md` (Étape 1)
- `docs/DATABASE_ERD.md` (tables `groups`, `user_groups`)
- `docs/API_REFERENCE.md` (endpoints groups)

---

### 4. Releases & Packaging
**Fichier** : `.cursor/rules/releases-packaging.mdc`

**Domaine** : Releases packagées, conformité Scene

**Règles principales** :
- ⚠️ **CRITIQUE** : Conformité absolue avec règle Scene
- ✅ Validation contre règle à toutes étapes
- ✅ Structure release conforme spécifications
- ✅ Nommage strict selon contraintes règle
- ✅ NFO généré selon template règle
- ✅ Formats acceptés selon règle (EBOOK priorité)

**Quand utiliser** :
- Développement packaging (Étape 8)
- Validation releases
- Structure release
- Nommage fichiers

**Références** :
- `docs/SCENERULES_INTEGRATION.md` ⭐
- `docs/PRDs/PRD-002-Nouvelle-Release.md` (Étape 8)
- `docs/PRDs/PRD-003-Liste-Releases.md`
- `docs/DATABASE_ERD.md` (tables `releases`, `jobs`)

---

### 5. Users, Roles & Permissions
**Fichier** : `.cursor/rules/users-roles-permissions.mdc`

**Domaine** : Gestion utilisateurs, rôles, permissions granulaires

**Règles principales** :
- ✅ Username unique (UNIQUE)
- ✅ Password fort (min 8 caractères)
- ✅ Rôle unique par utilisateur
- ✅ Matrice permissions : Resource × Action (READ/WRITE/MOD/DELETE)
- ✅ Logique automatique : MOD → WRITE → READ
- ✅ Groupes multiples par utilisateur

**Quand utiliser** :
- Développement PRD-005 (Users)
- Développement PRD-006 (Roles)
- Système permissions granulaires
- Vérification permissions

**Références** :
- `docs/PRDs/PRD-005-Utilisateurs.md`
- `docs/PRDs/PRD-006-Roles.md`
- `docs/DATABASE_ERD.md` (tables `users`, `roles`, `permissions`, etc.)
- `docs/API_REFERENCE.md` (endpoints users, roles)

---

### 6. Configurations, APIs & Destinations
**Fichier** : `.cursor/rules/configurations-api-destinations.mdc`

**Domaine** : Configurations système, APIs externes, destinations FTP/SSH

**Règles principales** :
- ⚠️ **CRITIQUE** : Chiffrement Fernet OBLIGATOIRE pour credentials
- ✅ API keys chiffrées avant stockage
- ✅ FTP/SSH passwords chiffrés
- ✅ Test connexion OBLIGATOIRE avant sauvegarde
- ✅ Paramètres système configurables
- ✅ Préférences utilisateur (theme, language)

**Quand utiliser** :
- Développement PRD-007 (Configurations)
- Gestion APIs externes
- Destinations FTP/SSH
- Chiffrement credentials

**Références** :
- `docs/PRDs/PRD-007-Configurations.md`
- `docs/DATABASE_ERD.md` (tables `api_configs`, `destinations`, `preferences`)
- `docs/API_REFERENCE.md` (endpoints configurations)

---

## 🔄 Utilisation des Règles

### Développement par Phase

**Phase 1 (Infrastructure Core)** :
- Toutes règles générales (`project-v2`, `tdd-methodology`, etc.)
- `users-roles-permissions.mdc` (modèles User, Role, Permission)
- `configurations-api-destinations.mdc` (chiffrement, configs)

**Phase 3 (Wizard)** :
- `groups-scene.mdc` (Étape 1)
- `rules-scene.mdc` (Étape 3) ⚠️ CRITIQUE
- `templates-nfo.mdc` (Étape 7) ⚠️ CRITIQUE
- `releases-packaging.mdc` (Étape 8) ⚠️ CRITIQUE

**Phase 4 (Releases)** :
- `releases-packaging.mdc` (gestion releases)

**Phase 5 (Rules)** :
- `rules-scene.mdc` (gestion rules)

**Phase 6 (Users & Roles)** :
- `users-roles-permissions.mdc` (gestion users/roles)

---

## 📊 Tableau Récapitulatif

| Domaine | Règle | Priorité | Référence PRD |
|---------|-------|----------|---------------|
| **Templates NFO** | `templates-nfo.mdc` | ⚠️ CRITIQUE | PRD-002 (Étape 7) |
| **Rules Scene** | `rules-scene.mdc` | ⚠️ CRITIQUE | PRD-002 (Étape 3), PRD-004 |
| **Groups Scene** | `groups-scene.mdc` | ⚠️ CRITIQUE | PRD-002 (Étape 1) |
| **Releases & Packaging** | `releases-packaging.mdc` | ⚠️ CRITIQUE | PRD-002 (Étape 8), PRD-003 |
| **Users, Roles & Permissions** | `users-roles-permissions.mdc` | ⚠️ CRITIQUE | PRD-005, PRD-006 |
| **Configurations, APIs & Destinations** | `configurations-api-destinations.mdc` | ⚠️ CRITIQUE | PRD-007 |

---

## ✅ Checklist Vérification

### Avant Développement Domaine Spécifique

- [ ] Règle domaine correspondante identifiée
- [ ] Règle attachée au prompt
- [ ] PRD correspondant consulté
- [ ] Références techniques vérifiées
- [ ] Règles générales actives (alwaysApply)

### Avant Commit

- [ ] Conformité règle domaine vérifiée
- [ ] Tests conformes règle domaine
- [ ] Validation stricte respectée
- [ ] Documentation mise à jour si nécessaire

---

## 🔗 Références Complémentaires

- **Guide Attachement** : `.cursor/RULES_ATTACHMENT_GUIDE.md`
- **Règles Générales** : `.cursor/rules/project-v2.mdc`
- **Definition of Done** : `.cursor/rules/definition-of-done.mdc` ⚠️
- **Scenerules Integration** : `docs/SCENERULES_INTEGRATION.md` ⭐
- **Database ERD** : `docs/DATABASE_ERD.md`
- **API Reference** : `docs/API_REFERENCE.md`

---

**Dernière mise à jour** : 2025-11-01  
**Version** : 1.0.0  
**Priorité** : CRITIQUE ⚠️

**Rappel** : Chaque domaine a ses règles spécifiques pour garantir conformité absolue avec logique et objectifs du projet.

