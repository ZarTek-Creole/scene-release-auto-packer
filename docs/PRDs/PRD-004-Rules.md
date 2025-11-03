# PRD-004 : Rules Management

**ID** : PRD-004  
**Version** : 1.0.0  
**Date** : 2025-11-01  
**Statut** : Draft  
**Auteur** : Dev Team

---

## Vue d'Ensemble

Système de gestion des règles Scene permettant la consultation, l'organisation, l'upload, le téléchargement et l'édition des rules locales et distantes (scenerules.org), avec organisation par scène, section et année.

**Priorité MoSCoW** : Must Have

**Phase** : Phase 5 (après Releases)

---

## User Stories

### US-004-001 : Liste Rules Locales
**En tant que** utilisateur  
**Je veux** voir la liste des rules locales  
**Afin de** consulter les rules disponibles localement

**Critères d'acceptation** :
- Affichage toutes rules locales stockées
- Organisation par scène, section, année
- Informations affichées : Nom, scène, section, année, date ajout
- Recherche dans la liste
- Filtres par scène, section, année, type release

### US-004-002 : Liste Rules scenerules.org
**En tant que** utilisateur  
**Je veux** voir la liste des rules disponibles sur scenerules.org  
**Afin de** découvrir et télécharger de nouvelles rules

**Critères d'acceptation** :
- Affichage rules disponibles sur https://scenerules.org/
- Organisation par scène, section, année
- Informations : Nom, scène, section, année, dernière mise à jour
- Recherche dans la liste
- Indicateur si rule déjà téléchargée localement

### US-004-003 : Recherche Rules
**En tant que** utilisateur  
**Je veux** rechercher dans les rules  
**Afin de** trouver rapidement une rule spécifique

**Critères d'acceptation** :
- Recherche textuelle dans nom/contenu rule
- Recherche dans rules locales ET scenerules.org
- Filtrage par scène, section, année, type release
- Résultats triés par pertinence
- Highlight résultats recherche

### US-004-004 : Filtrage Rules
**En tant que** utilisateur  
**Je veux** filtrer les rules par scène, section, année  
**Afin de** naviguer efficacement dans les règles

**Critères d'acceptation** :
- Filtre par scène (English, French, German, etc.)
- Filtre par section (eBOOK, TV-720p, X264, etc.)
- Filtre par année
- Filtre par type release (EBOOK, TV, etc.)
- Filtres combinables
- Sauvegarde préférences filtres

### US-004-005 : Prévisualisation Rule
**En tant que** utilisateur  
**Je veux** prévisualiser une rule en mode NFO viewer  
**Afin de** consulter le contenu avant téléchargement/utilisation

**Critères d'acceptation** :
- Bouton "Voir" sur chaque rule
- Affichage NFO viewer monospace UTF-8
- Contenu rule affiché complet
- Syntax highlighting si possible
- Zoom/défilement fonctionnels

### US-004-006 : Téléchargement Rule scenerules.org
**En tant que** utilisateur avec permission WRITE  
**Je veux** télécharger une rule depuis scenerules.org  
**Afin de** ajouter la rule aux rules locales

**Critères d'acceptation** :
- Bouton "Télécharger" sur rule scenerules.org
- Téléchargement vers rules locales
- Barre progression téléchargement
- Confirmation succès/échec
- Rule disponible immédiatement après téléchargement
- Mise à jour automatique si rule existe déjà

### US-004-007 : Upload Rule Locale
**En tant que** utilisateur avec permission WRITE  
**Je veux** uploader une rule depuis mon ordinateur  
**Afin de** ajouter une rule personnalisée

**Critères d'acceptation** :
- Bouton "Upload" visible
- Sélecteur fichier (NFO ou texte)
- Validation format rule
- Extraction métadonnées (scène, section, année) si possible
- Sauvegarde dans rules locales
- Confirmation succès/échec

### US-004-008 : Édition Rule Locale
**En tant que** utilisateur avec permission MOD  
**Je veux** éditer une rule locale  
**Afin de** personnaliser ou corriger une rule

**Critères d'acceptation** :
- Bouton "Éditer" visible si permission MOD
- Éditeur NFO viewer monospace UTF-8
- Sauvegarde modifications
- Validation format avant sauvegarde
- Historique modifications (audit trail)

### US-004-009 : Suppression Rule Locale
**En tant que** utilisateur avec permission MOD  
**Je veux** supprimer une rule locale  
**Afin de** nettoyer les rules obsolètes

