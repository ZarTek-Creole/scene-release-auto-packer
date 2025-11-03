# 🔍 Analyse Complète du Projet - Questions et Informations Manquantes

**Date** : 2025-11-01  
**Objectif** : Identifier toutes les questions critiques et informations manquantes pour compléter le projet v2

---

## 📊 État Actuel du Projet

### ✅ Phase 0 : Complétée à 100%
- Backup v1/ créé
- Documentation structurée (10 fichiers)
- Règles Cursor (6 règles)
- Environnement développement configuré
- Tests Phase 0 : 34/34 passent (100%)

### ⏳ Phase 1+ : À démarrer
- Infrastructure Core non commencée
- Code v2 non implémenté (structure vide)
- Frontend React non créé

---

## 🎯 Catégories de Questions

### 1. Architecture et Structure

### 2. Fonctionnalités et PRDs

### 3. Intégration v1 → v2

### 4. Décisions Techniques

### 5. Frontend React

### 6. Backend Flask

### 7. Base de Données

### 8. Sécurité et Permissions

### 9. Déploiement et Infrastructure

### 10. Tests et Qualité

---

## 1. Architecture et Structure

### Q1.1 : Structure Frontend React
**Question** : Quelle structure exacte pour le frontend React ?

**Contexte** :
- CDC mentionne React 18+ avec Bootstrap 5
- PRD-001 mentionne composants mais pas de structure détaillée
- v1 n'a pas de React (templates Flask)

**Réponses suggérées** :
```javascript
// Option 1 : Structure modulaire
src/
├── components/
│   ├── common/          # Composants réutilisables
│   ├── wizard/          # Composants wizard
│   ├── releases/        # Composants releases
│   └── rules/           # Composants rules
├── contexts/            # React Contexts
│   ├── AuthContext.js
│   ├── ThemeContext.js
│   └── WizardContext.js
├── services/            # Services API
│   └── api.js
├── hooks/               # Custom hooks
├── utils/               # Utilitaires
└── pages/               # Pages/Views
    ├── Dashboard.js
    ├── NewRelease.js
    ├── ReleasesList.js
    └── ...

// Option 2 : Structure feature-based
features/
├── auth/
├── wizard/
├── releases/
└── rules/
```

**Recommandation** : Option 1 (modulaire) pour commencer, migrer vers Option 2 si le projet grandit.

---

### Q1.2 : Migration Progressive vs From Scratch
**Question** : Doit-on réutiliser du code v1 ou tout refaire from scratch ?

**Contexte** :
- v1 contient beaucoup de code fonctionnel (packaging, métadonnées, etc.)
- v2 est une refonte complète

**✅ Décision finale** : Tout refaire from scratch en s'inspirant de v1

**Raison** : Utiliser v1 uniquement pour prendre des exemples. La v2 doit être faite de manière propre et être la v2 totalement, avec brainstorming.

**Stratégie** :
- ✅ Code propre, architecture moderne
- ✅ Tests complets dès le départ
- ✅ Pas de dette technique v1
- ✅ Refonte complète avec meilleures pratiques
- ❌ Plus long mais nécessaire pour qualité

---

### Q1.3 : Structure Backend Flask
**Question** : Quelle structure exacte pour `web/` ?

**Contexte** :
- CDC mentionne blueprints modulaires
- v1 a déjà une structure avec blueprints

**Réponses suggérées** :
```python
web/
├── app.py               # Application factory
├── config.py            # Configuration
├── extensions.py        # Extensions Flask (db, jwt, cache)
├── blueprints/
│   ├── auth.py         # Authentification
│   ├── dashboard.py    # Dashboard
│   ├── wizard.py       # Wizard 9 étapes
│   ├── releases.py     # Liste releases
│   ├── rules.py        # Rules management
│   ├── users.py        # Gestion utilisateurs
│   ├── roles.py        # Gestion rôles
│   └── config.py       # Configurations
├── models/
│   ├── user.py
│   ├── role.py
│   ├── permission.py
│   ├── group.py
│   ├── release.py
│   └── job.py
├── services/
│   ├── packaging.py
│   ├── metadata.py
│   ├── ftp_upload.py
│   └── template_renderer.py
├── schemas/
│   └── ...            # Marshmallow schemas
└── utils/
    ├── crypto.py      # Chiffrement
    └── validators.py
```

