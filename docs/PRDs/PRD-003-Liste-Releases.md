# PRD-003 : Liste des Releases

**ID** : PRD-003  
**Version** : 1.0.0  
**Date** : 2025-11-01  
**Statut** : Draft  
**Auteur** : Dev Team

---

## Vue d'Ensemble

Interface de gestion des releases créées permettant l'affichage, la recherche, le filtrage, l'édition et les actions spéciales (NFOFIX, READNFO, REPACK, DIRFIX) sur les releases selon les permissions utilisateur.

**Priorité MoSCoW** : Must Have

**Phase** : Phase 3 (après Wizard)

---

## User Stories

### US-003-001 : Vue Par Groupe
**En tant que** utilisateur  
**Je veux** voir les releases par groupe selon mes droits  
**Afin de** accéder aux releases de mes groupes autorisés

**Critères d'acceptation** :
- Affichage releases filtrées par groupes auxquels l'utilisateur a accès
- Permissions READ vérifiées
- Liste paginée si nombreuses releases
- Informations essentielles visibles (nom, groupe, type, date, statut)

### US-003-002 : Vue Mes Releases
**En tant que** utilisateur  
**Je veux** voir mes propres releases créées  
**Afin de** gérer mes releases personnelles

**Critères d'acceptation** :
- Liste releases créées par l'utilisateur connecté
- Tri par date (plus récent en premier)
- Affichage toutes releases (complètes et drafts)

### US-003-003 : Filtrage Releases
**En tant que** utilisateur  
**Je veux** filtrer et rechercher dans les releases  
**Afin de** trouver rapidement une release spécifique

**Critères d'acceptation** :
- Filtres : Par type (EBOOK, TV, DOCS, etc.), groupe, date (range), statut
- Recherche textuelle : Dans nom release, groupe, métadonnées
- Tri : Par date, nom, taille, groupe
- Filtres combinables
- Sauvegarde préférences filtres (optionnel)

### US-003-004 : Détail Release
**En tant que** utilisateur  
**Je veux** voir les détails d'une release  
**Afin de** consulter toutes les informations et métadonnées

**Critères d'acceptation** :
- Page détail release avec toutes informations
- Métadonnées complètes affichées
- Arborescence fichiers release
- Historique jobs associés
- Logs packaging disponibles
- Actions disponibles selon permissions

### US-003-005 : Édition Release
**En tant que** utilisateur avec permission WRITE  
**Je veux** éditer une release existante  
**Afin de** corriger ou modifier les informations

**Critères d'acceptation** :
- Bouton "Éditer" visible si permission WRITE
- Formulaire édition pré-rempli
- Validation avant sauvegarde
- Confirmation modifications
- Historique modifications tracé

### US-003-006 : Actions Spéciales - NFOFIX
**En tant que** utilisateur avec permission MOD  
**Je veux** corriger le fichier NFO d'une release  
**Afin de** réparer un NFO mal formaté

**Critères d'acceptation** :
- Bouton "NFOFIX" visible si permission MOD
- Correction automatique format NFO
- Prévisualisation corrections avant application
- Confirmation succès/échec

### US-003-007 : Actions Spéciales - READNFO
**En tant que** utilisateur avec permission MOD  
**Je veux** regénérer à partir du NFO existant  
**Afin de** recréer la structure release depuis NFO

**Critères d'acceptation** :
- Bouton "READNFO" visible si permission MOD
- Lecture NFO et extraction métadonnées
- Régénération structure release
- Prévisualisation avant application

### US-003-008 : Actions Spéciales - REPACK
**En tant que** utilisateur avec permission MOD  
**Je veux** repackager une release  
**Afin de** recréer les fichiers ZIP/RAR avec nouveaux paramètres

**Critères d'acceptation** :
- Bouton "REPACK" visible si permission MOD
- Réutilisation métadonnées et options existantes
- Possibilité modifier options packaging
- Packaging asynchrone avec logs temps réel
- Notification completion

### US-003-009 : Actions Spéciales - DIRFIX
**En tant que** utilisateur avec permission MOD  
**Je veux** corriger la structure de répertoires  
**Afin de** réparer une arborescence incorrecte

**Critères d'acceptation** :
- Bouton "DIRFIX" visible si permission MOD
- Détection anomalies structure
- Correction automatique selon règles Scene
- Prévisualisation corrections
- Confirmation application

