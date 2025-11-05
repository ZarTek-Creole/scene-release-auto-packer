# Guide de Tests - Site Web Next.js

Ce guide détaille la configuration et l'utilisation des tests pour le site web Next.js.

## 🧪 Frameworks de Test

### 1. Vitest (Tests Unitaires)

Vitest est utilisé pour les tests unitaires et d'intégration.

#### Configuration

- Fichier : `vitest.config.ts`
- Setup : `tests/setup.ts`

#### Exécution

```bash
# Tous les tests
npm run test

# Mode watch
npm run test:watch

# Interface UI
npm run test:ui

# Avec coverage
npm run test:coverage
```

#### Structure des Tests

```
tests/
├── setup.ts                 # Configuration globale
├── components/
│   ├── Hero.test.tsx        # Tests composant Hero
│   ├── FeatureCard.test.tsx # Tests composant FeatureCard
│   └── Header.test.tsx      # Tests composant Header
└── accessibility.spec.ts    # Tests accessibilité (Playwright)
```

### 2. Playwright (Tests E2E et Accessibilité)

Playwright est utilisé pour les tests d'accessibilité et les tests E2E.

#### Configuration

- Fichier : `tests/accessibility.spec.ts`
- Configuration Playwright : `playwright.config.ts` (à créer si nécessaire)

#### Exécution

```bash
# Tests d'accessibilité
npm run test:a11y

# Tous les tests Playwright
npx playwright test
```

## 📝 Écrire des Tests

### Test Unitaire avec Vitest

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MyComponent } from '@/components/MyComponent';

describe('MyComponent', () => {
  it('should render correctly', () => {
    render(<MyComponent />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});
```

### Test d'Accessibilité avec Playwright

```typescript
import { test, expect } from '@playwright/test';

test('should be accessible', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toBeVisible();
});
```

## ✅ Checklist de Tests

### Avant Commit

- [ ] Tests unitaires passent (`npm run test`)
- [ ] Coverage ≥80% (`npm run test:coverage`)
- [ ] Lint passe (`npm run lint`)
- [ ] Format check passe (`npm run format:check`)
- [ ] Build production réussit (`npm run build`)

### Avant Merge

- [ ] Tous les tests CI/CD passent
- [ ] Tests d'accessibilité passent (`npm run test:a11y`)
- [ ] Pas de régression détectée

## 🔧 Configuration

### Coverage Thresholds

Dans `vitest.config.ts` :

```typescript
coverage: {
  thresholds: {
    lines: 80,
    functions: 80,
    branches: 80,
    statements: 80,
  },
}
```

### Mocks

Les mocks suivants sont configurés dans `tests/setup.ts` :
- `next/navigation` (useRouter, usePathname, useSearchParams)
- `next/image` (Image component)
- `next/link` (Link component)

## 📊 CI/CD

Les tests sont exécutés automatiquement dans GitHub Actions :
- Lint et format check
- TypeScript type check
- Tests unitaires avec coverage
- Build production

## 🚨 Troubleshooting

### Tests qui échouent localement mais passent en CI

```bash
# Nettoyer le cache
rm -rf node_modules .next
npm ci
npm run test
```

### Erreur de mock Next.js

Vérifier que les mocks dans `tests/setup.ts` sont à jour avec la version Next.js utilisée.

### Erreur Playwright

```bash
# Installer les navigateurs
npx playwright install
```

## 📚 Ressources

- [Documentation Vitest](https://vitest.dev/)
- [Documentation Playwright](https://playwright.dev/)
- [Documentation React Testing Library](https://testing-library.com/react)