**Recommandation** : Suivre cette structure (inspirée v1 mais simplifiée).

---

## 2. Fonctionnalités et PRDs

### Q2.1 : PRDs Manquants
**Question** : Quels PRDs doivent être créés en priorité ?

**Contexte** :
- Seul PRD-001 (Interface Admin) existe
- CDC mentionne 7 fonctionnalités principales
- PRD-002 à PRD-007 manquants

**Réponses suggérées** :
**Priorité Must Have** :
1. ✅ PRD-001 : Interface Administration (existe)
2. ⏳ PRD-002 : Nouvelle Release Wizard (9 étapes) - **CRITIQUE**
3. ⏳ PRD-003 : Liste des Releases
4. ⏳ PRD-004 : Rules Management
5. ⏳ PRD-005 : Utilisateurs
6. ⏳ PRD-006 : Rôles

**Priorité Should Have** :
7. ⏳ PRD-007 : Configurations

**✅ Action confirmée** : Créer tous les PRDs au complet (PRD-002 à PRD-007).

---

### Q2.2 : Détails Wizard 9 Étapes
**Question** : Quels sont les détails exacts de chaque étape du wizard ?

**Contexte** :
- CDC décrit 9 étapes mais pas tous les détails
- v1 a un wizard 12 étapes (à adapter pour v2)
- Besoin de spécifications précises pour implémentation

**Réponses suggérées** :

**✅ Étape 1 : Groupe**
- Validation : Format Scene (regex)
- Stockage : Backend (Job avec statut draft)
- UI : Input texte avec autocomplete (suggestions groupes existants)

**✅ Étape 2 : Type Release**
- Types exacts : EBOOK en priorité (première fonctionnalité complète)
- Autres types (TV, DOCS, AUDIOBOOK, GAME, etc.) : Créer quand tout fonctionnel et confirmé pour EBOOK
- Format fichiers acceptés par type : Selon rules de https://scenerules.org/

**✅ Étape 3 : Règle**
- Source : Locales + scenerules.org + upload
- Format affichage : Liste ET arborescence (double vue)
- Filtrage : Par scène, section, année

**✅ Étape 4 : Fichier**
- Upload local : Drag & drop, sélecteur, navigation dans l'arborescence
- URL distante : Formats acceptés (HTTP/HTTPS uniquement, pas FTP direct)
- Taille maximale : 20GB
- Validation en temps réel : OUI

**✅ Étape 5 : Analyse**
- Quelles métadonnées : Maximum possibles
- MediaInfo : Pour tous types
- Temps traitement estimé affiché : OUI avec barre de progression

**✅ Étape 6 : Enrichissement**
- Quelles APIs exactement : À rechercher sur internet par rapport au Type Release
- Ordre de priorité si plusieurs sources : Configurable par utilisateur
- Validation manuelle obligatoire : OUI avec prévisualisation

**✅ Étape 7 : Templates**
- Où sont stockés les templates : Disque OU base de données (choix configurable)
- Édition inline ou popup : Inline avec visualisation "nfo viewer" monospace, UTF-8
- Prévisualisation temps réel : OUI avec "nfo viewer" monospace, UTF-8

**✅ Étape 8 : Options/Paramètres**
- Quels paramètres exactement : Tout ce qui peut être utile
- Validation avant exécution : Évidemment OUI
- Logs en temps réel : OUI

**✅ Étape 9 : Destination**
- Formats de destination exacts : Directory local (on backup le fichier source)
- Test connexion avant upload : OUI pour FTP/SSH
- Progress bar upload : OUI

