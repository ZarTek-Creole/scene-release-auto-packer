# 🧪 Test Plan - eBook Scene Packer v2

**Date de création** : 2025-11-01  
**Méthodologie** : TDD (Test Driven Development) strict  
**Objectif couverture** : 100%

---

## 🎯 Objectifs

- **Couverture** : 100% du code source
- **Types** : Unitaires, Intégration, E2E
- **Approche** : TDD (Red → Green → Refactor)
- **Outils** : pytest, pytest-cov, Playwright

---

## 📋 Stratégie de Tests

### Pyramide de Tests
```
        /\
       /  \      E2E (10%)
      /____\
     /      \    Intégration (20%)
    /________\
   /          \  Unitaires (70%)
  /____________\
```

### Types de Tests

#### 1. Tests Unitaires (70%)
**Objectif** : Tester fonctions/méthodes isolées  
**Outils** : pytest, unittest.mock  
**Temps** : < 1s par test

**Exemples** :
- Fonctions utilitaires
- Méthodes de modèles
- Composants React isolés

#### 2. Tests d'Intégration (20%)
**Objectif** : Tester interactions entre composants  
**Outils** : pytest, Flask test client  
**Temps** : < 5s par test

**Exemples** :
- API endpoints avec DB
- Services avec dépendances
- Flux complets backend

#### 3. Tests E2E (10%)
**Objectif** : Tester flux utilisateur complets  
**Outils** : Playwright, Selenium  
**Temps** : < 30s par test

**Exemples** :
- Création release complète
- Login/logout
- Navigation entre pages

---

## 🔧 Outils et Configuration

### Backend (Python)
```python
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=web
    --cov=src
    --cov-report=html
    --cov-report=term
    -v
```

### Frontend (React)
```javascript
// Jest configuration
module.exports = {
  testEnvironment: 'jsdom',
  coverageThreshold: {
    global: {
      branches: 100,
      functions: 100,
      lines: 100,
      statements: 100
    }
  }
};
```

### E2E (Playwright)
```javascript
// playwright.config.js
module.exports = {
  testDir: './tests/e2e',
  use: {
    baseURL: 'http://localhost:5000',
  },
};
```

---

## 📝 Scénarios de Test par Fonctionnalité

### Infrastructure Core

#### Authentification JWT
**Tests Unitaires** :
- `test_hash_password()` : Hash mot de passe
- `test_verify_password()` : Vérification mot de passe
- `test_generate_token()` : Génération token
- `test_verify_token()` : Vérification token

**Tests Intégration** :
- `test_login_endpoint()` : POST /api/auth/login
- `test_refresh_endpoint()` : POST /api/auth/refresh
- `test_protected_route()` : Protection route JWT

**Tests E2E** :
- Login complet (formulaire → redirection)
- Refresh token automatique
- Logout

#### Modèles Database
**Tests Unitaires** :
- `test_create_user()` : Création utilisateur
- `test_user_relations()` : Relations user/role
- `test_permission_check()` : Vérification permission

**Tests Intégration** :
- `test_user_crud()` : CRUD complet utilisateur
- `test_role_assign()` : Assignation rôle

---

### Interface Administration

#### Dashboard
**Tests Unitaires** :
- `test_dashboard_component()` : Rendu composant
- `test_stats_display()` : Affichage stats

**Tests Intégration** :
- `test_dashboard_api()` : GET /api/dashboard/stats
- `test_dashboard_auth()` : Authentification requise

**Tests E2E** :
- Chargement dashboard
- Affichage stats correctes

#### Navigation
**Tests Unitaires** :
- `test_nav_component()` : Rendu navigation
- `test_active_tab()` : Onglet actif

**Tests E2E** :
- Navigation entre toutes pages
- État actif correct

#### Thème Jour/Nuit
**Tests Unitaires** :
- `test_theme_toggle()` : Bascule thème
- `test_theme_persistence()` : Persistance localStorage

**Tests E2E** :
- Bascule thème fonctionnelle
- Préférence sauvegardée

---

### Nouvelle Release Wizard

#### Étape 1 : Groupe
**Tests Unitaires** :
- `test_group_validation()` : Validation groupe
- `test_group_component()` : Composant formulaire

**Tests Intégration** :
- `test_group_save()` : Sauvegarde groupe en session

**Tests E2E** :
- Saisie groupe → validation → étape suivante

#### Étape 2 : Type Release
**Tests Unitaires** :
- `test_type_validation()` : Validation type
- `test_type_options()` : Options disponibles

**Tests E2E** :
- Sélection type → étape suivante

#### Étape 3 : Règle
**Tests Intégration** :
- `test_rules_filter()` : Filtrage règles par type
- `test_rule_selection()` : Sélection règle

**Tests E2E** :
- Affichage règles → sélection → étape suivante

*(Étapes suivantes similaires)*

---

## 🎯 Critères de Validation

### Par Type de Test

#### Tests Unitaires
- ✅ Exécution < 1s
- ✅ Isolation complète (mocks)
- ✅ Couverture 100% fonction testée

#### Tests Intégration
- ✅ Exécution < 5s
- ✅ Base de données test isolée
- ✅ Nettoyage après chaque test

#### Tests E2E
- ✅ Exécution < 30s
- ✅ Navigateur réel (Chrome/Firefox)
- ✅ Scénarios utilisateur complets

---

## 📊 Reporting

### Coverage Reports
- **Format HTML** : `htmlcov/index.html`
- **Format Terminal** : Affichage inline
- **Seuil** : 100% requis pour merge

### Test Reports
- **Format JUnit** : `tests/results/junit.xml`
- **Format HTML** : `tests/results/report.html`

---

## 🔄 Processus TDD

### Cycle Red-Green-Refactor

1. **Red** : Écrire test qui échoue
   ```python
   def test_create_user():
       user = User(username='test')
       assert user.id is None  # Pas encore créé
   ```

2. **Green** : Implémenter code minimal pour passer
   ```python
   def create_user(username):
       user = User(username=username)
       db.session.add(user)
       db.session.commit()
       return user
   ```

3. **Refactor** : Améliorer code
   ```python
   def create_user(username, note=None):
       user = User(username=username, note=note)
       db.session.add(user)
       db.session.commit()
       return user
   ```

4. **Vérifier** : Tous tests passent toujours

---

## 🚀 Exécution

### Commandes

```bash
# Tests unitaires backend
pytest tests/unit/

# Tests intégration backend
pytest tests/integration/

# Tests E2E
playwright test

# Coverage
pytest --cov=web --cov=src

# Tests frontend
npm test

# Tous tests
pytest && npm test && playwright test
```

---

## 📋 Checklist Tests

### Avant Merge
- [ ] Tous tests passent
- [ ] Couverture 100%
- [ ] Tests E2E passent
- [ ] Pas de tests flaky
- [ ] Documentation tests à jour

### Avant Release
- [ ] Tests performance passent
- [ ] Tests sécurité passent
- [ ] Tests accessibilité passent
- [ ] Smoke tests production passent

---

## 🔗 Liens

- **CDC** : `docs/cdc.md`
- **DEVBOOK** : `docs/DEVBOOK.md`
- **PRDs** : `docs/PRDs/`

---

**Dernière mise à jour** : 2025-11-01  
**Maintenu par** : Équipe QA/Développement

