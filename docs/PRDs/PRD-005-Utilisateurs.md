# PRD-005 : Utilisateurs

**ID** : PRD-005  
**Version** : 1.0.0  
**Date** : 2025-11-01  
**Statut** : Draft  
**Auteur** : Dev Team

---

## Vue d'Ensemble

Interface de gestion des utilisateurs permettant la création, modification, suppression et affectation de groupes et rôles aux utilisateurs, avec gestion des permissions granulaires.

**Priorité MoSCoW** : Must Have

**Phase** : Phase 6 (après Rules)

---

## User Stories

### US-005-001 : Liste Utilisateurs
**En tant que** administrateur  
**Je veux** voir la liste de tous les utilisateurs  
**Afin de** gérer les accès et permissions

**Critères d'acceptation** :
- Affichage tous utilisateurs
- Informations : Username, groupes, rôles, statut (actif/inactif)
- Recherche textuelle
- Filtrage par statut, rôle, groupe
- Tri par nom, date création

### US-005-002 : Création Utilisateur
**En tant que** administrateur  
**Je veux** créer un nouvel utilisateur  
**Afin de** donner accès à un nouvel opérateur

**Critères d'acceptation** :
- Formulaire création avec validation
- Champs : Username, password, note, statut actif
- Validation username unique
- Validation password (force minimale)
- Création avec confirmation

### US-005-003 : Modification Utilisateur
**En tant que** administrateur  
**Je veux** modifier un utilisateur existant  
**Afin de** mettre à jour ses informations

**Critères d'acceptation** :
- Formulaire édition pré-rempli
- Champs éditables : Note, password (optionnel), statut actif
- Validation avant sauvegarde
- Historique modifications (audit trail)

### US-005-004 : Suppression Utilisateur
**En tant que** administrateur  
**Je veux** supprimer ou désactiver un utilisateur  
**Afin de** retirer l'accès

**Critères d'acceptation** :
- Bouton "Supprimer" ou "Désactiver"
- Confirmation suppression/désactivation (modal)
- Option suppression définitive ou désactivation
- Vérification utilisations (releases créées, etc.)
- Log suppression tracé

### US-005-005 : Affectation Groupe
**En tant que** administrateur  
**Je veux** affecter un groupe à un utilisateur  
**Afin de** définir ses groupes Scene autorisés

**Critères d'acceptation** :
- Sélecteur groupes disponibles
- Multi-select si plusieurs groupes
- Sauvegarde affectations
- Liste groupes affectés affichée
- Possibilité retirer groupe

### US-005-006 : Affectation Rôle
**En tant que** administrateur  
**Je veux** affecter un rôle à un utilisateur  
**Afin de** définir ses permissions

**Critères d'acceptation** :
- Sélecteur rôles disponibles
- Sélection unique (un rôle par utilisateur)
- Sauvegarde affectation
- Affichage rôle actuel
- Possibilité changer rôle

### US-005-007 : Configuration Permissions Utilisateur
**En tant que** administrateur  
**Je veux** configurer les droits READ/WRITE/MOD pour chaque option d'un utilisateur  
**Afin de** personnaliser ses permissions

**Critères d'acceptation** :
- Matrice permissions par option :
  - Nouvelle Release : READ/WRITE/MOD
  - Liste Releases : READ/WRITE/MOD
  - Rules : READ/WRITE/MOD
  - Utilisateurs : READ/WRITE/MOD
  - Rôles : READ/WRITE/MOD
  - Configurations : READ/WRITE/MOD
- Cases à cocher pour chaque permission
- Sauvegarde permissions
- Héritage permissions depuis rôle (baseline)

### US-005-008 : Détail Utilisateur
**En tant que** administrateur  
**Je veux** voir le détail complet d'un utilisateur  
**Afin de** consulter toutes ses informations et permissions

**Critères d'acceptation** :
- Page détail avec toutes informations
- Groupes associés listés
- Rôle assigné avec permissions
- Permissions personnalisées affichées
- Historique actions (releases créées, etc.)
- Date création, dernière connexion

---

## Détails Fonctionnels

### Interface Liste Utilisateurs

**Layout** :
- Tableau avec colonnes : Username, Groupes, Rôle, Statut, Actions
- Pagination si > 20 utilisateurs
- Recherche barre supérieure
- Filtres sidebar ou barre supérieure