**Action** : Créer PRD-002 détaillé avec spécifications précises.

---

### Q2.3 : Fonctionnalités v1 à Reprendre
**Question** : Quelles fonctionnalités v1 doivent être reprises dans v2 ?

**Contexte** :
- v1 a 91 tests, beaucoup de fonctionnalités
- Certaines peuvent être simplifiées ou améliorées

**Réponses suggérées** :
**À reprendre (Must Have)** :
- ✅ Packaging EBOOK (logique métier)
- ✅ Packaging TV (logique métier)
- ✅ Packaging DOCS
- ✅ Extraction métadonnées
- ✅ Enrichissement APIs
- ✅ Templates NFO
- ✅ Upload FTP/SFTP
- ✅ Système jobs/logs

**À améliorer** :
- 🔄 Wizard (12 étapes v1 → 9 étapes v2 simplifié)
- 🔄 Frontend (templates Flask → React moderne)
- 🔄 Architecture (refactor pour tests)

**À laisser tomber** :
- ❌ Fonctionnalités non utilisées
- ❌ Code mort

**Action** : Audit v1 pour identifier code à réutiliser.

---

## 3. Intégration v1 → v2

### Q3.1 : Réutilisation Code v1
**Question** : Comment réutiliser le code v1 de manière propre ?

**Contexte** :
- v1 contient logique métier fonctionnelle
- v2 doit avoir architecture propre

**✅ Décision finale** : Utiliser v1 uniquement pour prendre des exemples

**Stratégie** :
- ✅ Utiliser v1 comme référence/exemples
- ✅ V2 doit être faite de manière propre et être la v2 totalement
- ✅ Brainstorming complet pour meilleures pratiques
- ✅ Pas de réutilisation directe de code v1
- ✅ Architecture moderne from scratch

**Action** : Référencer v1 pour comprendre logique métier, puis implémenter v2 proprement avec brainstorming complet.

---

### Q3.2 : Migration Données v1
**Question** : Comment migrer les données de v1 vers v2 si nécessaire ?

**Contexte** :
- v1 a une base de données avec données
- v2 aura nouveau schéma (potentiellement différent)

**Réponses suggérées** :
- **Option A** : Nouvelle base v2, pas de migration
  - ✅ Simple
  - ✅ Pas de dette
- **Option B** : Script migration v1 → v2
  - ✅ Préserve données
  - ❌ Complexe si schéma change

**Recommandation** : **Option A** (fresh start) pour v2, sauf si données critiques.

---

## 4. Décisions Techniques

### Q4.1 : State Management Frontend
**Question** : Context API ou Redux pour état global ?

**Contexte** :
- CDC mentionne "Context API ou Redux selon besoin"
- Wizard 9 étapes aura beaucoup d'état

**Réponses suggérées** :
- **Context API** :
  - ✅ Simple, natif React
  - ✅ Suffisant pour wizard
  - ❌ Performance si state complexe
- **Redux** :
  - ✅ Performance, DevTools
  - ✅ Évolutif
  - ❌ Plus complexe

**Recommandation** : **Context API** pour commencer, Redux si besoin performance.

---

### Q4.2 : TypeScript Frontend
**Question** : Migrer vers TypeScript maintenant ou plus tard ?

**Contexte** :
- CDC mentionne "TypeScript recommandé (à migrer progressivement)"
- Frontend pas encore créé

**Réponses suggérées** :
- **Option A** : JavaScript maintenant, TypeScript plus tard
  - ✅ Développement rapide
  - ❌ Refactoring nécessaire plus tard
- **Option B** : TypeScript dès le début
  - ✅ Type safety
  - ✅ Meilleure DX
  - ❌ Setup initial plus long

**Recommandation** : **Option B** (TypeScript dès le début) pour éviter refactoring.

---

### Q4.3 : Gestion État Wizard
**Question** : Comment gérer l'état du wizard (session, localStorage, backend) ?

