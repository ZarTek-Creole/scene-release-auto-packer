# 🎨 Design System UI/UX - eBook Scene Packer v2

**Date** : 2025-11-01  
**Version** : 1.0.0  
**Statut** : Design System Complet  
**Objectif** : Design System intégralement clair, moderne et cohérent dès le début

---

## 🎯 Principes Fondamentaux

### Objectifs UX/UI
- ✅ **Clarté totale** : Interface intuitive, aucune ambiguïté
- ✅ **Modernité** : Design contemporain, professionnel
- ✅ **Cohérence** : Même langage visuel partout
- ✅ **Accessibilité** : WCAG 2.2 AA minimum
- ✅ **Performance** : Chargement rapide, interactions fluides

### Philosophie Design
- **Minimalisme fonctionnel** : Chaque élément a un but
- **Hiérarchie visuelle claire** : Information structurée
- **Feedback utilisateur** : Actions visibles, états clairs
- **Responsive** : Adaptatif mobile/tablette/desktop

---

## 🎨 Système de Couleurs

### Palette Principale

#### Couleurs Primaires
```css
/* Thème Clair (Jour) */
--primary: #0d6efd;          /* Bleu Bootstrap 5 */
--primary-hover: #0b5ed7;
--primary-active: #0a58ca;
--primary-light: #cfe2ff;
--primary-dark: #084298;

/* Thème Sombre (Nuit) */
--primary-dark-mode: #4dabf7;  /* Bleu plus clair pour contraste */
--primary-hover-dark: #339af0;
--primary-active-dark: #228be6;
```

#### Couleurs Secondaires
```css
/* Thème Clair */
--secondary: #6c757d;
--success: #198754;
--danger: #dc3545;
--warning: #ffc107;
--info: #0dcaf0;
--light: #f8f9fa;
--dark: #212529;

/* Thème Sombre */
--secondary-dark: #adb5bd;
--success-dark: #51cf66;
--danger-dark: #ff6b6b;
--warning-dark: #ffd43b;
--info-dark: #4dabf7;
--light-dark: #343a40;
--dark-dark: #f8f9fa;  /* Inversion pour thème sombre */
```

#### Couleurs de Fond
```css
/* Thème Clair */
--bg-primary: #ffffff;
--bg-secondary: #f8f9fa;
--bg-tertiary: #e9ecef;
--bg-hover: #f1f3f5;
--bg-active: #dee2e6;

/* Thème Sombre */
--bg-primary-dark: #1a1d20;
--bg-secondary-dark: #212529;
--bg-tertiary-dark: #2b2f33;
--bg-hover-dark: #343a40;
--bg-active-dark: #495057;
```

#### Couleurs de Texte
```css
/* Thème Clair */
--text-primary: #212529;
--text-secondary: #6c757d;
--text-muted: #adb5bd;
--text-inverse: #ffffff;

/* Thème Sombre */
--text-primary-dark: #f8f9fa;
--text-secondary-dark: #adb5bd;
--text-muted-dark: #6c757d;
--text-inverse-dark: #212529;
```

#### Couleurs d'État
```css
/* États Standards (Clair/Sombre) */
--state-success-bg: #d1e7dd;
--state-success-text: #0f5132;
--state-success-bg-dark: #2b8a3e;
--state-success-text-dark: #d3f9d8;

--state-error-bg: #f8d7da;
--state-error-text: #842029;
--state-error-bg-dark: #c92a2a;
--state-error-text-dark: #ffc9c9;

--state-warning-bg: #fff3cd;
--state-warning-text: #664d03;
--state-warning-bg-dark: #f59f00;
--state-warning-text-dark: #fff9db;

--state-info-bg: #cff4fc;
--state-info-text: #055160;
--state-info-bg-dark: #1c7ed6;
--state-info-text-dark: #d0ebff;
```

### Variables CSS Personnalisées

