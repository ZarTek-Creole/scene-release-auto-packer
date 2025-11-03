# ⚡ Configuration Vite - React + TypeScript

**Date** : 2025-11-01  
**Source** : Recherche avec Context7 MCP  
**Version Vite** : Latest (recommandé 5.x+)

---

## 🎯 Vue d'Ensemble

Configuration complète de Vite pour le frontend eBook Scene Packer v2 avec React 18+ et TypeScript strict.

**Choix technique** : **Vite** au lieu de Create React App
- ✅ Très rapide (HMR instantané)
- ✅ Moderne (ES modules natifs)
- ✅ Optimisé pour TypeScript
- ✅ Build production optimisé
- ✅ Recommandé 2024

---

## 📦 Installation

### 1. Installer Vite et Dépendances

```bash
# Créer projet React + TypeScript avec Vite
npm create vite@latest frontend -- --template react-ts

# OU manuellement
cd frontend
npm install -D vite @vitejs/plugin-react typescript @types/react @types/react-dom
npm install react react-dom

# Dépendances additionnelles (selon besoins)
npm install react-router-dom axios
npm install -D @types/react-router-dom
```

### 2. Structure Projet Recommandée

```
frontend/
├── public/                 # Assets statiques
├── src/
│   ├── components/         # Composants React
│   │   ├── common/
│   │   ├── wizard/
│   │   └── ...
│   ├── contexts/           # React Contexts
│   │   ├── AuthContext.tsx
│   │   ├── ThemeContext.tsx
│   │   └── WizardContext.tsx
│   ├── services/           # Services API
│   │   └── api.ts
│   ├── hooks/              # Custom hooks
│   ├── utils/              # Utilitaires
│   ├── pages/              # Pages/Views
│   │   ├── Dashboard.tsx
│   │   ├── NewRelease.tsx
│   │   └── ...
│   ├── App.tsx             # Composant racine
│   ├── main.tsx            # Point d'entrée
│   └── vite-env.d.ts       # Types Vite
├── index.html              # HTML principal
├── vite.config.ts          # Configuration Vite
├── tsconfig.json           # Configuration TypeScript
└── package.json
```

---

## ⚙️ Configuration Vite (`vite.config.ts`)

### Configuration de Base avec React + TypeScript

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [
    react({
      // Options React plugin
      jsxRuntime: 'automatic',
    }),
  ],
  
  // Alias de chemins
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '~': path.resolve(__dirname, './'),
    },
  },
  
  // Serveur de développement
  server: {
    host: '0.0.0.0',           // Accessible depuis réseau
    port: 5173,                // Port par défaut
    strictPort: false,         // Utiliser autre port si occupé
    open: false,               // Ne pas ouvrir navigateur automatiquement
    cors: true,                // CORS activé
    hmr: {
      overlay: true,            // Afficher erreurs en overlay
    },
    proxy: {
      // Proxy API Flask vers backend
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  
  // Build production
  build: {
    outDir: 'dist',
    sourcemap: true,           // Source maps pour debug
    target: 'esnext',          // Target ES modules modernes
    minify: 'esbuild',         // Minification rapide
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: {
          // Code splitting optimisé
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
        },
      },
    },
  },
  
  // Variables d'environnement
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
  },
  
  // CSS
  css: {
    modules: {
      localsConvention: 'camelCase',
    },
  },
})
```

### Configuration Conditionnelle (Dev/Build)

```typescript
import { defineConfig, type UserConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig(({ command, mode }) => {
  const isDev = command === 'serve'
  const isProd = mode === 'production'
  
  const config: UserConfig = {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
  }
  
  if (isDev) {
    // Configuration développement
    config.server = {
      port: 5173,
      proxy: {
        '/api': {
          target: 'http://localhost:5000',
          changeOrigin: true,
        },
      },
    }
  } else {
    // Configuration production
    config.build = {
      minify: 'terser',
      sourcemap: false,
      rollupOptions: {
        output: {
          manualChunks: {
            'react-vendor': ['react', 'react-dom'],
          },
        },
      },
    }
  }
  
  return config
})
```

---

## 📝 Configuration TypeScript (`tsconfig.json`)

### Configuration Recommandée

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    
    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    
    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    
    /* Paths */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },
    
    /* Types */
    "types": ["vite/client"]
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Fichier Types Vite (`src/vite-env.d.ts`)

```typescript
/// <reference types="vite/client" />

// Types pour import.meta.env
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_APP_NAME: string
  // Ajouter autres variables d'environnement
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

// Types pour HMR
interface ImportMetaHot {
  accept(): void
  accept(cb: (mod: any) => void): void
  accept(dep: string, cb: (mod: any) => void): void
  accept(deps: string[], cb: (mods: any[]) => void): void
  dispose(cb: (data: any) => void): void
  decline(): void
  invalidate(): void
  on(event: string, cb: (...args: any[]) => void): void
  off(event: string, cb: (...args: any[]) => void): void
  send(event: string, data?: any): void
}
```

---

## 🔧 ESLint Configuration

### Installation

```bash
npm install -D eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser
npm install -D eslint-plugin-react eslint-plugin-react-hooks
npm install -D eslint-plugin-react-x eslint-plugin-react-dom
```

### Configuration (`eslint.config.js`)

```javascript
import { defineConfig } from 'eslint-define-config'
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'
import tseslint from 'typescript-eslint'

export default defineConfig([
  {
    ignores: ['dist', 'node_modules'],
  },
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // TypeScript strict
      ...tseslint.configs.strictTypeChecked,
      // React
      ...reactX.configs['recommended-typescript'],
      ...reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.json'],
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      // Règles personnalisées
      '@typescript-eslint/no-unused-vars': 'error',
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
    },
  },
])
```

---

## 📦 Scripts `package.json`

### Scripts Recommandés

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint src --ext ts,tsx --fix",
    "type-check": "tsc --noEmit"
  }
}
```