**Informations Affichées** :
- **Username** : Nom d'utilisateur (lien vers détail)
- **Groupes** : Badges groupes affectés (multi)
- **Rôle** : Rôle assigné (badge coloré)
- **Statut** : Actif/Inactif (badge)
- **Actions** : Éditer, Supprimer (icônes)

**Recherche et Filtres** :
- **Recherche** : Dans username
- **Filtres** :
  - Statut (Actif, Inactif)
  - Rôle (sélecteur multi)
  - Groupe (sélecteur multi)
- **Tri** : Par username (A-Z), date création

### Création Utilisateur

**Formulaire** :
- **Username** : Input texte (validation unique, min 3 chars, max 100)
- **Password** : Input password (force minimale : 8 chars, majuscule, chiffre)
- **Note** : Textarea (optionnel, max 500 chars)
- **Statut actif** : Checkbox (activé par défaut)

**Validation** :
- Username unique en base
- Password force suffisante
- Messages erreur clairs

**Création** :
- Sauvegarde en base
- Confirmation succès
- Redirection vers liste ou détail

### Modification Utilisateur

**Formulaire Édition** :
- Champs pré-remplis (sauf password)
- **Note** : Éditable
- **Password** : Input optionnel (changement si rempli)
- **Statut actif** : Checkbox

**Validation** :
- Même validation que création

**Sauvegarde** :
- Mise à jour en base
- Historique modifications (audit trail)
- Confirmation succès

### Affectation Groupes

**Interface** :
- Liste groupes disponibles (table `groups`)
- Multi-select groupes
- Badges groupes affectés affichés
- Bouton "Retirer" sur chaque groupe affecté

**Actions** :
- Ajout groupe : Sélection depuis liste
- Retrait groupe : Clic sur badge "Retirer"
- Sauvegarde modifications

**Permissions** :
- Groupes affectés déterminent releases accessibles
- Filtrage automatique dans Liste Releases (PRD-003)

### Affectation Rôle

**Interface** :
- Sélecteur rôles disponibles (table `roles`)
- Sélection unique (radio ou select)
- Rôle actuel affiché et surligné

**Actions** :
- Changement rôle : Sélection nouveau rôle
- Sauvegarde affectation
- Mise à jour permissions (baseline depuis rôle)

**Permissions** :
- Rôle détermine permissions baseline
- Permissions personnalisables ensuite (US-005-007)

### Configuration Permissions Granulaires

**Matrice Permissions** :
- **Options disponibles** :
  1. Nouvelle Release (Wizard)
  2. Liste Releases
  3. Rules (locales/distantes)
  4. Utilisateurs
  5. Rôles
  6. Configurations

- **Niveaux de droits** :
  - **READ** : Lecture seule
  - **WRITE** : Création/écriture
  - **MOD** : Modification/édition/suppression

**Interface** :
- Tableau avec options en lignes, permissions en colonnes
- Cases à cocher pour chaque permission
- Héritage permissions depuis rôle (baseline, grisé mais visible)
- Permissions personnalisées (éditables, surlignées)

**Logique** :
- Permissions depuis rôle = baseline
- Permissions personnalisées = override baseline
- Sauvegarde permissions finales

---

## Contraintes Techniques

### Frontend

**Technologies** :
- React 18+ avec TypeScript
- React Router v6
- Bootstrap 5
- Formik ou React Hook Form pour formulaires

**Composants** :
- `UserList` : Liste utilisateurs
- `UserCard` : Card utilisateur (si vue cards)
- `UserCreate` : Formulaire création
- `UserEdit` : Formulaire édition
- `UserDetail` : Page détail
- `UserGroups` : Gestion groupes utilisateur
- `UserRoles` : Gestion rôles utilisateur
- `UserPermissions` : Matrice permissions

**Performance** :
- Chargement liste : < 1s
- Recherche : < 300ms

### Backend

**Endpoints API** :
- `GET /api/users` : Liste utilisateurs (avec filtres, recherche, pagination)
- `GET /api/users/:id` : Détail utilisateur
- `POST /api/users` : Création utilisateur
- `PUT /api/users/:id` : Modification utilisateur
- `DELETE /api/users/:id` : Suppression/désactivation utilisateur
- `POST /api/users/:id/groups` : Affectation groupes
- `DELETE /api/users/:id/groups/:group_id` : Retrait groupe
- `POST /api/users/:id/roles` : Affectation rôle
- `PUT /api/users/:id/permissions` : Configuration permissions granulaires
- `GET /api/users/:id/permissions` : Récupération permissions