```css
:root {
  /* Couleurs Thème Clair */
  --color-primary: var(--primary);
  --color-bg: var(--bg-primary);
  --color-text: var(--text-primary);
  
  /* Couleurs Thème Sombre */
  --color-primary-dark: var(--primary-dark-mode);
  --color-bg-dark: var(--bg-primary-dark);
  --color-text-dark: var(--text-primary-dark);
  
  /* Transitions */
  --transition-fast: 150ms ease-in-out;
  --transition-normal: 250ms ease-in-out;
  --transition-slow: 350ms ease-in-out;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  
  /* Borders */
  --border-width: 1px;
  --border-style: solid;
  --border-color: var(--bg-tertiary);
  --border-radius: 0.375rem;  /* 6px */
  --border-radius-sm: 0.25rem;  /* 4px */
  --border-radius-lg: 0.5rem;   /* 8px */
  --border-radius-xl: 0.75rem;  /* 12px */
  --border-radius-full: 9999px;
}

[data-theme="dark"] {
  --color-primary: var(--color-primary-dark);
  --color-bg: var(--color-bg-dark);
  --color-text: var(--color-text-dark);
  --border-color: var(--bg-tertiary-dark);
}
```

---

## 📝 Typographie

### Polices

**Famille Principale** : Système de polices modernes
```css
/* Stack de Polices */
--font-family-base: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
                     "Helvetica Neue", Arial, sans-serif, 
                     "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";

/* Police Monospace (NFO Viewer, Code) */
--font-family-monospace: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", 
                          Consolas, "Courier New", monospace;

/* Police Headings (Optionnelle - Plus distinctive) */
--font-family-headings: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
                        "Helvetica Neue", Arial, sans-serif;
```

### Hiérarchie Typographique

```css
/* Tailles et Poids */
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;  /* 14px */
--font-size-base: 1rem;    /* 16px */
--font-size-lg: 1.125rem;  /* 18px */
--font-size-xl: 1.25rem;   /* 20px */
--font-size-2xl: 1.5rem;   /* 24px */
--font-size-3xl: 1.875rem; /* 30px */
--font-size-4xl: 2.25rem;  /* 36px */
--font-size-5xl: 3rem;     /* 48px */

--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;

/* Line Heights */
--line-height-tight: 1.25;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;
```

### Éléments Typographiques

```css
/* Headings */
h1 {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

h2 {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: var(--text-primary);
  margin-bottom: 1.25rem;
}

h3 {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  color: var(--text-primary);
  margin-bottom: 1rem;
}

h4 {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  color: var(--text-primary);
  margin-bottom: 0.75rem;
}

h5 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-normal);
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

h6 {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-normal);
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

/* Body Text */
p {
  font-size: var(--font-size-base);
  line-height: var(--line-height-relaxed);
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.text-muted {
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.text-small {
  font-size: var(--font-size-sm);
  line-height: var(--line-height-normal);
}

/* Code & Monospace */
code, pre, .nfo-viewer {
  font-family: var(--font-family-monospace);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-relaxed);
}
```

---

## 🧩 Composants UI

### Navigation - Onglets

**Structure** :
```tsx
<TabsContainer>
  <TabList>
    <Tab id="new-release" icon={<PlusIcon />}>
      Nouvelle Release
    </Tab>
    <Tab id="releases" icon={<ListIcon />}>
      Liste des Releases
    </Tab>
    <Tab id="rules" icon={<RulesIcon />}>
      Rules
    </Tab>
    <Tab id="users" icon={<UsersIcon />}>
      Utilisateurs
    </Tab>
    <Tab id="roles" icon={<ShieldIcon />}>
      Rôles
    </Tab>
    <Tab id="config" icon={<SettingsIcon />}>
      Configurations
    </Tab>
  </TabList>
  <TabPanels>
    <TabPanel id="new-release">...</TabPanel>
    <!-- ... autres panels ... -->
  </TabPanels>
</TabsContainer>
```

**Styles Onglets** :
```css
/* Conteneur Onglets */
.tabs-container {
  border-bottom: var(--border-width) var(--border-style) var(--border-color);
  background-color: var(--color-bg);
  padding: 0 1.5rem;
}

/* Liste Onglets */
.tab-list {
  display: flex;
  gap: 0.5rem;
  list-style: none;
  padding: 0;
  margin: 0;
}

/* Onglet Individuel */
.tab {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.25rem;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text-secondary);
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.tab:hover {
  color: var(--color-primary);
  background-color: var(--bg-hover);
}

.tab[aria-selected="true"] {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
  font-weight: var(--font-weight-semibold);
}

.tab:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: -2px;
  border-radius: var(--border-radius) var(--border-radius) 0 0;
}

/* Icône dans Onglet */
.tab-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

/* Panel Contenu */
.tab-panel {
  padding: 2rem 1.5rem;
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Bordures et Contours

**Système de Bordures** :
```css
/* Bordures Standards */
.border {
  border: var(--border-width) var(--border-style) var(--border-color);
}

