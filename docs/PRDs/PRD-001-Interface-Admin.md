# PRD-001 : Interface Administration

**ID** : PRD-001  
**Version** : 1.0.0  
**Date** : 2025-11-01  
**Statut** : Draft  
**Auteur** : Dev Team

---

## Vue d'Ensemble

Interface d'administration complète permettant la navigation entre toutes les sections de l'application, avec dashboard, navigation, structure de pages uniforme et support thème jour/nuit.

**Priorité MoSCoW** : Must Have

---

## User Stories

### US-001 : Dashboard
**En tant que** administrateur  
**Je veux** voir un dashboard avec mes informations et statistiques  
**Afin de** avoir une vue d'ensemble de l'application

**Critères d'acceptation** :
- Afficher nom utilisateur connecté ("admin") (typographie selon Design System)
- Afficher statistiques basiques (nombre releases, etc.) : Cards avec bordures élégantes
- Design clair et lisible : Conforme Design System (polices, couleurs, espacements, bordures)
- **Icônes** : Bootstrap Icons (tailles standardisées)
- **Bordures** : Cards avec `border-radius-lg`, ombres subtiles
- **Espacements** : Système cohérent (padding, margin selon Design System)

### US-002 : Navigation
**En tant que** utilisateur connecté  
**Je veux** naviguer entre les sections (Nouvelle Release, Liste, Rules, etc.)  
**Afin de** accéder aux différentes fonctionnalités

**Critères d'acceptation** :
- Menu de navigation avec tous les onglets : Onglets avec icônes Bootstrap Icons
- Onglets avec **icônes claires** : PlusIcon, ListIcon, FileTextIcon, UsersIcon, ShieldIcon, SettingsIcon
- État actif visible : Bordure inférieure couleur primaire, police semibold
- Navigation au clavier fonctionnelle : ARIA labels, focus visible
- **Bordures** : Bordure inférieure élégante pour onglet actif (3px)
- **Polices** : `font-weight-medium` pour onglets, `font-weight-semibold` pour actif
- **Couleurs** : Couleur primaire pour actif, texte secondaire pour inactif
- **Espacements** : Padding cohérent selon Design System

### US-003 : Structure Pages
**En tant que** utilisateur  
**Je veux** voir un titre et description sur chaque page  
**Afin de** comprendre le contexte de la page

**Critères d'acceptation** :
- Toutes pages ont un titre clair : Typographie h1 selon Design System (`font-size-3xl`, `font-weight-bold`)
- Toutes pages ont une description : Typographie body selon Design System (`font-size-base`, `color-text-secondary`)
- Layout uniforme : Structure cohérente avec espacements selon Design System
- **Polices** : Hiérarchie typographique respectée (h1 pour titre, p pour description)
- **Espacements** : Marges cohérentes selon système 4px
- **Bordures** : Sections avec bordures élégantes si nécessaire (`border-radius-lg`)

### US-004 : Thème Jour/Nuit
**En tant que** utilisateur  
**Je veux** basculer entre thème jour et nuit  
**Afin de** améliorer mon confort visuel

**Critères d'acceptation** :
- Bouton toggle visible : Bouton variant="ghost" selon Design System avec icône
- Icônes : SunIcon (jour), MoonIcon (nuit) - Bootstrap Icons, taille `icon-md`
- Bascule instantanée : Transition fluide 250ms (variables CSS)
- Préférence sauvegardée : localStorage avec persistance
- **Couleurs** : Variables CSS adaptatives selon thème (toutes couleurs mises à jour)
- **Design** : Bouton élégant avec icône, transition douce

### US-005 : Déconnexion
**En tant que** utilisateur connecté  
**Je veux** me déconnecter  
**Afin de** sécuriser ma session

**Critères d'acceptation** :
- Bouton déconnexion visible
- Déconnexion effective
- Redirection vers login

---

## Détails Fonctionnels

### Dashboard
- Zone d'informations utilisateur (nom, rôle)
- Statistiques :
  - Nombre total de releases
  - Mes releases (si opérateur)
  - Dernières releases créées
- Design responsive Bootstrap

### Navigation
- Barre de navigation supérieure : Header avec bordures élégantes (border-bottom), ombre subtile
- Onglets :
  - Nouvelle Release : Icône PlusIcon (Bootstrap Icons)
  - Liste des Releases : Icône ListIcon
  - Rules : Icône FileTextIcon
  - Utilisateurs : Icône UsersIcon
  - Rôles : Icône ShieldIcon
  - Configurations : Icône SettingsIcon