**Contexte** :
- Wizard 9 étapes avec beaucoup de données
- Sauvegarde progression nécessaire
- Persistance entre sessions?

**Réponses suggérées** :
- **Option A** : LocalStorage frontend uniquement
  - ✅ Simple
  - ❌ Perdu si changement navigateur
- **Option B** : Backend session (Job avec statut draft)
  - ✅ Persistant
  - ✅ Partageable
  - ❌ Plus complexe
- **Option C** : Hybride (localStorage + backend draft)
  - ✅ Meilleur des deux mondes

**Recommandation** : **Option C** (hybride) pour UX optimale.

---

### Q4.4 : Format Templates NFO
**Question** : Format exact des templates NFO ?

**Contexte** :
- v1 a système templates avec placeholders
- Besoin comprendre format exact

**✅ Format confirmé** :
- **Format v1** : Placeholders `{{variable}}`, conditionnelles `{% if %}`
- **Améliorations v2** :
  - Support fonctions `{{format_date(date)}}`
  - Validation template
  - Preview temps réel
  - Ajout de Placeholders selon les outputs des métadonnées/mediainfo, au fur et à mesure des tests

**Action** : Analyser v1 pour comprendre format exact, documenter dans PRD, et ajouter Placeholders progressivement selon besoins réels.

---

## 5. Frontend React

### Q5.1 : Setup React
**Question** : Create React App, Vite, ou autre ?

**Contexte** :
- CDC ne spécifie pas l'outil de build
- Performance et DX importantes

**✅ Décision finale** : **Vite**

**Raisons** :
- ✅ Très rapide (dev server instantané)
- ✅ Moderne, ES modules natifs
- ✅ Recommandé 2024
- ✅ Excellent support TypeScript
- ✅ Configuration simple et flexible

**Action** : 
- ✅ Rechercher sur internet avec MCP Context7 pour confirmer avec dernières technologies
- ✅ Confirmer comment l'implémentation fonctionne (React + TypeScript + Vite)
- ✅ Documenter configuration complète dans PRD ou guide setup

---

### Q5.2 : Routing Frontend
**Question** : Structure exacte des routes React ?

**Contexte** :
- CDC mentionne React Router v6
- 6 sections principales à router

**Réponses suggérées** :
```javascript
Routes:
/                          # Dashboard (redirect si auth)
/login                     # Login
/dashboard                 # Dashboard
/releases/new              # Wizard Nouvelle Release
/releases/new/:step        # Étape spécifique wizard
/releases                  # Liste releases
/releases/:id              # Détail release
/releases/:id/edit         # Édition release
/rules                     # Rules locales
/rules/scenerules          # Rules scenerules.org
/users                     # Liste utilisateurs
/users/:id                 # Détail utilisateur
/roles                     # Liste rôles
/roles/:id                  # Détail rôle
/config                    # Configurations
/config/apis               # Config APIs
/config/ftp                # Config FTP
```

**Action** : Valider structure routes avec utilisateurs.

---

### Q5.3 : Composants Wizard
**Question** : Quels composants exacts pour le wizard ?

**Contexte** :
- 9 étapes avec interactions complexes
- Navigation, validation, sauvegarde

**Réponses suggérées** :
**Composants à créer** :
- `WizardContainer` : Container principal avec state
- `WizardNavigation` : Previous/Next buttons
- `WizardProgress` : Indicateur progression (1/9, 2/9, etc.)
- `StepGroup` : Formulaire groupe
- `StepReleaseType` : Sélecteur type
- `StepRules` : Liste/filtre rules
- `StepFileSelection` : Upload + URL
- `StepAnalysis` : Résultats analyse
- `StepEnrichment` : APIs + édition
- `StepTemplates` : Sélection + preview
- `StepOptions` : Paramètres packaging
- `StepDestination` : Choix destination

**Action** : Créer maquettes ou wireframes pour chaque étape.

---

### Q5.4 : Authentification Frontend
**Question** : Comment gérer l'authentification React ?

