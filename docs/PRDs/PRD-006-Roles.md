# PRD-006 : Rôles

**ID** : PRD-006  
**Version** : 1.0.0  
**Date** : 2025-11-01  
**Statut** : Draft  
**Auteur** : Dev Team

---

## Vue d'Ensemble

Système de gestion des rôles et permissions permettant la création, modification, suppression de rôles et la configuration des permissions granulaires (READ/WRITE/MOD) pour chaque option, avec affichage des utilisateurs par rôle.

**Priorité MoSCoW** : Must Have

**Phase** : Phase 6 (après Utilisateurs)

---

## User Stories

### US-006-001 : Liste Rôles
**En tant que** administrateur  
**Je veux** voir la liste de tous les rôles  
**Afin de** gérer les rôles et leurs permissions

**Critères d'acceptation** :
- Affichage tous rôles disponibles
- Informations : Nom, description, permissions, nombre utilisateurs
- Recherche textuelle
- Tri par nom, nombre utilisateurs

### US-006-002 : Création Rôle
**En tant que** administrateur  
**Je veux** créer un nouveau rôle  
**Afin de** définir un nouveau profil de permissions

**Critères d'acceptation** :
- Formulaire création avec validation
- Champs : Nom, description
- Validation nom unique
- Création rôle avec permissions par défaut (toutes READ)

### US-006-003 : Modification Rôle
**En tant que** administrateur  
**Je veux** modifier un rôle existant  
**Afin de** ajuster ses permissions

**Critères d'acceptation** :
- Formulaire édition pré-rempli
- Champs éditables : Nom, description, permissions
- Validation avant sauvegarde
- Mise à jour automatique permissions utilisateurs ayant ce rôle

### US-006-004 : Suppression Rôle
**En tant que** administrateur  
**Je veux** supprimer un rôle  
**Afin de** nettoyer les rôles obsolètes

**Critères d'acceptation** :
- Bouton "Supprimer" visible
- Vérification utilisateurs ayant ce rôle (avertissement)
- Confirmation suppression (modal)
- Option réassigner utilisateurs à autre rôle
- Log suppression tracé

### US-006-005 : Configuration Permissions Rôle
**En tant que** administrateur  
**Je veux** configurer les droits READ/WRITE/MOD pour chaque option d'un rôle  
**Afin de** définir les permissions baseline

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
- Mise à jour automatique utilisateurs ayant ce rôle

### US-006-006 : Liste Utilisateurs par Rôle
**En tant que** administrateur  
**Je veux** voir la liste des utilisateurs ayant un rôle spécifique  
**Afin de** gérer les affectations de rôles

**Critères d'acceptation** :
- Filtrage utilisateurs par rôle
- Liste utilisateurs avec rôle sélectionné
- Informations : Username, groupes
- Actions : Éditer, Changer rôle

### US-006-007 : Détail Rôle
**En tant que** administrateur  
**Je veux** voir le détail complet d'un rôle  
**Afin de** consulter toutes ses permissions et utilisateurs

**Critères d'acceptation** :
- Page détail avec toutes informations
- Permissions configurées affichées (matrice)
- Liste utilisateurs ayant ce rôle
- Historique modifications (audit trail)
- Date création

---

## Détails Fonctionnels

### Interface Liste Rôles

**Layout** :
- Tableau ou cards (toggle vue)
- Colonnes : Nom, Description, Permissions (résumé), Utilisateurs (compteur), Actions
- Pagination si > 20 rôles
- Recherche barre supérieure

**Informations Affichées** :
- **Nom** : Nom du rôle (lien vers détail)
- **Description** : Description du rôle
- **Permissions** : Résumé permissions (ex: "READ: All, WRITE: Releases/Rules")
- **Utilisateurs** : Nombre utilisateurs ayant ce rôle (lien vers liste)
- **Actions** : Éditer, Supprimer (icônes)

**Recherche et Tri** :
- Recherche textuelle dans nom, description
- Tri par nom (A-Z), nombre utilisateurs

### Création Rôle

**Formulaire** :
- **Nom** : Input texte (validation unique, min 3 chars, max 100)
- **Description** : Textarea (max 500 chars)
- **Permissions** : Matrice permissions (toutes READ par défaut)

**Validation** :
- Nom unique en base
- Nom non vide
- Messages erreur clairs

**Création** :
- Sauvegarde rôle en base
- Permissions par défaut (toutes READ)
- Confirmation succès
- Redirection vers édition permissions

### Modification Rôle

**Formulaire Édition** :
- Champs pré-remplis : Nom, description
- Matrice permissions éditables
- Bouton "Sauvegarder"

**Validation** :
- Même validation que création
- Vérification nom unique (si modifié)

**Sauvegarde** :
- Mise à jour rôle en base
- Mise à jour automatique permissions utilisateurs ayant ce rôle
- Historique modifications (audit trail)
- Confirmation succès

**Impact Utilisateurs** :
- Permissions baseline utilisateurs ayant ce rôle mises à jour
- Permissions personnalisées conservées (override)

### Suppression Rôle

**Vérifications** :
- Détection utilisateurs ayant ce rôle
- Avertissement si utilisateurs trouvés
- Option réassigner à autre rôle avant suppression

