# 🎨 Plan d'Implémentation UI/UX - eBook Scene Packer v2

**Date** : 2025-11-01  
**Objectif** : Plan d'implémentation du Design System UI/UX intégralement clair et moderne dès le début

---

## 🎯 Objectif Principal

**Design System intégralement clair, moderne, dés le début, bien réfléchi** :
- ✅ Polices (typographie complète)
- ✅ Onglets (navigation claire)
- ✅ Bordures (élégantes et cohérentes)
- ✅ Icônes (bibliothèque complète)
- ✅ Espacements (système cohérent)
- ✅ Couleurs (thème jour/nuit)
- ✅ Accessibilité (WCAG 2.2 AA)

---

## 📋 Étapes d'Implémentation

### Phase 1 : Setup Design System (En même temps que Phase 1 Infrastructure)

**Objectif** : Mettre en place le Design System de base avant développement composants.

#### Étape 1.1 : Variables CSS et Thème
- [ ] Créer `frontend/src/styles/_variables.css`
  - Variables couleurs (jour/nuit)
  - Variables espacements (spacing system)
  - Variables bordures (rayons, largeurs)
  - Variables typographie (tailles, poids, line-height)
  - Variables transitions et shadows
- [ ] Créer `frontend/src/styles/_theme.css`
  - Thème jour (light)
  - Thème nuit (dark)
  - Transition fluide entre thèmes
- [ ] Créer `frontend/src/contexts/ThemeContext.tsx`
  - Context React pour gestion thème
  - Persistance localStorage
  - Toggle thème fonctionnel

#### Étape 1.2 : Typographie
- [ ] Créer `frontend/src/styles/_typography.css`
  - Stack polices système
  - Police monospace (NFO viewer)
  - Hiérarchie complète (h1-h6, p, code, etc.)
  - Classes utilitaires (.text-muted, .text-small, etc.)

#### Étape 1.3 : Bibliothèque Icônes
- [ ] Installer Bootstrap Icons
```bash
npm install bootstrap-icons
```
- [ ] Créer composant wrapper `frontend/src/components/ui/Icon.tsx`
  - Tailles standardisées (xs, sm, md, lg, xl)
  - Couleurs dynamiques
  - Support accessibility (aria-label)
- [ ] Créer fichier mapping icônes principales
  - Navigation, Actions, Wizard, Releases, Rules, etc.

#### Étape 1.4 : Composants Base UI
- [ ] Créer `frontend/src/components/ui/Button.tsx`
  - Variantes (primary, secondary, outline, ghost, link)
  - Tailles (sm, md, lg)
  - États (disabled, loading)
  - Support icônes (left, right)
- [ ] Créer `frontend/src/components/ui/Input.tsx`
  - Validation et erreurs
  - Support icônes
  - États (disabled, readonly)
  - Help text et error text
- [ ] Créer `frontend/src/components/ui/Card.tsx`
  - Header, Body, Footer
  - Bordures élégantes
  - Ombres et hover states
- [ ] Créer `frontend/src/components/ui/Tabs.tsx`
  - Navigation onglets avec icônes
  - États actifs/inactifs
  - Animation transition
  - Accessibilité (ARIA)
- [ ] Créer `frontend/src/components/ui/Alert.tsx`
  - Variantes (success, error, warning, info)
  - Support icônes
  - Dismissible optionnel

#### Étape 1.5 : Composants Spéciaux
- [ ] Créer `frontend/src/components/ui/NFOViewer.tsx`
  - Monospace UTF-8
  - Line numbers optionnel
  - ASCII ≤ 80 colonnes
  - Thème adaptatif
- [ ] Créer `frontend/src/components/ui/ProgressBar.tsx`
  - Affichage pourcentage
  - Label personnalisable
  - Animations fluides

#### Étape 1.6 : Layout Components
- [ ] Créer `frontend/src/components/layout/Header.tsx`
  - Logo/Brand
  - User menu
  - Theme toggle
  - Logout
- [ ] Créer `frontend/src/components/layout/Navigation.tsx`
  - Onglets navigation selon PRD-001
  - Icônes Bootstrap Icons
  - États actifs/inactifs

**Tests TDD** :
- [ ] Tests composants UI (rendu, props, états)
- [ ] Tests thème (toggle, persistance)
- [ ] Tests accessibilité (contraste, ARIA, focus)

---

### Phase 2 : Interface Administration (Avec Design System)