**Critères d'acceptation** :
- Bouton "Supprimer" visible si permission MOD
- Confirmation suppression (modal)
- Vérification utilisation rule (avertissement si utilisée)
- Suppression effective
- Log suppression tracé

### US-004-010 : Synchronisation scenerules.org
**En tant que** administrateur  
**Je veux** synchroniser automatiquement les rules depuis scenerules.org  
**Afin de** maintenir les rules à jour

**Critères d'acceptation** :
- Option synchronisation automatique (configurable)
- Synchronisation périodique (quotidienne, hebdomadaire)
- Détection nouvelles rules
- Mise à jour rules modifiées
- Notification changements
- Log synchronisation

---

## Détails Fonctionnels

### Organisation Rules

**Par Scène** :
- English, Baltic, Danish, Dutch, Flemish, French, German, Hungarian, Italian, Lithuanian, Polish, Spanish, Swedish, etc.
- Navigation par scène (sidebar ou tabs)
- Compteur rules par scène

**Par Section** :
- 0DAY7, AUDiOBOOK, BLURAY, CONSOLE, eBOOK, FLAC v3, FLAC (WEB), GAMEiSO, MP3, MViD, NSW
- PS4 v1.17, PS5, PSV, TV-720p, TV-SD, WEB, X264, X265, X2655
- SD-X2647, SD-XXX, XXX-iMAGESETS, XXX-iMAGESETS1, XXX-PAYSiTES, etc.
- Filtrage par section avec compteur

**Par Année** :
- Filtrage par année de la rule
- Affichage années disponibles
- Tri par année (décroissant)

**Par Type Release** :
- Filtrage automatique selon type release sélectionné dans wizard
- Rules disponibles par type affichées

### Interface Rules Locales

**Liste** :
- Vue liste ou cards (toggle)
- Informations : Nom, scène, section, année, date ajout, taille
- Actions : Voir, Éditer (si MOD), Supprimer (si MOD)
- Recherche et filtres actifs

**Actions** :
- **Recherche** : Recherche textuelle temps réel
- **Suppression** : Suppression avec confirmation
- **Upload** : Upload fichier rule
- **NFO Viewer** : Prévisualisation rule
- **Édition** : Édition inline avec NFO viewer

**Stockage** :
- Base de données (table `rules`)
- Champs : id, name, content (NFO), scene, section, year, created_at, updated_at

### Interface Rules scenerules.org

**Liste** :
- Fetch depuis API scenerules.org ou scraping si nécessaire
- Affichage toutes rules disponibles
- Indicateur si rule déjà téléchargée localement
- Organisation identique rules locales (scène/section/année)

**Actions** :
- **Recherche** : Recherche textuelle dans liste distante
- **Télécharger** : Téléchargement vers rules locales
- **NFO Viewer** : Prévisualisation rule distante (fetch contenu)

**Synchronisation** :
- Option synchronisation automatique (admin)
- Détection nouvelles/mises à jour rules
- Notification changements

### NFO Viewer

**Fonctionnalités** :
- Affichage monospace UTF-8
- Syntax highlighting (si possible)
- Zoom in/out
- Recherche dans contenu
- Copie contenu
- Défilement fluide

**Utilisation** :
- Prévisualisation rule avant téléchargement
- Édition rule locale
- Consultation contenu rule

### Upload Rule

**Processus** :
1. Sélection fichier (NFO ou texte)
2. Validation format
3. Extraction métadonnées (scène, section, année) si possible
4. Confirmation métadonnées (édition manuelle possible)
5. Upload et sauvegarde
6. Confirmation succès

**Validation** :
- Format fichier valide (NFO, TXT)
- Structure rule conforme
- Métadonnées extractibles ou saisies manuellement

---

## Contraintes Techniques

### Frontend

**Technologies** :
- React 18+ avec TypeScript
- React Router v6
- Bootstrap 5
- NFO Viewer component (monospace UTF-8)

**Composants** :
- `RulesList` : Liste principale (locales et distantes)
- `RulesFilters` : Barre filtres (scène, section, année, type)
- `RuleCard` : Card rule individuelle
- `RuleViewer` : NFO Viewer pour prévisualisation
- `RuleEditor` : Éditeur rule (si permission MOD)
- `RuleUpload` : Formulaire upload

**Performance** :
- Chargement liste : < 1s
- Recherche : < 300ms
- Prévisualisation : < 500ms

### Backend