**Contexte** :
- JWT backend
- Protection routes
- Refresh token

**Réponses suggérées** :
- **AuthContext** : Gestion état auth
- **ProtectedRoute** : Wrapper routes protégées
- **Token refresh** : Automatique avant expiration
- **localStorage** : Stockage token
- **Axios interceptors** : Injection token automatique

**Action** : Créer composants auth de base.

---

## 6. Backend Flask

### Q6.1 : Modèles Base de Données
**Question** : Quels modèles exacts doivent être créés ?

**Contexte** :
- CDC mentionne User, Role, Permission, Group
- v1 a d'autres modèles (Job, Preference, etc.)

**Réponses suggérées** :
**Modèles Must Have** :
- `User` : Utilisateurs
- `Role` : Rôles
- `Permission` : Permissions (resource, action)
- `Group` : Groupes Scene
- `Release` : Releases créées
- `Job` : Jobs de packaging
- `Rule` : Rules Scene locales

**Modèles Should Have** :
- `Preference` : Préférences utilisateur
- `ApiConfig` : Configuration APIs
- `Destination` : Destinations FTP/SSH
- `Template` : Templates NFO

**Relations** :
- User ↔ Role (many-to-many)
- Role ↔ Permission (many-to-many)
- User ↔ Group (many-to-many)
- User → Release (one-to-many)
- Release → Job (one-to-many)

**Action** : Créer diagramme ERD, puis modèles SQLAlchemy.

---

### Q6.2 : Endpoints API
**Question** : Quels endpoints API exacts doivent être créés ?

**Contexte** :
- CDC décrit fonctionnalités mais pas endpoints détaillés
- v1 a beaucoup d'endpoints

**Réponses suggérées** :
**Auth** :
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `POST /api/auth/logout`
- `GET /api/auth/me`

**Dashboard** :
- `GET /api/dashboard/stats`

**Wizard** :
- `POST /api/wizard/step/:step/validate`
- `POST /api/wizard/step/:step/save`
- `POST /api/wizard/pack`
- `GET /api/wizard/step/:step/data`

**Releases** :
- `GET /api/releases`
- `GET /api/releases/:id`
- `PUT /api/releases/:id`
- `DELETE /api/releases/:id`
- `POST /api/releases/:id/repack`

**Rules** :
- `GET /api/rules`
- `GET /api/rules/local`
- `GET /api/rules/scenerules`
- `POST /api/rules/download`
- `DELETE /api/rules/:id`

**Users** :
- `GET /api/users`
- `POST /api/users`
- `PUT /api/users/:id`
- `DELETE /api/users/:id`
- `POST /api/users/:id/groups`
- `POST /api/users/:id/roles`

**Roles** :
- `GET /api/roles`
- `POST /api/roles`
- `PUT /api/roles/:id`
- `DELETE /api/roles/:id`
- `GET /api/roles/:id/permissions`
- `PUT /api/roles/:id/permissions`

**Action** : Créer document API complet (OpenAPI/Swagger).

---

### Q6.3 : Services Métier
**Question** : Quels services métier doivent être créés ?

**Contexte** :
- Architecture en services pour séparation logique
- Réutilisabilité

**Réponses suggérées** :
**Services Must Have** :
- `PackagingService` : Logique packaging
- `MetadataService` : Extraction/enrichissement métadonnées
- `RuleService` : Gestion rules (locales + scenerules.org)
- `TemplateService` : Rendu templates NFO
- `FtpUploadService` : Upload FTP/SFTP
- `JobService` : Gestion jobs
- `AuthService` : Logique authentification

**Structure** :
```python
web/services/packaging.py
class PackagingService:
    def package_ebook(self, file_path, group, rule):
        # Logique packaging
        pass
    
    def package_tv(self, file_path, group, rule):
        pass
```

**Action** : Créer interfaces/services de base.

---

## 7. Base de Données

### Q7.1 : Schéma MySQL Exact
**Question** : Quel est le schéma MySQL complet ?