.border-top {
  border-top: var(--border-width) var(--border-style) var(--border-color);
}

.border-bottom {
  border-bottom: var(--border-width) var(--border-style) var(--border-color);
}

.border-left {
  border-left: var(--border-width) var(--border-style) var(--border-color);
}

.border-right {
  border-right: var(--border-width) var(--border-style) var(--border-color);
}

/* Couleurs Bordures */
.border-primary {
  border-color: var(--color-primary);
}

.border-success {
  border-color: var(--state-success-bg);
}

.border-danger {
  border-color: var(--state-error-bg);
}

.border-warning {
  border-color: var(--state-warning-bg);
}

/* Rayons de Bordure */
.rounded {
  border-radius: var(--border-radius);
}

.rounded-sm {
  border-radius: var(--border-radius-sm);
}

.rounded-lg {
  border-radius: var(--border-radius-lg);
}

.rounded-xl {
  border-radius: var(--border-radius-xl);
}

.rounded-full {
  border-radius: var(--border-radius-full);
}

/* Cards avec Bordures Élégantes */
.card {
  border: var(--border-width) var(--border-style) var(--border-color);
  border-radius: var(--border-radius-lg);
  background-color: var(--color-bg);
  box-shadow: var(--shadow-sm);
  padding: 1.5rem;
  transition: all var(--transition-normal);
}

.card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary);
}