**Endpoints API** :
- `GET /api/rules` : Liste rules locales (avec filtres)
- `GET /api/rules/local` : Rules locales uniquement
- `GET /api/rules/scenerules` : Rules scenerules.org
- `GET /api/rules/:id` : Détail rule locale
- `GET /api/rules/:id/preview` : Prévisualisation rule (NFO viewer)
- `POST /api/rules/upload` : Upload rule locale
- `POST /api/rules/download` : Téléchargement depuis scenerules.org
- `PUT /api/rules/:id` : Édition rule locale
- `DELETE /api/rules/:id` : Suppression rule locale
- `POST /api/rules/sync` : Synchronisation scenerules.org (admin)

**Intégration scenerules.org** :
- Fetch depuis API si disponible
- Sinon scraping HTML (avec respect rate limiting)
- Cache résultats (1 heure)
- Gestion erreurs réseau

**Base de Données** :
- Table `rules` :
  - id, name, content (TEXT), scene, section, year
  - created_at, updated_at, created_by

**Permissions** :
- READ : Consultation rules
- WRITE : Upload et téléchargement rules
- MOD : Édition et suppression rules

**Performance** :
- Temps réponse liste : < 200ms
- Recherche : < 300ms
- Téléchargement rule : < 2s
- Synchronisation : Asynchrone (Job)

---

## Tests (TDD)

### Tests Unitaires Frontend

```typescript
describe('RulesList', () => {
  it('should filter rules by scene and section', () => {
    // Test filtrage combiné
  });
  
  it('should search rules in real-time', () => {
    // Test recherche textuelle
  });
  
  it('should display scenerules.org rules', () => {
    // Test affichage rules distantes
  });
});

describe('RuleViewer', () => {
  it('should display rule in NFO viewer', () => {
    // Test prévisualisation monospace UTF-8
  });
});

describe('RuleUpload', () => {
  it('should validate rule format', () => {
    // Test validation upload
  });
});
```

### Tests Backend

```python
def test_list_rules_filtered():
    """Test liste rules avec filtres."""
    # Test filtrage par scène/section/année

def test_download_rule_scenerules():
    """Test téléchargement rule depuis scenerules.org."""
    # Test fetch et sauvegarde

def test_upload_rule():
    """Test upload rule locale."""
    # Test validation et sauvegarde

def test_edit_rule_permission():
    """Test édition rule avec permission MOD."""
    # Test permission MOD requise
```

### Tests E2E (Playwright MCP)

```python
def test_rules_management_e2e():
    """Test gestion rules E2E avec Playwright MCP."""
    mcp_playwright_browser_navigate(url="http://localhost:5000/rules")
    mcp_playwright_browser_snapshot()
    
    # Filtrer par scène French
    mcp_playwright_browser_click(element="filter scene French")
    mcp_playwright_browser_wait_for(text="French rules")
    
    # Prévisualiser rule
    mcp_playwright_browser_click(element="view rule button")
    mcp_playwright_browser_wait_for(text="NFO Viewer")
    
    # Télécharger rule scenerules.org
    mcp_playwright_browser_navigate(url="http://localhost:5000/rules/scenerules")
    mcp_playwright_browser_click(element="download button")
    mcp_playwright_browser_wait_for(text="Rule downloaded")
```

---

## Critères de Réussite

### Fonctionnels
- ✅ Liste rules locales fonctionnelle
- ✅ Liste rules scenerules.org fonctionnelle
- ✅ Recherche et filtrage fonctionnels
- ✅ Prévisualisation NFO viewer fonctionnelle
- ✅ Upload rule locale fonctionnel
- ✅ Téléchargement rule scenerules.org fonctionnel
- ✅ Édition rule locale avec permissions
- ✅ Synchronisation automatique (admin)

### Performance
- Chargement liste : < 1s
- Recherche : < 300ms
- Téléchargement : < 2s

### Qualité
- Accessibilité WCAG 2.2 AA
- Responsive design
- Tests couverture 100%

---

## Dépendances

- **Phase 1** : Infrastructure Core (JWT, DB, Models)
- **PRD-006** : Rôles (permissions READ/WRITE/MOD)
- **PRD-002** : Nouvelle Release Wizard (sélection rule étape 3)

---

**Liens** :
- [Backlog Agile](../BACKLOG_AGILE.md)
- [Test Plan](../TEST_PLAN.md)
- [DEVBOOK](../DEVBOOK.md)
- [CDC](../cdc.md)