---

## 🚀 Utilisation

### Développement

```bash
# Démarrer serveur dev
npm run dev

# Accès : http://localhost:5173
```

### Build Production

```bash
# Build optimisé
npm run build

# Prévisualiser build
npm run preview
```

---

## 🔗 Proxy API Flask

### Configuration Proxy (`vite.config.ts`)

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '/api'),
    },
  },
}
```

### Utilisation dans Code

```typescript
// Services API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

// Exemple requête
fetch(`${API_BASE_URL}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password }),
})
```

---

## 🌍 Variables d'Environnement

### Fichier `.env`

```bash
# .env.local (développement)
VITE_API_BASE_URL=http://localhost:5000/api
VITE_APP_NAME=eBook Scene Packer v2

# .env.production
VITE_API_BASE_URL=https://api.example.com/api
VITE_APP_NAME=eBook Scene Packer v2
```

### Utilisation

```typescript
// Accès variables
const apiUrl = import.meta.env.VITE_API_BASE_URL
const appName = import.meta.env.VITE_APP_NAME

// Types automatiques dans vite-env.d.ts
```

---

## 📊 Optimisations

### Code Splitting

```typescript
// Vite.config.ts
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        'react-vendor': ['react', 'react-dom'],
        'router-vendor': ['react-router-dom'],
        'utils-vendor': ['axios', 'lodash'],
      },
    },
  },
}
```

### Lazy Loading React

```typescript
// Lazy loading routes
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('./pages/Dashboard'))
const NewRelease = lazy(() => import('./pages/NewRelease'))

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/releases/new" element={<NewRelease />} />
      </Routes>
    </Suspense>
  )
}
```

---

## ✅ Checklist Installation

- [ ] Vite installé (`npm install -D vite`)
- [ ] Plugin React installé (`@vitejs/plugin-react`)
- [ ] TypeScript configuré (`tsconfig.json`)
- [ ] Fichier `vite-env.d.ts` créé
- [ ] ESLint configuré
- [ ] Proxy API Flask configuré
- [ ] Variables d'environnement définies
- [ ] Scripts `package.json` configurés
- [ ] Serveur dev fonctionne (`npm run dev`)
- [ ] Build production fonctionne (`npm run build`)

---

## 🔗 Ressources

- **Documentation Vite** : https://vitejs.dev/
- **Template React + TypeScript** : `npm create vite@latest -- --template react-ts`
- **Plugin React** : https://github.com/vitejs/vite-plugin-react
- **Context7 MCP** : Documentation structurée utilisée pour générer ce guide

---

## 📝 Notes

- **HMR** : Hot Module Replacement activé par défaut (très rapide)
- **TypeScript** : Configuration strict recommandée pour qualité code
- **Proxy** : Nécessaire pour éviter CORS en développement
- **Build** : Production optimisé automatiquement (minification, tree-shaking)

---

**Dernière mise à jour** : 2025-11-01  
**Source** : Context7 MCP (vitejs/vite) + Documentation officielle