**Contexte** :
- CDC mentionne MySQL 8.0+ InnoDB
- Modèles décrits mais pas schéma SQL

**✅ Schéma final confirmé** :
```sql
-- Users
users (id, username, note, password_hash, active, modify_at, created_at, created_by)

-- Roles & Permissions
roles (id, name, description, created_at)
permissions (id, role_id, resource, action, created_at)

-- Groups
groups (id, name, description, created_at)
user_groups (user_id, group_id)

-- Releases & Jobs
releases (id, user_id, group_id, release_type, status, created_at)
jobs (id, release_id, status, config_json, logs, created_at, created_by)

-- Rules
rules (id, name, content, scene, section, year, created_at)

-- Configurations
api_configs (id, name, api_key_encrypted, user_id, created_at)
destinations (id, name, host, port, user, password_encrypted, user_id)
```

**Modifications** :
- ✅ Users : Ajout `note`, `modify_at`, `created_by`
- ✅ Jobs : Ajout `created_by`

**Action** : Créer migrations Flask-Migrate avec schéma complet.

---

### Q7.2 : Migrations Database
**Question** : Comment gérer les migrations v2 ?

**Contexte** :
- Flask-Migrate configuré
- Schéma évoluera

**Réponses suggérées** :
- **Workflow** :
  1. Créer migration initiale (Phase 1)
  2. Migrations incrémentales par feature
  3. Tests migrations up/down
  4. Versioning migrations

**Action** : Configurer Flask-Migrate, créer première migration.

---

## 8. Sécurité et Permissions

### Q8.1 : Système Permissions Granulaire
**Question** : Comment implémenter permissions READ/WRITE/MOD par option ?

**Contexte** :
- CDC mentionne permissions granulaires
- Matrice permissions complexe

**Réponses suggérées** :
**Structure** :
```python
# Permission model
Permission:
    resource: "releases" | "rules" | "users" | "roles" | "config"
    action: "READ" | "WRITE" | "MOD" | "DELETE"

# Vérification
@require_permission("releases", "WRITE")
def create_release():
    pass
```

**Décorateur** :
```python
def require_permission(resource: str, action: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.has_permission(resource, action):
                return jsonify({"error": "Forbidden"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
```

**Action** : Implémenter système permissions avec tests.

---

### Q8.2 : Chiffrement Credentials
**Question** : Quel algorithme exact pour chiffrement ?

**Contexte** :
- CDC mentionne Fernet/AES-GCM
- v1 utilise Fernet

**Réponses suggérées** :
- **Fernet** (v1) :
  - ✅ Simple, symétrique
  - ✅ Bon pour credentials
- **AES-GCM** :
  - ✅ Plus moderne
  - ✅ Authentification intégrée
  - ❌ Plus complexe

**Recommandation** : **Fernet** pour rester compatible v1 et simplicité.

---

## 9. Déploiement et Infrastructure

### Q9.1 : Environnement Production
**Question** : Configuration exacte production ?

**Contexte** :
- DEPLOYMENT_PLAN existe mais général
- Besoin détails spécifiques

**✅ Configuration production confirmée** :
- **Serveur** : Dédié Debian 12 avec Docker/Docker Compose
- **OS** : Linux Debian 12
- **Web Server** : Nginx + Gunicorn ou uWSGI (peu importe, mais dans Docker)
- **Process Manager** : Supervisor dans Docker
- **Monitoring** : Prometheus, Grafana (le mieux)
- **Logs** : ELK stack ET simple fichiers (les deux)

**Architecture** : Tout containerisé avec Docker Compose pour facilité déploiement et maintenance.

---

### Q9.2 : CI/CD Pipeline
**Question** : Pipeline CI/CD nécessaire ?

**Contexte** :
- Definition of Done mentionne CI/CD
- Pas de configuration actuelle

**Réponses suggérées** :
- **GitHub Actions** :
  - ✅ Gratuit
  - ✅ Intégré GitHub
