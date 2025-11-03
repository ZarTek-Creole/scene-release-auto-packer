# 📋 Backlog Agile - eBook Scene Packer v2

**Date de création** : 2025-11-01  
**Méthodologie** : Scrum/Agile avec MoSCoW et Matrice Eisenhower

---

## 📊 Vue d'Ensemble

Ce backlog organise toutes les fonctionnalités en **Epics**, **User Stories** et **Tâches techniques**, avec priorités MoSCoW et classification Eisenhower.

---

## 🎯 Epics

### Epic 1 : Infrastructure Core
**Priorité MoSCoW** : Must Have  
**Matrice Eisenhower** : Urgent & Important  
**Statut** : ⏳ Non commencé

**Description** : Setup infrastructure technique (Flask, DB, JWT, Models)

**User Stories** :
- Voir section User Stories ci-dessous

---

### Epic 2 : Interface Administration
**Priorité MoSCoW** : Must Have  
**Matrice Eisenhower** : Important, pas urgent  
**Statut** : ⏳ Non commencé

**Description** : Interface d'administration complète (Dashboard, Navigation, Pages)

**User Stories** :
- US-001 à US-005 (voir ci-dessous)

---

### Epic 3 : Nouvelle Release Wizard
**Priorité MoSCoW** : Must Have  
**Matrice Eisenhower** : Urgent & Important  
**Statut** : ⏳ Non commencé

**Description** : Wizard 9 étapes pour création et packaging de release

**User Stories** :
- US-010 à US-018 (voir ci-dessous)

---

### Epic 4 : Liste des Releases
**Priorité MoSCoW** : Must Have  
**Matrice Eisenhower** : Important, pas urgent  
**Statut** : ⏳ Non commencé

**Description** : Affichage, filtres et actions sur releases

**User Stories** :
- US-020 à US-023

---

### Epic 5 : Rules Management
**Priorité MoSCoW** : Must Have  
**Matrice Eisenhower** : Important, pas urgent  
**Statut** : ⏳ Non commencé

**Description** : Gestion rules locales et distantes (scenerules.org)

**User Stories** :
- US-030 à US-035

---

### Epic 6 : Utilisateurs & Rôles
**Priorité MoSCoW** : Must Have  
**Matrice Eisenhower** : Important, pas urgent  
**Statut** : ⏳ Non commencé

**Description** : Gestion utilisateurs, groupes, rôles et permissions

**User Stories** :
- US-040 à US-047

---

### Epic 7 : Configurations
**Priorité MoSCoW** : Must Have  
**Matrice Eisenhower** : Important, pas urgent  
**Statut** : ⏳ Non commencé

**Description** : Configuration système, APIs, FTP/SSH, Templates

**User Stories** :
- US-050 à US-054

---

## 👥 User Stories

### Epic 1 : Infrastructure Core

#### US-001 : Setup Flask App Factory
**En tant que** développeur  
**Je veux** une structure Flask avec application factory  
**Afin de** avoir une architecture modulaire et testable

**Priorité MoSCoW** : Must Have  
**Estimation** : 1 jour  
**Tâches** :
- T-001 : Créer structure web/ avec create_app()
- T-002 : Configurer environnement (.env)
- T-003 : Setup blueprints structure
- T-004 : Tests TDD

**Acceptation** :
- App se lance en dev/prod
- Tests passent
- Structure modulaire

---

#### US-002 : Base de Données MySQL
**En tant que** développeur  
**Je veux** une base de données MySQL configurée  
**Afin de** stocker les données de l'application

**Priorité MoSCoW** : Must Have  
**Estimation** : 2 jours  
**Tâches** :
- T-010 : Setup Flask-SQLAlchemy
- T-011 : Configurer connexion MySQL
- T-012 : Setup Flask-Migrate
- T-013 : Tests TDD

---

#### US-003 : Authentification JWT
**En tant que** utilisateur  
**Je veux** m'authentifier via JWT  
**Afin de** accéder aux fonctionnalités de l'application

**Priorité MoSCoW** : Must Have  
**Estimation** : 3 jours  
**Tâches** :
- T-020 : Setup Flask-JWT-Extended
- T-021 : Endpoint login
- T-022 : Endpoint refresh
- T-023 : Protection routes
- T-024 : Tests TDD

---

### Epic 2 : Interface Administration

#### US-004 : Dashboard
**En tant que** administrateur  
**Je veux** voir un dashboard  
**Afin de** avoir une vue d'ensemble

**Priorité MoSCoW** : Must Have  
**Estimation** : 3 jours  
**Tâches** :
- T-030 : Composant Dashboard React
- T-031 : API endpoint stats
- T-032 : Tests TDD

---

#### US-005 : Navigation
**En tant que** utilisateur  
**Je veux** naviguer entre sections  
**Afin de** accéder aux fonctionnalités

**Priorité MoSCoW** : Must Have  
**Estimation** : 2 jours  
**Tâches** :
- T-040 : Composant Navigation
- T-041 : React Router config
- T-042 : Tests TDD

---

#### US-006 : Thème Jour/Nuit
**En tant que** utilisateur  
**Je veux** basculer thème  
**Afin de** améliorer confort visuel

**Priorité MoSCoW** : Should Have  
**Estimation** : 1 jour  
**Tâches** :
- T-050 : ThemeContext
- T-051 : ThemeToggle component
- T-052 : Styles dark mode
- T-053 : Tests TDD

---

### Epic 3 : Nouvelle Release Wizard

#### US-010 : Étape 1 - Groupe
**En tant que** opérateur  
**Je veux** saisir le nom du groupe  
**Afin de** créer une release pour ce groupe

**Priorité MoSCoW** : Must Have  
**Estimation** : 1 jour  
**Tâches** :
- T-100 : Formulaire groupe
- T-101 : Validation groupe
- T-102 : Tests TDD

---

#### US-011 : Étape 2 - Type Release
**En tant que** opérateur  
**Je veux** sélectionner le type de release  
**Afin de** définir le format de packaging

**Priorité MoSCoW** : Must Have  
**Estimation** : 1 jour  
**Tâches** :
- T-110 : Sélecteur type
- T-111 : Validation type
- T-112 : Tests TDD

---

#### US-012 : Étape 3 - Règle
**En tant que** opérateur  
**Je veux** choisir la règle à appliquer  
**Afin de** packager selon les règles Scene

**Priorité MoSCoW** : Must Have  
**Estimation** : 2 jours  
**Tâches** :
- T-120 : Liste règles filtrées
- T-121 : Sélection règle
- T-122 : Tests TDD

---

*(User Stories suivantes détaillées dans PRDs correspondants)*

---

## 📋 Matrice Eisenhower

### Urgent & Important (À faire immédiatement)
- Epic 1 : Infrastructure Core
- Epic 3 : Nouvelle Release Wizard (étapes 1-3)

### Important, pas urgent (À planifier)
- Epic 2 : Interface Administration
- Epic 4 : Liste des Releases
- Epic 5 : Rules Management
- Epic 6 : Utilisateurs & Rôles
- Epic 7 : Configurations

### Urgent, pas important (À déléguer/automatiser)
- Documentation automatique
- Scripts CI/CD

### Ni urgent ni important (À éliminer)
- Optimisations prématurées
- Features non essentielles

---

## 🔗 Liens

- **PRDs** : `docs/PRDs/`
- **DEVBOOK** : `docs/DEVBOOK.md`
- **Test Plan** : `docs/TEST_PLAN.md`
- **CDC** : `docs/cdc.md`

---

**Dernière mise à jour** : 2025-11-01  
**Prochaine mise à jour** : À chaque sprint

