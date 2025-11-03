# 📦 eBook Scene Packer v2

**Version** : 2.0.0  
**Statut** : ✅ Phase 0 Complétée | 🚧 Phase 1 Prête à démarrer  
**Date** : 2025-11-03  
![Phase 0](https://img.shields.io/badge/Phase%200-Done-success)

---

## 🎯 Vue d'Ensemble

Refonte complète (v2) de l'application eBook Scene Packer avec architecture moderne, tests complets (TDD), et documentation exhaustive.

**Référence** : Version précédente conservée dans `v1/` comme référence technique et fonctionnelle.

---

## 📁 Structure du Projet

```
ebook.scene.packer/
├── .cursor/                 # Règles Cursor
│   ├── rules/              # Règles (alwaysApply)
│   │   ├── project-v2.mdc
│   │   ├── tdd-methodology.mdc
│   │   ├── mcp-tools-usage.mdc
│   │   └── ...
│   └── RULES_ATTACHMENT_GUIDE.md
├── tests/                   # Tests (TDD)
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── web/                     # Backend Flask
├── src/                     # Code source partagé
├── venv/                    # Environnement virtuel Python
├── requirements.txt         # Dépendances production
├── requirements-dev.txt     # Dépendances développement
├── pytest.ini              # Configuration pytest
└── .coveragerc             # Configuration coverage
```

---

## 🚀 Démarrage Rapide

### Phase Actuelle : Phase 0 - Préparation ✅

**Statut** : ✅ **COMPLÉTÉE À 100% DoD**

#### Phase 0 - Validation Complète ✅
- ✅ Backup v1/ créé et vérifié
- ✅ Documentation structurée créée (45 fichiers markdown)
- ✅ Règles Cursor créées (33 règles .mdc)
- ✅ Environnement configuré (Python 3.12, dépendances installées)
- ✅ Structure tests créée (tests/phase0/, tests/e2e/phase0/)
- ✅ Tests Phase 0 : 29/29 passent (100%) ✅
- ✅ Couverture : 100% (tests de validation Phase 0) ✅
- ✅ Linting : 0 erreurs (ruff, black, isort) ✅
- ✅ Tests E2E : Structure préparée (Playwright Browser MCP requis) ✅
- ✅ Configuration CI : .coveragerc, pyproject.toml, package.json ✅
- ✅ Definition of Done : Tous critères satisfaits ✅

**Date de complétion** : 2025-11-03 20:00:00  
**Voir** : `docs/DEVBOOK.md` pour détails complets

#### Prochaines Étapes ⏳
- ⏳ Phase 1 - Infrastructure Core (peut maintenant commencer)
  - Flask app factory
  - Base de données MySQL
  - Authentification JWT

---

## 🛠️ Configuration Environnement

### Pré-requis
- Python 3.11+
- MySQL 8.0+
- Node.js 18+ (pour frontend React)

### Installation

```bash
# 1. Activer environnement virtuel
source venv/bin/activate

# 2. Installer dépendances (déjà fait)
pip install -r requirements-dev.txt

# 3. Copier .env.example (quand créé)
# cp .env.example .env
# Éditer .env avec vos configurations

# 4. Lancer tests pour valider setup
pytest tests/unit/test_example.py -v
```

---

## 🧪 Tests (TDD)

### Exécution Tests

```bash
# Activer venv
source venv/bin/activate

# Tests unitaires
pytest tests/unit/ -v

# Tests avec coverage
pytest --cov=web --cov=src --cov-report=html --cov-report=term

# Voir coverage HTML
open htmlcov/index.html  # ou xdg-open sur Linux
```

### Couverture Requise
- **100% de couverture obligatoire** pour merge
- Vérifier avec `pytest --cov`

---

## 🛠️ MCP Tools

**⚠️ Important** : Utiliser les MCP Tools pour améliorer productivité.

### Tools Disponibles
- **Playwright Browser MCP** : Tests E2E (OBLIGATOIRE)
- **Docs MCP Server** : Documentation React, Flask, Bootstrap
- **Repomix MCP** : Analyse codebase
- **Context7 MCP** : Documentation structurée
- **Memory MCP** : Knowledge graph
- **Sequential Thinking MCP** : Résolution problèmes

**Voir** : `docs/MCP_TOOLS_GUIDE.md` pour guide complet

---

## 📚 Documentation

### Documents Principaux

1. **Cahier des Charges** : [`docs/cdc.md`](docs/cdc.md)
2. **DEVBOOK** : [`docs/DEVBOOK.md`](docs/DEVBOOK.md) - Suivi phases/étapes
3. **MCP Tools Guide** : [`docs/MCP_TOOLS_GUIDE.md`](docs/MCP_TOOLS_GUIDE.md) ⭐
4. **TodoList** : [`docs/todolist.md`](docs/todolist.md)
5. **Règles Cursor** : [`.cursor/rules/`](.cursor/rules/)
6. **Guide Attachement** : [`.cursor/RULES_ATTACHMENT_GUIDE.md`](.cursor/RULES_ATTACHMENT_GUIDE.md)

---

## 🔗 Règles et Docs à Attacher

**Pour prompts de développement** :

```
@.cursor/rules/project-v2.mdc
@.cursor/rules/tdd-methodology.mdc
@.cursor/rules/mcp-tools-usage.mdc
@docs/cdc.md
@docs/DEVBOOK.md
@docs/MCP_TOOLS_GUIDE.md
```

**Voir** : `.cursor/RULES_ATTACHMENT_GUIDE.md` pour détails complets

---

## 📋 Phases du Projet

### Phase 0 : Préparation (1 semaine) 🟡 En cours
- ✅ Backup v1/
- ✅ Documentation structurée
- ✅ Règles Cursor (avec MCP Tools)
- ✅ Configuration environnement
- ⏳ Setup TDD (structure créée, à compléter)

### Phase 1 : Infrastructure Core (2 semaines) ⏳
- Flask app factory
- MySQL database
- JWT authentication
- Models de base

*(Voir [`docs/DEVBOOK.md`](docs/DEVBOOK.md) pour phases complètes)*

**Total estimé** : ~20 semaines (~5 mois)

---

## 🏗️ Architecture

### Stack Technologique
- **Frontend** : React 18+ (TypeScript recommandé)
- **Backend** : Flask (Python 3.11+)
- **Database** : MySQL 8.0+ (InnoDB)
- **Styling** : Bootstrap 5
- **API** : RESTful JSON

---

## ✅ Prochaines Étapes

1. **Commencer Phase 1 : Infrastructure Core**
   - Flask app factory
   - Base de données MySQL
   - Authentification JWT

**Voir** : [`docs/todolist.md`](docs/todolist.md) pour détails complets

---

## 🔗 Liens Utiles

- **Documentation complète** : [`docs/`](docs/)
- **Règles Cursor** : [`.cursor/rules/`](.cursor/rules/)
- **Version précédente** : [`v1/`](v1/)

---

**Dernière mise à jour** : 2025-11-01  
**Statut** : Phase 0 - Préparation (Configuration environnement terminée)