**Confirmation** :
- Modal confirmation avec liste utilisateurs affectés
- Option sélection nouveau rôle pour réassignation
- Confirmation suppression définitive

**Suppression** :
- Réassignation utilisateurs si option choisie
- Suppression rôle en base
- Log suppression tracé

### Configuration Permissions Rôle

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
- Logique : Si MOD coché, WRITE et READ cochés automatiquement
- Sauvegarde permissions

**Rôles Par Défaut** :
- **Admin** : Toutes permissions (READ/WRITE/MOD) sur tout
- **Operator** : READ/WRITE sur Releases/Rules uniquement, pas accès Users/Roles/Config

### Liste Utilisateurs par Rôle

**Filtrage** :
- Sélection rôle dans liste déroulante
- Filtrage automatique utilisateurs ayant ce rôle
- Liste utilisateurs affichée

**Actions** :
- Voir détail utilisateur
- Éditer utilisateur
- Changer rôle utilisateur

---

## Contraintes Techniques

### Frontend

**Technologies** :
- React 18+ avec TypeScript
- React Router v6
- Bootstrap 5
- Formik ou React Hook Form pour formulaires

**Composants** :
- `RoleList` : Liste rôles
- `RoleCard` : Card rôle
- `RoleCreate` : Formulaire création
- `RoleEdit` : Formulaire édition
- `RoleDetail` : Page détail
- `RolePermissions` : Matrice permissions
- `UsersByRole` : Liste utilisateurs par rôle

**Performance** :
- Chargement liste : < 1s
- Recherche : < 300ms

### Backend

**Endpoints API** :
- `GET /api/roles` : Liste rôles (avec filtres, recherche)
- `GET /api/roles/:id` : Détail rôle
- `POST /api/roles` : Création rôle
- `PUT /api/roles/:id` : Modification rôle
- `DELETE /api/roles/:id` : Suppression rôle
- `GET /api/roles/:id/permissions` : Récupération permissions rôle
- `PUT /api/roles/:id/permissions` : Configuration permissions rôle
- `GET /api/roles/:id/users` : Liste utilisateurs ayant ce rôle

**Base de Données** :
- Table `roles` : id, name, description, created_at
- Table `permissions` : id, role_id, resource, action, created_at
- Relation : Role ↔ Permission (many-to-many)

**Permissions** :
- Endpoints protégés admin uniquement
- Vérification permission admin sur chaque action

**Logique Permissions** :
- Si MOD coché, WRITE et READ cochés automatiquement
- Si WRITE coché, READ coché automatiquement
- Validation logique permissions avant sauvegarde

**Performance** :
- Temps réponse liste : < 200ms
- Création/modification : < 500ms
- Mise à jour permissions utilisateurs : Asynchrone si nombreux

---

## Tests (TDD)

### Tests Unitaires Frontend

```typescript
describe('RoleList', () => {
  it('should display all roles', () => {
    // Test affichage liste
  });
});

describe('RolePermissions', () => {
  it('should auto-check READ/WRITE when MOD checked', () => {
    // Test logique permissions
  });
  
  it('should auto-check READ when WRITE checked', () => {
    // Test logique permissions
  });
});

describe('RoleDelete', () => {
  it('should warn if users have this role', () => {
    // Test vérification utilisateurs
  });
});
```

### Tests Backend

```python
def test_create_role():
    """Test création rôle."""
    # Test création avec permissions par défaut

def test_update_role_permissions():
    """Test mise à jour permissions rôle."""
    # Test update permissions et impact utilisateurs

def test_delete_role_with_users():
    """Test suppression rôle avec utilisateurs."""
    # Test vérification et réassignation
```

### Tests E2E (Playwright MCP)

```python
def test_role_management_e2e():
    """Test gestion rôles E2E avec Playwright MCP."""
    mcp_playwright_browser_navigate(url="http://localhost:5000/roles")
    
    # Créer rôle
    mcp_playwright_browser_click(element="create role button")
    mcp_playwright_browser_type(element="role name", text="CustomRole")
    mcp_playwright_browser_click(element="save button")
    
    # Configurer permissions
    mcp_playwright_browser_click(element="edit permissions")
    mcp_playwright_browser_click(element="MOD checkbox Releases")
    mcp_playwright_browser_click(element="save permissions")
    mcp_playwright_browser_wait_for(text="Permissions updated")
```

---

## Critères de Réussite

### Fonctionnels
- ✅ Liste rôles fonctionnelle
- ✅ Création rôle avec validation
- ✅ Modification rôle fonctionnelle
- ✅ Suppression rôle avec vérifications
- ✅ Configuration permissions granulaires fonctionnelle
- ✅ Liste utilisateurs par rôle fonctionnelle
- ✅ Mise à jour automatique permissions utilisateurs

### Performance
- Chargement liste : < 1s
- Recherche : < 300ms
- Création/modification : < 500ms

### Qualité
- Accessibilité WCAG 2.2 AA
- Responsive design
- Tests couverture 100%

---

## Dépendances

- **Phase 1** : Infrastructure Core (JWT, DB, Models)
- **PRD-005** : Utilisateurs (affectation rôles)

---

**Liens** :
- [Backlog Agile](../BACKLOG_AGILE.md)
- [Test Plan](../TEST_PLAN.md)
- [DEVBOOK](../DEVBOOK.md)
- [CDC](../cdc.md)