**Objectif** : Implémenter l'interface admin avec Design System appliqué.

#### Étape 2.1 : Structure Layout
- [ ] Créer layout principal avec Header et Navigation
- [ ] Appliquer système espacements
- [ ] Appliquer système couleurs
- [ ] Appliquer typographie

#### Étape 2.2 : Pages avec Design System
- [ ] Dashboard : Cards, statistiques, graphiques
- [ ] Navigation : Onglets avec icônes et bordures élégantes
- [ ] Structure pages : Titre, description selon PRD-001
- [ ] Thème jour/nuit : Toggle fonctionnel partout

**Design Appliqué** :
- ✅ Polices selon Design System
- ✅ Onglets avec icônes Bootstrap Icons
- ✅ Bordures élégantes (cards, inputs, etc.)
- ✅ Espacements cohérents
- ✅ Couleurs thème jour/nuit

---

### Phase 3 : Wizard 9 Étapes (Avec Design System)

**Objectif** : Implémenter wizard avec Design System pour UX claire.

#### Design Wizard Spécifique
- [ ] Progress Bar élégante (Étape X/9)
- [ ] Étapes avec icônes claires
- [ ] Navigation Previous/Next avec icônes
- [ ] Formulaires avec validation visuelle
- [ ] Alertes pour erreurs/succès
- [ ] Cards pour résumés

**Composants Utilisés** :
- `ProgressBar` : Progression étapes
- `Button` : Navigation (avec icônes ArrowLeft/ArrowRight)
- `Input` : Formulaires (avec validation)
- `Card` : Résumés étapes
- `Alert` : Messages erreur/succès
- `NFO Viewer` : Prévisualisation templates

---

## 🎨 Règles de Design à Respecter

### 1. Cohérence Totale
- ✅ **Même polices** partout (système de polices)
- ✅ **Même espacements** (système 4px base)
- ✅ **Même bordures** (rayons, largeurs cohérents)
- ✅ **Même icônes** (Bootstrap Icons uniquement)
- ✅ **Même couleurs** (variables CSS, thème)

### 2. Clarté Visuelle
- ✅ **Hiérarchie claire** : Titres, sous-titres, texte
- ✅ **Contraste suffisant** : WCAG 2.2 AA
- ✅ **Feedback utilisateur** : États hover, active, focus
- ✅ **Messages clairs** : Alertes, erreurs, succès

### 3. Modernité
- ✅ **Design contemporain** : Pas de skeuomorphisme
- ✅ **Animations fluides** : Transitions 150-350ms
- ✅ **Ombres subtiles** : Depth perception
- ✅ **Bordures élégantes** : Rayons cohérents

### 4. Accessibilité
- ✅ **Contraste couleurs** : ≥ 4.5:1 (texte normal)
- ✅ **Focus visible** : Outline 2px primary color
- ✅ **ARIA labels** : Tous éléments interactifs
- ✅ **Navigation clavier** : Tab order logique

---

## 📦 Dépendances à Installer

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "bootstrap": "^5.3.2",
    "bootstrap-icons": "^1.11.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0"
  }
}
```

---

## 🔄 Intégration avec Bootstrap 5

**Bootstrap 5** utilisé pour :
- ✅ Grid system
- ✅ Utilities (spacing, colors, etc.)
- ✅ Base components (comme inspiration, mais composants React custom)

**Composants React Custom** :
- Créer composants React avec classes Bootstrap + CSS Variables
- Permet contrôle total du design
- Cohérence garantie avec Design System

---

## ✅ Checklist Avant Développement Composants

### Design System Prêt
- [ ] Variables CSS définies
- [ ] Thème jour/nuit fonctionnel
- [ ] Typographie complète
- [ ] Bibliothèque icônes intégrée
- [ ] Composants base créés (Button, Input, Card, Tabs)
- [ ] Composants spéciaux créés (NFO Viewer, Progress Bar)

### Documentation
- [ ] `docs/DESIGN_SYSTEM_UI_UX.md` créé ✅
- [ ] Composants documentés avec exemples
- [ ] Guide utilisation pour développeurs

### Tests
- [ ] Tests composants UI
- [ ] Tests accessibilité
- [ ] Tests thème jour/nuit

---

**Voir** : `docs/DESIGN_SYSTEM_UI_UX.md` pour spécifications complètes du Design System.

---

**Dernière mise à jour** : 2025-11-01  
**Statut** : ✅ Design System Complet et Prêt pour Implémentation

