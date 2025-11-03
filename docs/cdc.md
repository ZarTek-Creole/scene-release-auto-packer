# 📋 Cahier des Charges - eBook Scene Packer v2

**Date de création** : 2025-11-01  
**Version** : 2.0.0  
**Statut** : En développement

---

## 1. Vision du Projet

Application web moderne de packaging de releases Scene (EBOOK, TV, DOCS) avec interface d'administration complète, permettant la gestion des releases, règles Scene, utilisateurs, rôles et configurations. L'objectif est de reconstruire une v2 propre en prenant en compte les leçons apprises de la v1, avec une architecture solide, une méthodologie TDD stricte et une documentation exhaustive.

### Référence
- **v1/** : Version précédente conservée comme référence technique et fonctionnelle

---

## 2. Objectifs

### Objectifs Principaux
- ✅ Créer une application moderne avec architecture propre et modulaire (v2)
- ✅ Implémenter une interface d'administration complète et intuitive
- ✅ Gérer les releases avec processus multi-étapes (wizard)
- ✅ Gérer les règles Scene (locales et distantes depuis scenerules.org)
- ✅ Gérer utilisateurs, rôles et permissions granulaires (READ/WRITE/MOD)
- ✅ Configuration centralisée et sécurisée

### Objectifs Techniques
- Architecture modulaire et testable
- Couverture de tests à 100% (méthodologie TDD)
- Sécurité renforcée (JWT, chiffrement credentials)
- Performance optimisée (caching, requêtes optimisées)
- Accessibilité WCAG 2.2 AA

---

## 3. Utilisateurs Cibles

### 3.1 Administrateurs
- **Accès** : Accès complet à toutes les fonctionnalités
- **Responsabilités** :
  - Gestion des utilisateurs et rôles
  - Configuration système et APIs
  - Gestion des règles Scene
  - Supervision des releases

### 3.2 Opérateurs
- **Accès** : Packaging uniquement, sans accès configuration système
- **Responsabilités** :
  - Création de releases via wizard
  - Édition de leurs propres releases
  - Visualisation des règles Scene

---

## 4. Fonctionnalités Principales

### 4.1 Interface Administration

#### 4.1.1 Navigation
- Dashboard avec informations utilisateur connecté ("admin")
- Navigation entre sections :
  - Nouvelle Release
  - Liste des Releases
  - Rules
  - Utilisateurs
  - Rôles
  - Configurations
- Thème jour/nuit (bascule)
- Déconnexion

#### 4.1.2 Structure des Pages
Chaque onglet dispose d'un **titre** et d'une **description** dans le corps de la page.

---

### 4.2 Nouvelle Release (Wizard Multi-étapes)

**Objectif** : Créer une nouvelle release et la packager via un processus guidé en 9 étapes.

#### Étape 1 : Formulaire Initial
- **Action** : Demander le nom du groupe
- **Validation** : Groupe conforme aux règles Scene
- **Stockage** : Sauvegarde temporaire en session

#### Étape 2 : Type de Release
- **Options** : TV, EBOOK, DOCS, etc.
- **Validation** : Type valide selon règles Scene
- **Dépendances** : Définit les formats de fichiers acceptés

#### Étape 3 : Règle à Appliquer
- **Source** : Rules locales ou scenerules.org
- **Filtrage** : Par type de release sélectionné
- **Sélection** : Choix de la règle applicable

#### Étape 4 : Sélection du Fichier
- **Modes** :
  - Upload local (drag & drop ou sélecteur)
  - URL distante (HTTP/HTTPS/FTP)
- **Validation** :
  - Formats/extensions acceptés selon type de release
  - Taille maximale
  - Vérification intégrité
- **Traitement** : Téléchargement si distant

#### Étape 5 : Analyse du Fichier
- **Extraction** :
  - MediaInfo (pour vidéo/TV)
  - Métadonnées (auteur, titre, ISBN, etc.)
  - Structure interne (pour EPUB, PDF, etc.)
- **Stockage** : Résultats sauvegardés pour étapes suivantes

#### Étape 6 : Résumé et Enrichissement
- **Affichage** :
  - Résumé des informations collectées
  - Options choisies par l'utilisateur
- **Enrichissement** :
  - Proposition d'APIs externes pour compléter
  - Affichage résultats APIs (OpenLibrary, Google Books, OMDb, TVDB, TMDb, etc.)
- **Édition** : Possibilité de modification manuelle

#### Étape 7 : Templates
- **Affichage** : Templates disponibles avec informations pré-remplies
- **Source** : Informations de l'étape précédente injectées dans templates
- **Édition** : Possibilité de modification manuelle du template sélectionné
- **Prévisualisation** : Aperçu du NFO/DIZ généré

#### Étape 8 : Options et Paramètres
- **Affichage** :
  - Options/paramètres des commandes qui seront exécutées
  - Configuration packaging (ZIP, RAR, volumes, etc.)
- **Édition** : Possibilité de modification manuelle
- **Validation** : Bouton "Valider et Packager"
- **Exécution** :
  - Lancement des commandes
  - Packaging de la Release
  - Logs en temps réel

#### Étape 9 : Destination
- **Options** :
  - Répertoire local
  - FTP/SFTP
  - SSH
  - Autres protocoles
- **Configuration** : Sélection ou création destination
- **Upload** : Transfert automatique de la release packagée

---

### 4.3 Liste des Releases

**Objectif** : Afficher et gérer les releases créées.

#### 4.3.1 Vues
- **Par Groupe** : Liste des releases par groupe (selon droits utilisateur)
- **Mes Releases** : Liste des releases créées par l'utilisateur connecté

#### 4.3.2 Actions sur Release
- **Édition** : Modifier une release existante
- **Corrections** : Possibilité de corriger/refaire le packaging
- **Actions Spéciales** :
  - NFOFIX : Corriger le fichier NFO
  - READNFO : Regénérer à partir du NFO
  - REPACK : Repackager la release
  - DIRFIX : Corriger la structure de répertoires

#### 4.3.3 Filtres et Recherche
- Filtrage par type, groupe, date
- Recherche textuelle
- Tri (date, nom, taille)

---

### 4.4 Rules (Règles Scene)

**Objectif** : Gérer les règles Scene locales et distantes.

#### 4.4.1 Organisation
- **Par Scène** : English, Baltic, Danish, Dutch, Flemish, French, German, Hungarian, Italian, Lithuanian, Polish, Spanish, Swedish, etc.
- **Par Section** :
  - 0DAY7, AUDiOBOOK, BLURAY, CONSOLE, eBOOK, FLAC v3, FLAC (WEB), GAMEiSO, MP3, MViD, NSW
  - PS4 v1.17, PS5, PSV, TV-720p, TV-SD, WEB, X264, X265, X2655
  - SD-X2647, SD-XXX, XXX-iMAGESETS, XXX-iMAGESETS1, XXX-PAYSiTES, etc.
- **Par Année** : Filtrage par année de la règle

#### 4.4.2 Rules Locales
- **Liste** : Affichage des rules utilisées localement
- **Actions** :
  - Recherche dans la liste
  - Suppression d'une rule
  - Upload d'une rule (fichier local)
  - Affichage d'une rule en mode NFO viewer
  - Édition d'une rule

#### 4.4.3 Rules de scenerules.org
- **Liste** : Affichage des rules disponibles sur https://scenerules.org/
- **Actions** :
  - Recherche dans la liste
  - Téléchargement d'une rule vers les rules locales
  - Affichage d'une rule en mode NFO viewer
  - Synchronisation automatique (optionnelle)

---

### 4.5 Utilisateurs

**Objectif** : Gérer les utilisateurs sous l'administration.

#### 4.5.1 Liste des Utilisateurs
- Affichage de tous les utilisateurs
- Informations affichées :
  - Nom d'utilisateur
  - Groupes associés
  - Rôles assignés
  - Statut (actif/inactif)

#### 4.5.2 Actions
- **Création** : Créer un nouvel utilisateur
- **Modification** : Éditer un utilisateur existant
- **Suppression** : Désactiver/supprimer un utilisateur
- **Affectation Groupe** : Définir un groupe à un utilisateur
- **Affectation Rôle** :
  - Assigner un rôle à un utilisateur
  - Configurer les droits READ/WRITE/MOD pour chaque option du rôle

---

### 4.6 Rôles

**Objectif** : Gérer les rôles et leurs permissions.

#### 4.6.1 Liste des Rôles
- Affichage de tous les rôles disponibles
- Informations affichées :
  - Nom du rôle
  - Description
  - Permissions associées
  - Nombre d'utilisateurs ayant ce rôle

#### 4.6.2 Actions CRUD
- **Création** : Créer un nouveau rôle
- **Suppression** : Supprimer un rôle (avec vérification utilisateurs)
- **Modification** : Éditer un rôle existant

#### 4.6.3 Configuration Permissions
- **Options disponibles** :
  - Nouvelle Release
  - Liste des Releases
  - Rules (locales/distantes)
  - Utilisateurs
  - Rôles
  - Configurations
- **Niveaux de droits** :
  - **READ** : Lecture seule
  - **WRITE** : Création/écriture
  - **MOD** : Modification/édition
- **Interface** : Matrice permissions par option

#### 4.6.4 Liste Utilisateurs par Rôle
- Affichage des utilisateurs ayant un rôle spécifique
- Filtrage et recherche

---

### 4.7 Configurations

**Objectif** : Configuration centralisée de l'application.

#### 4.7.1 Paramètres Système
- Chemins de base (uploads, releases, cache)
- Limites (taille fichiers, timeouts)
- Logs (niveau, rotation)

#### 4.7.2 Configuration APIs Externes
- OpenLibrary
- Google Books
- OMDb
- TVDB
- TMDb
- Autres APIs nécessaires
- **Sécurité** : Chiffrement des clés API

#### 4.7.3 Configuration FTP/SSH
- Destinations FTP/SFTP
- Identifiants chiffrés
- Paramètres de connexion

#### 4.7.4 Configuration Templates
- Gestion des templates NFO/DIZ
- Variables disponibles
- Structure et validation

---

## 5. Contraintes Techniques

### 5.1 Stack Technologique
- **Frontend** : ReactJS (dernière version)
- **Backend** : Flask (Python 3.11+)
- **Database** : MySQL 8.0+ (InnoDB)
- **Styling** : Bootstrap 5 (dernière version)
- **API** : RESTful JSON

### 5.2 Architecture
- **Pattern** : Application Factory (Flask)
- **Structure** : Blueprints modulaires
- **ORM** : Flask-SQLAlchemy
- **Sérialisation** : Marshmallow
- **Authentification** : Flask-JWT-Extended
- **Caching** : Flask-Caching
- **Migrations** : Flask-Migrate

### 5.3 Sécurité
- **JWT** : Tokens avec refresh et révocation
- **Chiffrement** : Credentials API/FTP chiffrés (Fernet/AES-GCM)
- **Validation** : Input validation stricte
- **CORS** : Configuration sécurisée
- **HTTPS** : Obligatoire en production

### 5.4 Performance
- **Caching** : Endpoints fréquemment accédés
- **Optimisation** : Requêtes DB optimisées (indexes)
- **Lazy Loading** : Frontend (React.lazy, Suspense)
- **Bundle** : Code splitting et minification

### 5.5 Accessibilité
- **WCAG 2.2 AA** : Conformité niveau AA
- **ARIA** : Attributs ARIA appropriés
- **Clavier** : Navigation au clavier complète
- **Écran** : Compatible lecteurs d'écran

---

## 6. Méthodologies

### 6.1 TDD (Test Driven Development)
- **Obligatoire** : Tous les développements en TDD
- **Cycle** : Red → Green → Refactor
- **Couverture** : Objectif 100%
- **Types** :
  - Tests unitaires (pytest)
  - Tests d'intégration
  - Tests E2E (Playwright/Selenium)
  - Tests de performance

### 6.2 MoSCoW (Priorisation)
- **Must Have** : Fonctionnalités essentielles
- **Should Have** : Fonctionnalités importantes
- **Could Have** : Fonctionnalités souhaitables
- **Won't Have** : Fonctionnalités exclues

### 6.3 SWOT (Analyse)
- **Forces** : Points forts du projet
- **Faiblesses** : Points faibles identifiés
- **Opportunités** : Opportunités externes
- **Menaces** : Risques externes

### 6.4 Backlog Agile
- **Epics** : Grandes fonctionnalités
- **User Stories** : Besoins utilisateur
- **Tâches** : Tâches techniques détaillées
- **Sprints** : Itérations de développement

### 6.5 DMAIC (Optimisation)
- **Define** : Définir processus critiques
- **Measure** : Mesurer performance
- **Analyze** : Analyser données
- **Improve** : Améliorer processus
- **Control** : Contrôler et maintenir

### 6.6 OKRs (Objectives and Key Results)
- **Objectifs** : Objectifs mesurables par phase
- **Key Results** : Résultats clés pour validation

### 6.7 Matrice Eisenhower (Priorisation)
- **Urgent & Important** : À faire immédiatement
- **Important, pas urgent** : À planifier
- **Urgent, pas important** : À déléguer
- **Ni urgent ni important** : À éliminer

---

## 7. Livrables

### 7.1 Code
- Application web fonctionnelle (Frontend + Backend)
- Tests avec couverture 100%
- Documentation code (docstrings)
- Scripts utilitaires

### 7.2 Documentation
- **CDC** : Ce cahier des charges
- **DEVBOOK** : Suivi des phases et étapes
- **PRDs** : Product Requirement Documents
- **BACKLOG** : Backlog Agile avec User Stories
- **TEST_PLAN** : Plan de tests complet
- **DEPLOYMENT_PLAN** : Plan de déploiement
- **RISKS_REGISTER** : Registre des risques

### 7.3 Infrastructure
- Configuration Docker (docker-compose.yml)
- Scripts de déploiement
- Configuration CI/CD
- Monitoring et logging

---

## 8. Timeline (Estimation)

### Phase 0 : Préparation (1 semaine)
- Backup v1/
- Création documentation structurée
- Configuration environnement développement
- Setup TDD

### Phase 1 : Infrastructure Core (2 semaines)
- Setup Flask app factory
- Base de données MySQL
- Authentification JWT
- Modèles de base

### Phase 2 : Interface Administration (3 semaines)
- Dashboard
- Navigation
- Pages principales (structure)
- Thème jour/nuit

### Phase 3 : Nouvelle Release Wizard (4 semaines)
- Étapes 1-3 : Groupe, Type, Règle
- Étapes 4-5 : Fichier, Analyse
- Étapes 6-7 : Enrichissement, Templates
- Étapes 8-9 : Packaging, Destination

### Phase 4 : Liste des Releases (2 semaines)
- Affichage liste
- Filtres et recherche
- Actions (édition, corrections)

### Phase 5 : Rules Management (3 semaines)
- Rules locales
- Integration scenerules.org
- NFO viewer

### Phase 6 : Utilisateurs & Rôles (2 semaines)
- Gestion utilisateurs
- Gestion rôles
- Permissions granulaires

### Phase 7 : Configurations (2 semaines)
- Paramètres système
- APIs externes
- FTP/SSH

### Phase 8 : Tests & Optimisation (2 semaines)
- Tests E2E complets
- Optimisation performance
- Accessibilité

### Phase 9 : Déploiement (1 semaine)
- Configuration production
- Déploiement
- Monitoring

**Total estimé** : ~20 semaines (~5 mois)

---

## 9. Dépendances Externes

### 9.1 APIs
- OpenLibrary API
- Google Books API
- OMDb API
- TVDB API
- TMDb API
- scenerules.org (scraping)

### 9.2 Services
- MySQL Database
- FTP/SFTP Servers (destinations)
- File Storage (local ou cloud)

---

## 10. Risques Identifiés

Voir `docs/RISKS_REGISTER.md` pour le registre complet des risques avec analyses SWOT et plans de mitigation.

---

## 11. Critères de Réussite

### 11.1 Fonctionnels
- ✅ Toutes les fonctionnalités décrites implémentées
- ✅ Interface utilisateur intuitive et accessible
- ✅ Performance acceptable (< 2s chargement pages)
- ✅ Compatibilité navigateurs modernes

### 11.2 Techniques
- ✅ Couverture tests 100%
- ✅ Aucune vulnérabilité critique de sécurité
- ✅ Documentation complète et à jour
- ✅ Code maintenable et modulaire

### 11.3 Qualité
- ✅ Conformité WCAG 2.2 AA
- ✅ Code reviews effectués
- ✅ Tests automatisés passent
- ✅ Déploiement réussi en production

---

## 12. Références

### 12.1 Documentation v1
- Codebase v1 conservé dans `v1/`
- Documentation v1 archivée dans `v1/docs/`

### 12.2 Standards Scene
- Scene Rules disponibles sur scenerules.org
- Formats de releases standards

### 12.3 Technologies
- ReactJS Documentation
- Flask Documentation
- MySQL Documentation
- Bootstrap Documentation

---

**Document maintenu par** : Équipe de développement  
**Dernière mise à jour** : 2025-11-01  
**Version** : 2.0.0