### US-003-010 : Suppression Release
**En tant que** administrateur  
**Je veux** supprimer une release  
**Afin de** nettoyer les releases obsolètes

**Critères d'acceptation** :
- Bouton "Supprimer" visible si admin uniquement
- Confirmation suppression (modal)
- Option suppression fichiers physiques
- Log suppression tracé

---

## Détails Fonctionnels

### Interface Liste

**Layout** :
- Liste en cards ou tableau (toggle vue)
- Pagination si > 20 releases par page
- Chargement progressif (lazy loading)
- Filtres en sidebar ou barre supérieure
- Barre recherche visible

**Informations Affichées** :
- Nom release (lien vers détail)
- Groupe
- Type (badge coloré)
- Date création
- Statut (complète, draft, failed)
- Taille totale
- Utilisateur créateur
- Actions disponibles (icônes)

**Responsive** :
- Desktop : Tableau complet avec toutes colonnes
- Tablette : Cards avec informations essentielles
- Mobile : Cards compactes, filtres en overlay

### Filtrage et Recherche

**Filtres** :
- **Type** : EBOOK, TV, DOCS, AUDIOBOOK, GAME (multi-select)
- **Groupe** : Sélecteur groupes (selon droits)
- **Date** : Range date picker (création)
- **Statut** : Complète, Draft, Failed (multi-select)
- **Utilisateur** : Filtre créateur (admin uniquement)

**Recherche Textuelle** :
- Recherche dans : Nom release, groupe, métadonnées (titre, auteur)
- Recherche temps réel (< 300ms)
- Highlight résultats recherche

**Tri** :
- Par défaut : Date création (décroissant)
- Options : Date, Nom (A-Z), Taille, Groupe
- Toggle ascendant/descendant

**Sauvegarde Préférences** :
- Sauvegarde filtres/tri dans préférences utilisateur (optionnel)
- Restauration automatique au chargement page

### Vue Détaillée Release

**Page Détail** :
- **Onglet Informations** :
  - Métadonnées complètes
  - Groupe, type, date création
  - Utilisateur créateur
  - Statut
- **Onglet Fichiers** :
  - Arborescence complète release
  - Taille chaque fichier
  - Actions : Télécharger, Voir
- **Onglet Jobs** :
  - Historique jobs associés (packaging, repack, etc.)
  - Statut chaque job
  - Liens vers logs
- **Onglet Actions** :
  - Actions disponibles selon permissions
  - Boutons actions spéciales

**Métadonnées Affichées** :
- Métadonnées extraction initiale
- Métadonnées enrichissement APIs
- MediaInfo (si disponible)
- Template NFO utilisé

### Édition Release

**Formulaire Édition** :
- Champs éditables :
  - Groupe (si permission)
  - Métadonnées (titre, auteur, etc.)
  - Options packaging
  - Template NFO
- Validation avant sauvegarde
- Confirmation modifications
- Historique modifications (audit trail)

**Permissions** :
- **READ** : Consultation uniquement
- **WRITE** : Création et édition
- **MOD** : Modification + actions spéciales

### Actions Spéciales

**NFOFIX** :
- Détection erreurs format NFO
- Correction automatique :
  - Encoding UTF-8
  - Structure conforme Scene
  - Placeholders valides
- Prévisualisation corrections
- Application avec confirmation

**READNFO** :
- Lecture fichier NFO existant
- Extraction métadonnées depuis NFO
- Régénération structure release :
  - Arborescence répertoires
  - Fichiers manquants détectés
- Prévisualisation régénération
- Confirmation application

**REPACK** :
- Réutilisation métadonnées existantes
- Formulaire options packaging :
  - Nouveaux paramètres ZIP/RAR
  - Nouveau template NFO (optionnel)
- Packaging asynchrone (Job)
- Logs temps réel
- Notification completion

**DIRFIX** :
- Analyse structure répertoires actuelle
- Détection anomalies :
  - Noms fichiers incorrects
  - Structure non conforme
  - Fichiers manquants
- Correction selon règles Scene
- Prévisualisation corrections
- Application avec backup

---

## Contraintes Techniques

### Frontend

**Technologies** :
- React 18+ avec TypeScript
- React Router v6
- Bootstrap 5
- Context API pour état liste