- **GitLab CI** :
  - ✅ Intégré GitLab
- **Jenkins** :
  - ✅ Flexible
  - ❌ Plus complexe

**Pipeline suggéré** :
1. Tests unitaires
2. Tests intégration
3. Coverage check (≥90%)
4. Linters
5. Build
6. Déploiement (staging/prod)

**Action** : Configurer GitHub Actions pour CI.

---

## 10. Tests et Qualité

### Q10.1 : Tests E2E Wizard
**Question** : Comment tester le wizard 9 étapes complet ?

**Contexte** :
- Wizard complexe, beaucoup d'étapes
- Tests E2E nécessaires

**Réponses suggérées** :
**Avec Playwright MCP** :
```python
def test_wizard_complete_flow():
    # 1. Login
    mcp_playwright_browser_navigate(url="http://localhost:5000/login")
    mcp_playwright_browser_type(...)  # Username
    mcp_playwright_browser_type(...)  # Password
    mcp_playwright_browser_click(...)  # Login
    
    # 2. Naviguer vers wizard
    mcp_playwright_browser_navigate(url="http://localhost:5000/releases/new")
    
    # 3. Étape 1 : Groupe
    # ... toutes les étapes ...
    
    # 9. Valider completion
    mcp_playwright_browser_wait_for(text="Release created")
```

**Scénarios à tester** :
- Flow complet normal
- Navigation backward/forward
- Validation chaque étape
- Gestion erreurs
- Sauvegarde/reprise

**Action** : Créer tests E2E wizard avec Playwright MCP.

---

### Q10.2 : Tests Performance
**Question** : Quels tests de performance nécessaires ?

**Contexte** :
- CDC mentionne performance optimisée
- Pas de critères précis

**Réponses suggérées** :
- **Backend** :
  - Temps réponse API < 200ms (p95)
  - Requêtes DB optimisées
- **Frontend** :
  - First Contentful Paint < 1s
  - Time to Interactive < 2s
- **Packaging** :
  - Packaging petit fichier < 30s
  - Packaging gros fichier < 5min

**Action** : Définir benchmarks précis, créer tests performance.

---

## 📋 Questions Prioritaires (Must Answer Before Phase 1)

### 🔴 Critique - À Répondre Immédiatement

1. **Q2.2** : Détails Wizard 9 Étapes → **Créer PRD-002 détaillé**
2. **Q6.1** : Modèles Base de Données → **Créer diagramme ERD**
3. **Q6.2** : Endpoints API → **Créer document API complet**
4. **Q4.3** : Gestion État Wizard → **Décision architecture**
5. **Q1.2** : Migration Progressive → **Stratégie claire**

### 🟡 Important - À Répondre Avant Phase 2

6. **Q5.1** : Setup React → **Décision outil build**
7. **Q5.2** : Routing Frontend → **Structure routes**
8. **Q4.2** : TypeScript → **Décision maintenant ou plus tard**
9. **Q8.1** : Permissions Granulaire → **Implémentation**

### 🟢 Optionnel - À Répondre Plus Tard

10. **Q9.1** : Production → **Détails déploiement**
11. **Q10.2** : Performance → **Benchmarks**

---

## 📝 Actions Immédiates Recommandées

### Avant Phase 1

1. **Créer PRD-002** : Nouvelle Release Wizard (détails 9 étapes)
2. **Créer PRD-003 à PRD-007** : Autres fonctionnalités
3. **Créer diagramme ERD** : Schéma base de données complet
4. **Créer document API** : OpenAPI/Swagger avec tous endpoints
5. **Audit code v1** : Identifier code à réutiliser vs refaire

### Pendant Phase 1

6. **Décisions techniques** : TypeScript, state management, etc.
7. **Setup React** : Vite + structure initiale
8. **Modèles DB** : Créer migrations initiales

---

## 🔗 Références

