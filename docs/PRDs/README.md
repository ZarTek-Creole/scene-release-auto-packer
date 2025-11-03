# 📄 PRDs - Product Requirement Documents

**Dossier** : `docs/PRDs/`  
**Objectif** : Définir les spécifications détaillées de chaque fonctionnalité majeure

---

## 📋 Structure des PRDs

Chaque PRD suit cette structure standardisée :

### 1. En-tête
- **ID** : PRD-XXX-Nom-Fonctionnalite
- **Version** : X.Y.Z
- **Date** : YYYY-MM-DD
- **Statut** : Draft | Review | Approved | Deprecated
- **Auteur** : Nom

### 2. Vue d'Ensemble
- Description fonctionnalité
- Objectifs
- Utilisateurs cibles

### 3. Détails Fonctionnels
- User Stories
- Scénarios d'utilisation
- Flux utilisateur

### 4. Contraintes Techniques
- API nécessaires
- Dépendances
- Limitations

### 5. Critères de Réussite
- Critères fonctionnels
- Critères de performance
- Critères de qualité

### 6. Tests (TDD)
- Tests unitaires nécessaires
- Tests d'intégration
- Tests E2E

### 7. Priorité MoSCoW
- Must Have | Should Have | Could Have | Won't Have

### 8. Dépendances
- PRDs liés
- Phases précédentes requises

---

## 📚 Liste des PRDs

### PRD-001 : Interface Administration
- **Fichier** : `PRD-001-Interface-Admin.md`
- **Description** : Navigation, dashboard, structure pages, thème
- **Priorité** : Must Have
- **Statut** : Draft

### PRD-002 : Nouvelle Release
- **Fichier** : `PRD-002-Nouvelle-Release.md`
- **Description** : Wizard 9 étapes pour création release
- **Priorité** : Must Have
- **Statut** : ✅ Créé (Draft)
- **Version** : 1.0.0

### PRD-003 : Liste des Releases
- **Fichier** : `PRD-003-Liste-Releases.md`
- **Description** : Affichage, filtres, actions sur releases
- **Priorité** : Must Have
- **Statut** : ✅ Créé (Draft)
- **Version** : 1.0.0

### PRD-004 : Rules Management
- **Fichier** : `PRD-004-Rules.md`
- **Description** : Gestion rules locales et scenerules.org
- **Priorité** : Must Have
- **Statut** : ✅ Créé (Draft)
- **Version** : 1.0.0

### PRD-005 : Utilisateurs
- **Fichier** : `PRD-005-Utilisateurs.md`
- **Description** : Gestion utilisateurs et groupes
- **Priorité** : Must Have
- **Statut** : ✅ Créé (Draft)
- **Version** : 1.0.0

### PRD-006 : Rôles
- **Fichier** : `PRD-006-Roles.md`
- **Description** : Gestion rôles et permissions
- **Priorité** : Must Have
- **Statut** : ✅ Créé (Draft)
- **Version** : 1.0.0

### PRD-007 : Configurations
- **Fichier** : `PRD-007-Configurations.md`
- **Description** : Configuration système, APIs, FTP/SSH
- **Priorité** : Must Have
- **Statut** : ✅ Créé (Draft)
- **Version** : 1.0.0

---

## 🔄 Règles de Mise à Jour

### Quand mettre à jour un PRD
1. **Nouvelle fonctionnalité** : Créer nouveau PRD
2. **Modification majeure** : Mettre à jour PRD existant (version++)
3. **Clarification** : Mettre à jour sans changer version
4. **Dépréciation** : Marquer comme Deprecated

### Processus de Review
1. Auteur crée/édite PRD
2. Statut : Draft → Review
3. Review par équipe
4. Modifications si nécessaire
5. Statut : Review → Approved

### Liens avec autres Documents
- **User Stories** : Lien vers `docs/BACKLOG_AGILE.md`
- **Tests** : Lien vers `docs/TEST_PLAN.md`
- **Risques** : Lien vers `docs/RISKS_REGISTER.md`
- **Phases** : Lien vers `docs/DEVBOOK.md`

---

**Dernière mise à jour** : 2025-11-01  
**Maintenu par** : Équipe de développement

