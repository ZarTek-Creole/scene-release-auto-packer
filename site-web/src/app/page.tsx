import { Hero } from '@/components/Hero';
import { FeaturesSection } from '@/components/FeaturesSection';
import { ScreenshotGallery } from '@/components/ScreenshotGallery';
import { Footer } from '@/components/Footer';
import { JsonLd } from '@/components/JsonLd';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Accueil',
  description:
    'Application moderne pour packaging automatique de releases eBook selon les règles Scene. Wizard 9 étapes, conformité stricte, génération NFO automatique.',
  openGraph: {
    title: 'eBook Scene Packer v2 - Packaging Automatique de Releases eBook',
    description:
      'Application moderne pour packaging automatique de releases eBook selon les règles Scene.',
    type: 'website',
  },
};

/** Page d'accueil - Landing Page.

  Page principale du site web avec Hero, Features, Screenshots, Footer.
  Conforme Next.js 15 App Router (Server Component par défaut).
  Inclut JSON-LD structured data pour SEO.
*/

export default function HomePage() {
  // Placeholder screenshots - À remplacer par vrais screenshots
  const screenshots = [
    {
      src: '/screenshots/dashboard.png',
      alt: 'Dashboard avec statistiques',
      title: 'Dashboard - Vue d\'ensemble',
    },
    {
      src: '/screenshots/wizard.png',
      alt: 'Wizard 9 étapes',
      title: 'Wizard - Création de release',
    },
    {
      src: '/screenshots/releases.png',
      alt: 'Liste des releases',
      title: 'Gestion des releases',
    },
  ];

  // JSON-LD Structured Data - Website Schema
  const websiteSchema = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'eBook Scene Packer v2',
    url: process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com',
    description:
      'Application moderne pour packaging automatique de releases eBook selon les règles Scene.',
    publisher: {
      '@type': 'Organization',
      name: 'eBook Scene Packer Team',
    },
    potentialAction: {
      '@type': 'SearchAction',
      target: {
        '@type': 'EntryPoint',
        urlTemplate: `${process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com'}/docs?q={search_term_string}`,
      },
      'query-input': 'required name=search_term_string',
    },
  };

  // JSON-LD Structured Data - SoftwareApplication Schema
  const softwareSchema = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'eBook Scene Packer v2',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Linux, macOS, Windows',
    description:
      'Application moderne pour packaging automatique de releases eBook selon les règles Scene.',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: '5',
      ratingCount: '1',
    },
  };

  return (
    <>
      {/* JSON-LD Structured Data */}
      <JsonLd data={websiteSchema} />
      <JsonLd data={softwareSchema} />

      {/* Hero Section */}
      <Hero />

      {/* Features Section */}
      <FeaturesSection />

      {/* Screenshots Section */}
      <ScreenshotGallery
        screenshots={screenshots}
        title="Aperçu de l'Application"
      />

      {/* Footer */}
      <Footer />
    </>
  );
}