- **CDC** : `docs/cdc.md`
- **DEVBOOK** : `docs/DEVBOOK.md`
- **v1/** : Code référence
- **PRDs** : `docs/PRDs/`

---

---

## 📝 Récapitulatif des Décisions Prises

### ✅ Architecture et Structure
- **Q1.1** : Structure Frontend React modulaire (Option 1) - TypeScript dès le début
- **Q1.2** : **Tout refaire from scratch** en s'inspirant de v1 (pas de réutilisation directe)
- **Q1.3** : Structure Backend Flask confirmée (blueprints modulaires)

### ✅ Fonctionnalités
- **Q2.1** : Créer tous les PRDs (PRD-002 à PRD-007)
- **Q2.2** : Wizard 9 étapes détaillé avec spécifications complètes
  - EBOOK en priorité, autres types après confirmation
  - Barre progression, prévisualisation temps réel, validation complète
- **Q2.3** : Fonctionnalités v1 à reprendre identifiées (packaging, métadonnées, etc.)

### ✅ Intégration v1 → v2
- **Q3.1** : Utiliser v1 uniquement comme référence/exemples (pas de réutilisation code)
- **Q3.2** : Nouvelle base v2, pas de migration (fresh start)

### ✅ Décisions Techniques
- **Q4.1** : Context API pour commencer (Redux si besoin performance)
- **Q4.2** : **TypeScript dès le début**
- **Q4.3** : Hybride (localStorage + backend draft)
- **Q4.4** : Format templates NFO confirmé, Placeholders progressifs selon tests

### ✅ Frontend React
- **Q5.1** : **Vite** confirmé (recherche Context7 nécessaire pour config)
- **Q5.2** : Routes React confirmées
- **Q5.3** : Composants Wizard identifiés
- **Q5.4** : Auth React avec Context + ProtectedRoute

### ✅ Backend Flask
- **Q6.1** : Modèles DB identifiés (User, Role, Permission, Group, Release, Job, Rule)
- **Q6.2** : Endpoints API listés (à documenter OpenAPI/Swagger)
- **Q6.3** : Services métier identifiés (7 services Must Have)

### ✅ Base de Données
- **Q7.1** : Schéma MySQL complet confirmé (avec `note`, `modify_at`, `created_by`)
- **Q7.2** : Migrations Flask-Migrate configurées

### ✅ Sécurité
- **Q8.1** : Système permissions granulaires (READ/WRITE/MOD/DELETE)
- **Q8.2** : Fernet pour chiffrement credentials

### ✅ Déploiement
- **Q9.1** : **Docker/Docker Compose** sur Debian 12 (Prometheus/Grafana, ELK + fichiers)
- **Q9.2** : GitHub Actions pour CI/CD

### ✅ Tests
- **Q10.1** : Tests E2E Wizard avec Playwright MCP
- **Q10.2** : Benchmarks performance définis

---

## 🎯 Actions Immédiates Prioritaires

### 🔴 Critique (Avant Phase 1)

1. **✅ Créer PRD-002** : Nouvelle Release Wizard (9 étapes détaillées avec toutes spécifications)
2. **✅ Créer PRD-003 à PRD-007** : Liste Releases, Rules, Users, Roles, Config
3. **✅ Créer diagramme ERD** : Schéma base de données complet
4. **✅ Rechercher Vite setup** : Avec Context7 MCP pour confirmer React+TypeScript+Vite
5. **✅ Créer document API** : OpenAPI/Swagger avec tous endpoints

### 🟡 Important (Pendant Phase 1)

6. **Setup React** : Vite + TypeScript + structure initiale
7. **Modèles DB** : Créer migrations Flask-Migrate initiales
8. **Décisions architecture** : Finaliser state management, routing

### 🟢 Optionnel (Plus tard)

9. **Production** : Détails déploiement Docker
10. **Performance** : Benchmarks et tests

---

**Dernière mise à jour** : 2025-11-01  
**Statut** : ✅ Toutes les questions ont reçu des réponses  
**Prochaine étape** : Créer PRD-002 et documents techniques manquants