**Base de Données** :
- Table `users` : id, username, note, password_hash, active, modify_at, created_at, created_by
- Table `user_groups` : user_id, group_id (many-to-many)
- Table `user_permissions` : user_id, resource, action (permissions personnalisées)

**Permissions** :
- Endpoints protégés admin uniquement
- Vérification permission admin sur chaque action

**Sécurité** :
- Password hashé avec werkzeug (PBKDF2)
- Validation strict inputs
- Audit trail (created_by, modify_at)

**Performance** :
- Temps réponse liste : < 200ms
- Création/modification : < 500ms

---

## Tests (TDD)

### Tests Unitaires Frontend

```typescript
describe('UserList', () => {
  it('should display all users', () => {
    // Test affichage liste
  });
  
  it('should filter users by role and status', () => {
    // Test filtres combinés
  });
});

describe('UserCreate', () => {
  it('should validate username uniqueness', () => {
    // Test validation username unique
  });
  
  it('should validate password strength', () => {
    // Test force password
  });
});

describe('UserPermissions', () => {
  it('should display permissions matrix', () => {
    // Test affichage matrice
  });
  
  it('should inherit permissions from role', () => {
    // Test héritage baseline
  });
});
```

### Tests Backend

```python
def test_create_user():
    """Test création utilisateur."""
    # Test création avec validation

def test_create_user_duplicate_username():
    """Test création utilisateur username dupliqué."""
    # Test validation username unique

def test_assign_groups():
    """Test affectation groupes utilisateur."""
    # Test affectation multi-groupes

def test_assign_role():
    """Test affectation rôle utilisateur."""
    # Test affectation rôle unique

def test_custom_permissions():
    """Test permissions personnalisées."""
    # Test override permissions rôle
```

### Tests E2E (Playwright MCP)

```python
def test_user_management_e2e():
    """Test gestion utilisateurs E2E avec Playwright MCP."""
    # Login admin
    mcp_playwright_browser_navigate(url="http://localhost:5000/login")
    mcp_playwright_browser_type(element="username", text="admin")
    mcp_playwright_browser_type(element="password", text="password")
    mcp_playwright_browser_click(element="login button")
    
    # Naviguer vers users
    mcp_playwright_browser_navigate(url="http://localhost:5000/users")
    mcp_playwright_browser_snapshot()
    
    # Créer utilisateur
    mcp_playwright_browser_click(element="create user button")
    mcp_playwright_browser_type(element="username", text="newuser")
    mcp_playwright_browser_type(element="password", text="SecurePass123")
    mcp_playwright_browser_click(element="save button")
    mcp_playwright_browser_wait_for(text="User created")
    
    # Affecter groupe
    mcp_playwright_browser_click(element="edit user button")
    mcp_playwright_browser_click(element="assign groups button")
    mcp_playwright_browser_click(element="group checkbox")
    mcp_playwright_browser_click(element="save button")
    mcp_playwright_browser_wait_for(text="Groups assigned")
```

---

## Critères de Réussite

### Fonctionnels
- ✅ Liste utilisateurs fonctionnelle
- ✅ Création utilisateur avec validation
- ✅ Modification utilisateur fonctionnelle
- ✅ Suppression/désactivation fonctionnelle
- ✅ Affectation groupes fonctionnelle
- ✅ Affectation rôle fonctionnelle
- ✅ Configuration permissions granulaires fonctionnelle

### Performance
- Chargement liste : < 1s
- Recherche : < 300ms
- Création/modification : < 500ms

### Qualité
- Accessibilité WCAG 2.2 AA
- Responsive design
- Tests couverture 100%
- Sécurité : Password hashé, validation strict

---

## Dépendances

- **Phase 1** : Infrastructure Core (JWT, DB, Models)
- **PRD-006** : Rôles (rôles à affecter)

---

**Liens** :
- [Backlog Agile](../BACKLOG_AGILE.md)
- [Test Plan](../TEST_PLAN.md)
- [DEVBOOK](../DEVBOOK.md)
- [CDC](../cdc.md)