**Composants** :
- `ReleaseList` : Liste principale
- `ReleaseCard` : Card release
- `ReleaseFilters` : Barre filtres
- `ReleaseDetail` : Page détail
- `ReleaseActions` : Actions spéciales
- `ReleaseEdit` : Formulaire édition

**Performance** :
- Chargement liste : < 1s
- Recherche temps réel : < 300ms
- Pagination : 20 releases par page

### Backend

**Endpoints API** :
- `GET /api/releases` : Liste releases (avec filtres, recherche, pagination)
- `GET /api/releases/:id` : Détail release
- `PUT /api/releases/:id` : Édition release
- `DELETE /api/releases/:id` : Suppression release
- `POST /api/releases/:id/repack` : Repackaging
- `POST /api/releases/:id/nfofix` : Correction NFO
- `POST /api/releases/:id/readnfo` : Régénération depuis NFO
- `POST /api/releases/:id/dirfix` : Correction structure
- `GET /api/releases/:id/files` : Arborescence fichiers
- `GET /api/releases/:id/jobs` : Historique jobs

**Permissions** :
- Vérification permissions READ/WRITE/MOD sur chaque endpoint
- Filtrage automatique selon groupes utilisateur

**Performance** :
- Temps réponse liste : < 200ms (p95)
- Recherche : < 300ms
- Édition : < 500ms

---

## Tests (TDD)

### Tests Unitaires Frontend

```typescript
describe('ReleaseList', () => {
  it('should display releases filtered by user groups', () => {
    // Test filtrage par groupes
  });
  
  it('should filter by type and date', () => {
    // Test filtres combinés
  });
  
  it('should search releases in real-time', () => {
    // Test recherche textuelle
  });
});

describe('ReleaseActions', () => {
  it('should show NFOFIX button if MOD permission', () => {
    // Test visibilité bouton selon permission
  });
  
  it('should execute REPACK action', () => {
    // Test action REPACK
  });
});
```

### Tests Backend

```python
def test_list_releases_filtered():
    """Test liste releases filtrée par groupes utilisateur."""
    # Test filtrage automatique selon groupes

def test_edit_release_permission():
    """Test édition release avec permission WRITE."""
    # Test permission WRITE requise

def test_nfofix_action():
    """Test action NFOFIX."""
    # Test correction NFO

def test_repack_action():
    """Test action REPACK."""
    # Test repackaging release
```

### Tests E2E (Playwright MCP)

```python
def test_list_releases_e2e():
    """Test liste releases E2E avec Playwright MCP."""
    mcp_playwright_browser_navigate(url="http://localhost:5000/releases")
    mcp_playwright_browser_snapshot()
    
    # Filtrer par type EBOOK
    mcp_playwright_browser_click(element="filter type EBOOK")
    mcp_playwright_browser_wait_for(text="EBOOK releases")
    
    # Rechercher release
    mcp_playwright_browser_type(element="search input", text="test")
    mcp_playwright_browser_wait_for(text="Test Release")
    
    # Cliquer sur release
    mcp_playwright_browser_click(element="release card")
    mcp_playwright_browser_wait_for(text="Release details")
```

---

## Critères de Réussite

### Fonctionnels
- ✅ Liste releases par groupe fonctionnelle
- ✅ Vue mes releases fonctionnelle
- ✅ Filtrage et recherche fonctionnels
- ✅ Détail release complet
- ✅ Édition release avec permissions
- ✅ Actions spéciales (NFOFIX, READNFO, REPACK, DIRFIX) fonctionnelles

### Performance
- Chargement liste : < 1s
- Recherche : < 300ms
- Filtrage : < 500ms

### Qualité
- Accessibilité WCAG 2.2 AA
- Responsive design
- Tests couverture 100%

---

## Dépendances

- **Phase 1** : Infrastructure Core (JWT, DB, Models)
- **PRD-002** : Nouvelle Release Wizard (création releases)
- **PRD-005** : Utilisateurs (gestion groupes)
- **PRD-006** : Rôles (permissions)

---

**Liens** :
- [Backlog Agile](../BACKLOG_AGILE.md)
- [Test Plan](../TEST_PLAN.md)
- [DEVBOOK](../DEVBOOK.md)
- [CDC](../cdc.md)

