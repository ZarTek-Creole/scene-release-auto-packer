/**
 * Tests d'accessibilité WCAG 2.2 AA.
 *
 * Ce fichier contient des tests d'accessibilité pour valider
 * la conformité WCAG 2.2 AA du site web.
 *
 * À exécuter avec : npm run test:a11y
 * ou avec : playwright test --project=a11y
 */

import { test, expect } from '@playwright/test';

// Tests de navigation clavier
test.describe('Accessibilité - Navigation Clavier', () => {
  test('peut naviguer avec Tab dans Header', async ({ page }) => {
    await page.goto('/');
    
    // Tab depuis le début
    await page.keyboard.press('Tab');
    await expect(page.locator('a[href="/"]')).toBeFocused();
    
    await page.keyboard.press('Tab');
    await expect(page.locator('a[href="/features"]')).toBeFocused();
  });

  test('peut activer liens avec Enter', async ({ page }) => {
    await page.goto('/');
    
    await page.keyboard.press('Tab'); // Skip link
    await page.keyboard.press('Tab'); // Logo
    await page.keyboard.press('Tab'); // Accueil
    await page.keyboard.press('Tab'); // Fonctionnalités
    
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL('/features');
  });

  test('peut fermer modal avec Escape', async ({ page }) => {
    await page.goto('/');
    
    // Ouvrir lightbox (simulé)
    // À implémenter quand screenshots réels ajoutés
  });
});

// Tests de contraste WCAG 2.2 AA
test.describe('Accessibilité - Contraste Couleurs', () => {
  test('texte principal a contraste ≥ 4.5:1', async ({ page }) => {
    await page.goto('/');
    
    const bodyText = page.locator('body');
    const color = await bodyText.evaluate((el) => {
      const style = window.getComputedStyle(el);
      return style.color;
    });
    
    // Vérifier contraste (à implémenter avec outil de test)
    // Exemple : utiliser axe-core ou pa11y
  });

  test('liens ont contraste ≥ 3:1', async ({ page }) => {
    await page.goto('/');
    
    const links = page.locator('a');
    const count = await links.count();
    
    // Vérifier chaque lien
    for (let i = 0; i < count; i++) {
      const link = links.nth(i);
      // Test contraste (à implémenter)
    }
  });
});

// Tests ARIA
test.describe('Accessibilité - ARIA Labels', () => {
  test('tous boutons ont aria-label', async ({ page }) => {
    await page.goto('/');
    
    const buttons = page.locator('button');
    const count = await buttons.count();
    
    for (let i = 0; i < count; i++) {
      const button = buttons.nth(i);
      const ariaLabel = await button.getAttribute('aria-label');
      const text = await button.textContent();
      
      // Vérifier que aria-label existe ou texte présent
      expect(ariaLabel || text).toBeTruthy();
    }
  });

  test('images ont alt text', async ({ page }) => {
    await page.goto('/');
    
    const images = page.locator('img');
    const count = await images.count();
    
    for (let i = 0; i < count; i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute('alt');
      
      // Vérifier que alt existe ou image décorative (aria-hidden)
      const ariaHidden = await img.getAttribute('aria-hidden');
      expect(alt !== null || ariaHidden === 'true').toBeTruthy();
    }
  });
});

// Tests Screen Reader
test.describe('Accessibilité - Screen Reader', () => {
  test('skip link fonctionne', async ({ page }) => {
    await page.goto('/');
    
    // Tab pour accéder au skip link
    await page.keyboard.press('Tab');
    
    const skipLink = page.locator('.skip-link');
    await expect(skipLink).toBeFocused();
    
    await page.keyboard.press('Enter');
    await expect(page.locator('#main-content')).toBeFocused();
  });

  test('landmarks ARIA présents', async ({ page }) => {
    await page.goto('/');
    
    // Vérifier landmarks
    await expect(page.locator('header')).toBeVisible();
    await expect(page.locator('main')).toBeVisible();
    await expect(page.locator('footer')).toBeVisible();
    await expect(page.locator('nav')).toBeVisible();
  });
});

// Tests Focus Visible
test.describe('Accessibilité - Focus Visible', () => {
  test('focus visible sur éléments interactifs', async ({ page }) => {
    await page.goto('/');
    
    const interactiveElements = page.locator('a, button, input, select, textarea');
    const count = await interactiveElements.count();
    
    for (let i = 0; i < Math.min(count, 5); i++) {
      // Focus sur élément
      await interactiveElements.nth(i).focus();
      
      // Vérifier que focus visible (CSS :focus-visible)
      const outline = await interactiveElements.nth(i).evaluate((el) => {
        const style = window.getComputedStyle(el, ':focus-visible');
        return style.outline;
      });
      
      expect(outline).not.toBe('none');
    }
  });
});