- Indicateur onglet actif : Bordure inférieure 3px couleur primaire, police semibold
- Menu responsive (collapse sur mobile) : Breakpoints Bootstrap, design adaptatif
- **Polices** : `font-weight-medium` pour onglets, `font-weight-semibold` pour actif
- **Bordures** : Bordure inférieure élégante pour actif, transition hover
- **Espacements** : Padding onglets cohérent (`0.875rem 1.25rem`)
- **Couleurs** : Couleur primaire pour actif, texte secondaire pour inactif, hover avec background

### Structure Pages
- Layout réutilisable (PageLayout component)
- Structure :
  ```
  <PageLayout>
    <Header>
      <Title>Nom de la page</Title>  {/* Typographie h1 : font-size-3xl, font-weight-bold */}
      <Description>Description de la page</Description>  {/* Typographie body : font-size-base, color-text-secondary */}
    </Header>
    <Content>
      {/* Contenu spécifique */}
    </Content>
  </PageLayout>
  ```
- **Polices** :
  - Titre : `font-size-3xl` (1.875rem), `font-weight-bold`, `line-height-tight`
  - Description : `font-size-base` (1rem), `color-text-secondary`, `line-height-relaxed`
- **Espacements** : `margin-bottom` titre (1.5rem), description (0.5rem), content padding (2rem 1.5rem)
- **Bordures** : Sections avec bordures si nécessaire (`border-radius-lg`)

### Thème Jour/Nuit
- Context React pour gestion thème : `ThemeContext` avec état light/dark
- Variables CSS pour couleurs : Toutes couleurs via variables CSS (`--color-primary`, `--color-bg`, `--color-text`)
- Toggle dans navbar : Bouton variant="ghost" avec icônes Bootstrap Icons (SunIcon/MoonIcon)
- Persistance localStorage : Préférence sauvegardée automatiquement
- Transition smooth : Transition 250ms pour toutes propriétés (background-color, color, border-color)
- **Icônes** : SunIcon (jour), MoonIcon (nuit) - taille `icon-md` (1.25rem)
- **Design** : Bouton élégant, icône visible, transition douce

---

## Contraintes Techniques

### Frontend
- React 18+
- React Router v6
- Bootstrap 5
- Context API pour état global

### Backend
- Endpoint : GET /api/dashboard/stats
- Protection JWT
- Retour JSON avec statistiques

---

## Tests (TDD)

### Tests Unitaires Frontend
```javascript
describe('Dashboard', () => {
  it('should display user info', () => {
    // Test affichage info utilisateur
  });
  
  it('should display statistics', () => {
    // Test affichage stats
  });
});

describe('Navigation', () => {
  it('should navigate to correct route', () => {
    // Test navigation
  });
  
  it('should highlight active tab', () => {
    // Test état actif
  });
});

describe('ThemeToggle', () => {
  it('should toggle theme', () => {
    // Test bascule thème
  });
  
  it('should persist theme preference', () => {
    // Test localStorage
  });
});
```

### Tests Backend
```python
def test_dashboard_stats():
    token = get_admin_token()
    response = client.get('/api/dashboard/stats',
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'releases_count' in response.json
```

### Tests E2E
- Navigation complète entre toutes pages
- Bascule thème fonctionnelle
- Déconnexion fonctionnelle

---

## Critères de Réussite

### Fonctionnels
- ✅ Dashboard affiche informations correctes
- ✅ Navigation fonctionnelle entre toutes pages
- ✅ Toutes pages ont titre + description
- ✅ Thème jour/nuit fonctionnel
- ✅ Déconnexion fonctionnelle

### Performance
- Chargement page < 1s
- Bascule thème instantanée (< 100ms)

### Qualité
- Accessibilité WCAG 2.2 AA
- Responsive design (mobile/tablette/desktop)
- Tests couverture 100%

---

## Dépendances

- **Phase 1** : Infrastructure Core (JWT, DB)
- **PRD-002** : Nouvelle Release
- **PRD-003** : Liste des Releases
- **PRD-004** : Rules
- **PRD-005** : Utilisateurs
- **PRD-006** : Rôles
- **PRD-007** : Configurations

---

**Liens** :
- [Backlog Agile](../BACKLOG_AGILE.md)
- [Test Plan](../TEST_PLAN.md)
- [DEVBOOK](../DEVBOOK.md)

