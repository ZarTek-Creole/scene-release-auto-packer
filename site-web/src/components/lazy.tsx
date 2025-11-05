/**
 * Composant pour optimiser le chargement des composants non critiques.
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * pour le lazy loading et le code splitting.
 */

import dynamic from 'next/dynamic';

// Lazy load Footer (non critique pour First Contentful Paint)
export const Footer = dynamic(() => import('./Footer').then((mod) => ({ default: mod.Footer })), {
  ssr: true, // SSR activé pour SEO
});

// Lazy load ScreenshotGallery (non critique pour initial load)
export const ScreenshotGallery = dynamic(
  () => import('./ScreenshotGallery').then((mod) => ({ default: mod.ScreenshotGallery })),
  {
    ssr: true,
    loading: () => (
      <div className="screenshot-gallery py-5">
        <div className="container">
          <div className="text-center mb-5">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Chargement...</span>
            </div>
          </div>
        </div>
      </div>
    ),
  }
);