.card-header {
  border-bottom: var(--border-width) var(--border-style) var(--border-color);
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.card-footer {
  border-top: var(--border-width) var(--border-style) var(--border-color);
  padding-top: 1rem;
  margin-top: 1rem;
}
```

### Espacements (Spacing)

**Système d'Espacement Cohérent** :
```css
/* Base : 4px (0.25rem) */
--spacing-0: 0;
--spacing-1: 0.25rem;   /* 4px */
--spacing-2: 0.5rem;    /* 8px */
--spacing-3: 0.75rem;   /* 12px */
--spacing-4: 1rem;      /* 16px */
--spacing-5: 1.25rem;   /* 20px */
--spacing-6: 1.5rem;    /* 24px */
--spacing-8: 2rem;      /* 32px */
--spacing-10: 2.5rem;   /* 40px */
--spacing-12: 3rem;     /* 48px */
--spacing-16: 4rem;     /* 64px */
--spacing-20: 5rem;     /* 80px */
--spacing-24: 6rem;     /* 96px */

/* Padding */
.p-1 { padding: var(--spacing-1); }
.p-2 { padding: var(--spacing-2); }
.p-3 { padding: var(--spacing-3); }
.p-4 { padding: var(--spacing-4); }
.p-6 { padding: var(--spacing-6); }
.p-8 { padding: var(--spacing-8); }

/* Margin */
.m-1 { margin: var(--spacing-1); }
.m-2 { margin: var(--spacing-2); }
.m-3 { margin: var(--spacing-3); }
.m-4 { margin: var(--spacing-4); }
.m-6 { margin: var(--spacing-6); }
.m-8 { margin: var(--spacing-8); }

/* Gap (pour Flexbox/Grid) */
.gap-2 { gap: var(--spacing-2); }
.gap-4 { gap: var(--spacing-4); }
.gap-6 { gap: var(--spacing-6); }
.gap-8 { gap: var(--spacing-8); }
```

---

## 🎯 Icônes

### Bibliothèque d'Icônes

**Choix** : **Bootstrap Icons** (recommandé) ou **Heroicons** ou **Lucide React**

**Avantages Bootstrap Icons** :
- ✅ Gratuit et open-source
- ✅ 2 000+ icônes
- ✅ Compatible Bootstrap 5
- ✅ Format SVG optimisé
- ✅ Légère (~150KB)

### Icônes Principales par Fonctionnalité

```tsx
// Navigation
<PlusIcon />          // Nouvelle Release
<ListIcon />          // Liste Releases
<FileTextIcon />      // Rules
<UsersIcon />        // Utilisateurs
<ShieldIcon />       // Rôles
<SettingsIcon />     // Configurations
<HomeIcon />         // Dashboard
<LogoutIcon />       // Déconnexion

// Actions Communes
<EditIcon />         // Éditer
<DeleteIcon />      // Supprimer
<SaveIcon />        // Sauvegarder
<CancelIcon />      // Annuler
<CheckIcon />      // Valider
<CloseIcon />      // Fermer
<SearchIcon />     // Rechercher
<FilterIcon />     // Filtrer
<DownloadIcon />   // Télécharger
<UploadIcon />     // Uploader
<RefreshIcon />    // Rafraîchir
<InfoIcon />       // Information
<WarningIcon />    // Avertissement
<ErrorIcon />      // Erreur

// Wizard
<ArrowLeftIcon />   // Précédent
<ArrowRightIcon />  // Suivant
<CheckCircleIcon /> // Étape complétée
<CircleIcon />      // Étape incomplète
<ProgressIcon />    // En cours

// Releases
<PackageIcon />     // Packaging
<FileIcon />        // Fichier
<FolderIcon />      // Dossier
<LinkIcon />        // URL distante
<EyeIcon />         // Voir/Preview
<PlayIcon />        // Démarrer

// Rules
<BookIcon />        // Règle
<GlobeIcon />       // scenerules.org
<LocalIcon />       // Locale
<SyncIcon />        // Synchroniser

// Thème
<SunIcon />         // Thème jour
<MoonIcon />        // Thème nuit
```

### Taille et Style des Icônes

```css
/* Tailles Standard */
.icon-xs {
  width: 0.75rem;   /* 12px */
  height: 0.75rem;
}

.icon-sm {
  width: 1rem;      /* 16px */
  height: 1rem;
}

.icon-md {
  width: 1.25rem;  /* 20px */
  height: 1.25rem;
}

.icon-lg {
  width: 1.5rem;    /* 24px */
  height: 1.5rem;
}

.icon-xl {
  width: 2rem;      /* 32px */
  height: 2rem;
}

/* Couleur Icônes */
.icon {
  color: currentColor;
  fill: currentColor;
  stroke: currentColor;
  flex-shrink: 0;
}

.icon-primary {
  color: var(--color-primary);
}

.icon-secondary {
  color: var(--text-secondary);
}

.icon-muted {
  color: var(--text-muted);
}

.icon-success {
  color: var(--state-success-text);
}

.icon-danger {
  color: var(--state-error-text);
}
```

---

## 🔘 Boutons

### Variantes de Boutons

```tsx
// Variantes
<Button variant="primary">Action Principale</Button>
<Button variant="secondary">Action Secondaire</Button>
<Button variant="success">Succès</Button>
<Button variant="danger">Danger</Button>
<Button variant="warning">Avertissement</Button>
<Button variant="info">Information</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Lien</Button>

// Tailles
<Button size="sm">Petit</Button>
<Button size="md">Moyen (défaut)</Button>
<Button size="lg">Grand</Button>

// États
<Button disabled>Désactivé</Button>
<Button loading>Chargement...</Button>

// Avec Icônes
<Button icon={<PlusIcon />}>Ajouter</Button>
<Button icon={<SaveIcon />} iconPosition="right">Sauvegarder</Button>
```

**Styles Boutons** :
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  line-height: 1.5;
  text-align: center;
  text-decoration: none;
  vertical-align: middle;
  cursor: pointer;
  user-select: none;
  border: var(--border-width) var(--border-style) transparent;
  border-radius: var(--border-radius);
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
  pointer-events: none;
}

/* Variantes */
.btn-primary {
  color: #fff;
  background-color: var(--color-primary);
  border-color: var(--color-primary);
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-hover);
  border-color: var(--primary-hover);
}

.btn-secondary {
  color: #fff;
  background-color: var(--secondary);
  border-color: var(--secondary);
}

.btn-outline {
  color: var(--color-primary);
  background-color: transparent;
  border-color: var(--color-primary);
}

.btn-outline:hover:not(:disabled) {
  color: #fff;
  background-color: var(--color-primary);
}

/* Tailles */
.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: var(--font-size-sm);
}

.btn-lg {
  padding: 0.75rem 1.5rem;
  font-size: var(--font-size-lg);
}
```

---

## 📦 Formulaires

### Inputs et Champs

```tsx
<FormGroup>
  <Label htmlFor="username" required>Nom d'utilisateur</Label>
  <Input
    id="username"
    type="text"
    placeholder="Entrez votre nom"
    error="Ce champ est requis"
    icon={<UserIcon />}
  />
  <HelpText>Le nom doit contenir au moins 3 caractères</HelpText>
</FormGroup>
```

**Styles Inputs** :
```css
.form-group {
  margin-bottom: 1.5rem;
}

.label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.label.required::after {
  content: "*";
  color: var(--state-error-text);
  margin-left: 0.25rem;
}

.input {
  display: block;
  width: 100%;
  padding: 0.625rem 0.875rem;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-normal);
  line-height: 1.5;
  color: var(--text-primary);
  background-color: var(--color-bg);
  border: var(--border-width) var(--border-style) var(--border-color);
  border-radius: var(--border-radius);
  transition: all var(--transition-fast);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.25);
}

.input:disabled {
  background-color: var(--bg-secondary);
  opacity: 0.65;
  cursor: not-allowed;
}

.input-error {
  border-color: var(--state-error-text);
}

.input-error:focus {
  border-color: var(--state-error-text);
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.25);
}

.help-text {
  margin-top: 0.375rem;
  font-size: var(--font-size-sm);
  color: var(--text-muted);
}

.error-text {
  margin-top: 0.375rem;
  font-size: var(--font-size-sm);
  color: var(--state-error-text);
  display: flex;
  align-items: center;
  gap: 0.375rem;
}
```

---

## 🌓 Thème Jour/Nuit

### Système de Thème

```tsx
// Context Theme
const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
```

**Toggle Thème** :
```tsx
<Button variant="ghost" onClick={toggleTheme}>
  {theme === 'light' ? <MoonIcon /> : <SunIcon />}
  <span>{theme === 'light' ? 'Thème sombre' : 'Thème clair'}</span>
</Button>
```

**Variables CSS Thème** :
```css
[data-theme="light"] {
  --color-bg: var(--bg-primary);
  --color-text: var(--text-primary);
  --color-border: var(--border-color);
}

[data-theme="dark"] {
  --color-bg: var(--bg-primary-dark);
  --color-text: var(--text-primary-dark);
  --color-border: var(--border-color-dark);
}

/* Transition douce entre thèmes */
* {
  transition: background-color var(--transition-normal),
              color var(--transition-normal),
              border-color var(--transition-normal);
}
```

---

## 🎭 Layout et Structure

### Header (En-tête)

```tsx
<Header>
  <HeaderBrand>
    <Logo />
    <Title>eBook Scene Packer v2</Title>
  </HeaderBrand>
  <HeaderActions>
    <UserMenu user={currentUser} />
    <ThemeToggle />
    <LogoutButton />
  </HeaderActions>
</Header>
```

**Styles Header** :
```css
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background-color: var(--color-bg);
  border-bottom: var(--border-width) var(--border-style) var(--border-color);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}
```

### Sidebar (Optionnel - Si nécessaire)

```css
.sidebar {
  width: 16rem;
  min-height: calc(100vh - 4rem);
  background-color: var(--bg-secondary);
  border-right: var(--border-width) var(--border-style) var(--border-color);
  padding: 1.5rem 1rem;
}
```

### Main Content

```css
.main-content {
  flex: 1;
  padding: 2rem 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.page-description {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  line-height: var(--line-height-relaxed);
}
```

---

## 📊 Composants Spéciaux

### NFO Viewer

**Spécifique au projet** : Visualisation des fichiers NFO Scene

```tsx
<NFOViewer
  content={nfoContent}
  lineNumbers={true}
  maxWidth={80}
  theme={theme}
/>
```

**Styles NFO Viewer** :
```css
.nfo-viewer {
  font-family: var(--font-family-monospace);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-tight);
  background-color: var(--bg-secondary);
  border: var(--border-width) var(--border-style) var(--border-color);
  border-radius: var(--border-radius);
  padding: 1rem;
  overflow-x: auto;
  max-width: 100%;
  white-space: pre-wrap;
  word-break: break-all;
  tab-size: 2;
}

.nfo-viewer.with-line-numbers {
  counter-reset: line-number;
}

.nfo-viewer.with-line-numbers::before {
  content: counter(line-number);
  counter-increment: line-number;
  display: inline-block;
  width: 3rem;
  color: var(--text-muted);
  text-align: right;
  margin-right: 1rem;
  user-select: none;
}
```

### Progress Bar (Barre de Progression)

```tsx
<ProgressBar
  value={65}
  max={100}
  label="Packaging en cours"
  showPercentage={true}
/>
```

**Styles Progress Bar** :
```css
.progress-bar-container {
  width: 100%;
  height: 1.25rem;
  background-color: var(--bg-tertiary);
  border-radius: var(--border-radius-full);
  overflow: hidden;
  position: relative;
}

.progress-bar-fill {
  height: 100%;
  background-color: var(--color-primary);
  border-radius: var(--border-radius-full);
  transition: width var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.5rem;
  color: #fff;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
}
```

### Alertes et Notifications

```tsx
<Alert variant="success">Opération réussie !</Alert>
<Alert variant="error">Erreur lors de l'opération</Alert>
<Alert variant="warning">Attention requise</Alert>
<Alert variant="info">Information importante</Alert>
```

**Styles Alertes** :
```css
.alert {
  padding: 1rem 1.25rem;
  border-radius: var(--border-radius);
  border: var(--border-width) var(--border-style) transparent;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.alert-success {
  background-color: var(--state-success-bg);
  color: var(--state-success-text);
  border-color: var(--state-success-text);
}

.alert-error {
  background-color: var(--state-error-bg);
  color: var(--state-error-text);
  border-color: var(--state-error-text);
}

.alert-warning {
  background-color: var(--state-warning-bg);
  color: var(--state-warning-text);
  border-color: var(--state-warning-text);
}

.alert-info {
  background-color: var(--state-info-bg);
  color: var(--state-info-text);
  border-color: var(--state-info-text);
}
```

---

## 📱 Responsive Design

### Breakpoints

```css
/* Breakpoints Bootstrap 5 */
--breakpoint-xs: 0;
--breakpoint-sm: 576px;
--breakpoint-md: 768px;
--breakpoint-lg: 992px;
--breakpoint-xl: 1200px;
--breakpoint-xxl: 1400px;

/* Media Queries */
@media (max-width: 575.98px) {
  /* Mobile */
  .tabs-container {
    padding: 0 1rem;
    overflow-x: auto;
  }
  
  .tab {
    padding: 0.75rem 1rem;
    font-size: var(--font-size-sm);
  }
  
  .main-content {
    padding: 1.5rem 1rem;
  }
}

@media (min-width: 576px) and (max-width: 767.98px) {
  /* Tablet Portrait */
}

@media (min-width: 768px) and (max-width: 991.98px) {
  /* Tablet Landscape */
}

@media (min-width: 992px) {
  /* Desktop */
}
```

---

## ♿ Accessibilité (WCAG 2.2 AA)

### Contraste Couleurs

**Exigences** :
- Texte normal : Ratio ≥ 4.5:1
- Texte large (18px+) : Ratio ≥ 3:1
- Éléments interactifs : Ratio ≥ 3:1

**Vérification** :
- Utiliser outils de vérification (WebAIM Contrast Checker)
- Tester avec simulateurs daltonisme

### Focus et Navigation

```css
/* Focus Visible */
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Skip Link */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-primary);
  color: #fff;
  padding: 0.5rem 1rem;
  z-index: 1000;
}

.skip-link:focus {
  top: 0;
}
```

### ARIA et Sémantique

```tsx
// Navigation accessible
<nav aria-label="Navigation principale">
  <Tabs role="tablist" aria-orientation="horizontal">
    <Tab
      id="new-release"
      role="tab"
      aria-selected={activeTab === 'new-release'}
      aria-controls="panel-new-release"
      tabIndex={activeTab === 'new-release' ? 0 : -1}
    >
      Nouvelle Release
    </Tab>
  </Tabs>
</nav>

// Formulaires accessibles
<FormGroup>
  <Label htmlFor="username" required>
    Nom d'utilisateur
    <span className="sr-only"> (requis)</span>
  </Label>
  <Input
    id="username"
    type="text"
    aria-required="true"
    aria-invalid={hasError}
    aria-describedby="username-error username-help"
  />
  <ErrorText id="username-error">{error}</ErrorText>
  <HelpText id="username-help">Minimum 3 caractères</HelpText>
</FormGroup>
```

---

## 🎨 Exemples de Composants Complets

### Card avec Actions

```tsx
<Card>
  <CardHeader>
    <CardTitle>Release Example</CardTitle>
    <CardSubtitle>Groupe-Test-Author-Title-EPUB-EN-2024-ISBN-eBook</CardSubtitle>
  </CardHeader>
  <CardBody>
    <CardContent>
      {/* Contenu */}
    </CardContent>
  </CardBody>
  <CardFooter>
    <ButtonGroup>
      <Button variant="outline" icon={<EyeIcon />}>Voir</Button>
      <Button variant="outline" icon={<EditIcon />}>Éditer</Button>
      <Button variant="danger" icon={<DeleteIcon />}>Supprimer</Button>
    </ButtonGroup>
  </CardFooter>
</Card>
```

### Table avec Tri et Filtres

```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHeaderCell sortable sortDirection="asc">Nom</TableHeaderCell>
      <TableHeaderCell sortable>Date</TableHeaderCell>
      <TableHeaderCell>Statut</TableHeaderCell>
      <TableHeaderCell>Actions</TableHeaderCell>
    </TableRow>
  </TableHeader>
  <TableBody>
    {/* Rows */}
  </TableBody>
</Table>
```

---

## 📐 Grille et Layout

### Grid System

```css
.container {
  width: 100%;
  padding-right: 1rem;
  padding-left: 1rem;
  margin-right: auto;
  margin-left: auto;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin-right: -0.5rem;
  margin-left: -0.5rem;
}

.col {
  flex: 1 0 0%;
  padding-right: 0.5rem;
  padding-left: 0.5rem;
}

.col-12 { flex: 0 0 auto; width: 100%; }
.col-6 { flex: 0 0 auto; width: 50%; }
.col-4 { flex: 0 0 auto; width: 33.333333%; }
.col-3 { flex: 0 0 auto; width: 25%; }
```

---

## 🚀 Implémentation

### Stack Technologique UI

**Composants** :
- **Bootstrap 5** : Grid, utilities, base components
- **React Components** : Custom components avec Bootstrap classes
- **CSS Variables** : Thème dynamique
- **Bootstrap Icons** : Bibliothèque icônes

**Structure** :
```
frontend/src/
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Tabs.tsx
│   │   ├── Card.tsx
│   │   ├── Alert.tsx
│   │   ├── ProgressBar.tsx
│   │   └── NFOViewer.tsx
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Navigation.tsx
│   │   └── Footer.tsx
│   └── ...
├── styles/
│   ├── _variables.css
│   ├── _typography.css
│   ├── _components.css
│   ├── _theme.css
│   └── main.css
└── ...
```

---

## ✅ Checklist Implémentation UI/UX

### Design System
- [ ] Variables CSS définies (couleurs, espacements, bordures)
- [ ] Typographie complète
- [ ] Bibliothèque icônes choisie et intégrée
- [ ] Thème jour/nuit fonctionnel
- [ ] Composants base créés (Button, Input, Card, Tabs)

### Composants Spécifiques
- [ ] NFO Viewer avec styles monospace
- [ ] Progress Bar pour packaging
- [ ] Alertes et notifications
- [ ] Tables avec tri et filtres
- [ ] Modals/Dialogs

### Layout
- [ ] Header avec navigation
- [ ] Structure pages cohérente
- [ ] Responsive design testé
- [ ] Accessibilité WCAG 2.2 AA

### Documentation
- [ ] Guide design system créé (ce document)
- [ ] Storybook ou équivalent (optionnel)
- [ ] Composants documentés avec exemples

---

**Dernière mise à jour** : 2025-11-01  
**Version** : 1.0.0  
**Statut** : ✅ Design System Complet

