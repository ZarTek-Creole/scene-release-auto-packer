# 🎯 Project Overview - eBook Scene Packer v2

**Date de création** : 2025-11-01  
**Version** : 2.0.0

---

## 🌟 Vision

Créer une application web moderne et robuste pour le packaging de releases Scene (EBOOK, TV, DOCS), avec une architecture propre, une couverture de tests à 100%, et une interface d'administration complète et intuitive.

**Inspiration** : Version v1 conservée dans `v1/` comme référence technique et fonctionnelle.

---

## 📐 Portée

### In Scope (Dans le périmètre)
- ✅ Interface d'administration complète
- ✅ Wizard 9 étapes pour création release
- ✅ Gestion releases (liste, édition, corrections)
- ✅ Gestion rules Scene (locales et scenerules.org)
- ✅ Gestion utilisateurs, rôles, permissions
- ✅ Configuration système, APIs, FTP/SSH
- ✅ Tests TDD avec couverture 100%
- ✅ Documentation exhaustive

### Out of Scope (Hors périmètre)
- ❌ CLI (prévu pour phase ultérieure)
- ❌ API publique (prévu pour phase ultérieure)
- ❌ Support multi-tenants (prévu pour phase ultérieure)
- ❌ Mobile app (hors périmètre v2)

---

## 🏗️ Architecture

### Stack Technologique
- **Frontend** : React 18+ (TypeScript recommandé)
- **Backend** : Flask (Python 3.11+)
- **Database** : MySQL 8.0+ (InnoDB)
- **Styling** : Bootstrap 5
- **API** : RESTful JSON

### Architecture Applicative
```
┌─────────────────────────────────────────┐
│         Frontend (React)                 │
│  - Components                            │
│  - Context API / Redux                   │
│  - React Router                          │
└────────────────┬─────────────────────────┘
                 │
                 │ HTTP/REST API (JWT)
                 │
┌────────────────▼─────────────────────────┐
│         Backend (Flask)                   │
│  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │Blueprints│  │ Services │  │ Models  ││
│  └──────────┘  └──────────┘  └─────────┘│
└────────────────┬─────────────────────────┘
                 │
                 │ SQLAlchemy ORM
                 │
┌────────────────▼─────────────────────────┐
│      Database (MySQL)                    │
│  - Users, Roles, Permissions             │
│  - Releases, Jobs                        │
│  - Rules, Configurations                 │
└─────────────────────────────────────────┘
```

---

## 📅 Phases Principales

### Phase 0 : Préparation (1 semaine)
- Backup v1/
- Documentation structurée
- Environnement développement
- Setup TDD
- Règles Cursor

### Phase 1 : Infrastructure Core (2 semaines)
- Flask app factory
- MySQL database
- JWT authentication
- Models de base

### Phase 2 : Interface Administration (3 semaines)
- Dashboard
- Navigation
- Structure pages
- Thème jour/nuit

### Phase 3 : Nouvelle Release Wizard (4 semaines)
- Étapes 1-9 du wizard
- Analyse fichiers
- Enrichissement APIs
- Packaging

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

**Total** : ~20 semaines (~5 mois)

---

## 🎯 Méthodologies

### TDD (Test Driven Development)
- **Obligatoire** pour tout développement
- **Cycle** : Red → Green → Refactor
- **Couverture** : Objectif 100%
- **Outils** : pytest, pytest-cov

### MoSCoW (Priorisation)
- **Must Have** : Fonctionnalités essentielles
- **Should Have** : Fonctionnalités importantes
- **Could Have** : Fonctionnalités souhaitables
- **Won't Have** : Fonctionnalités exclues

### SWOT (Analyse)
- Analyse forces/faiblesses/opportunités/menaces
- Pour chaque Epic majeur
- Lié aux User Stories

### Backlog Agile
- **Epics** : Grandes fonctionnalités
- **User Stories** : Besoins utilisateur
- **Tâches** : Tâches techniques
- **Sprints** : Itérations 2 semaines

### DMAIC (Optimisation)
- **Define** : Définir processus critiques
- **Measure** : Mesurer performance
- **Analyze** : Analyser données
- **Improve** : Améliorer processus
- **Control** : Contrôler et maintenir

### OKRs (Objectives and Key Results)
- Objectifs mesurables par phase
- Key Results pour validation
- Suivi dans DEVBOOK

### Matrice Eisenhower
- **Urgent & Important** : À faire immédiatement
- **Important, pas urgent** : À planifier
- **Urgent, pas important** : À déléguer
- **Ni urgent ni important** : À éliminer

---

## 👥 Équipe

### Rôles
- **Développeur Full-Stack** : Développement frontend/backend
- **DevOps** : Infrastructure, déploiement
- **QA** : Tests, qualité

### Responsabilités
- **Architecture** : Équipe technique
- **Design** : Équipe UX/UI
- **Documentation** : Équipe complète

---

## 📊 Métriques de Succès

### Techniques
- Couverture tests : 100%
- Temps chargement pages : < 2s
- Disponibilité : 99.9%
- Sécurité : 0 vulnérabilité critique

### Fonctionnels
- Toutes fonctionnalités Must Have implémentées
- Interface utilisateur intuitive
- Documentation complète
- Déploiement réussi

---

## 🔗 Documents Liés

- **CDC** : `docs/cdc.md` - Cahier des charges complet
- **DEVBOOK** : `docs/DEVBOOK.md` - Suivi phases et étapes
- **TodoList** : `docs/todolist.md` - Découpage détaillé
- **PRDs** : `docs/PRDs/` - Product Requirement Documents
- **Backlog** : `docs/BACKLOG_AGILE.md` - Backlog Agile
- **Test Plan** : `docs/TEST_PLAN.md` - Plan de tests
- **Risks** : `docs/RISKS_REGISTER.md` - Registre risques
- **Deployment** : `docs/DEPLOYMENT_PLAN.md` - Plan déploiement

---

**Dernière mise à jour** : 2025-11-01  
**Prochaine révision** : À chaque phase complétée

