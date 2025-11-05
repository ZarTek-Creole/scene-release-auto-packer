/**
 * Page Features - Détails des fonctionnalités.
 *
 * Cette page suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 */

import type { Metadata } from 'next';
import { FeatureCard } from '@/components/FeatureCard';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import { JsonLd } from '@/components/JsonLd';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Fonctionnalités',
  description:
    'Découvrez toutes les fonctionnalités de eBook Scene Packer v2 : Wizard 9 étapes, conformité Scene, génération NFO, gestion utilisateurs, configurations, dashboard.',
  openGraph: {
    title: 'Fonctionnalités - eBook Scene Packer v2',
    description:
      'Découvrez toutes les fonctionnalités de eBook Scene Packer v2.',
    url: `${baseUrl}/features`,
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Fonctionnalités - eBook Scene Packer v2',
    description: 'Découvrez toutes les fonctionnalités de eBook Scene Packer v2.',
  },
};

const features = [
  {
    icon: 'magic',
    title: 'Wizard 9 Étapes',
    description:
      'Processus guidé en 9 étapes pour créer des releases conformes aux règles Scene. Validation automatique à chaque étape avec feedback visuel.',
    details: [
      'Sélection du groupe Scene',
      'Choix du type de release',
      'Sélection des règles Scene',
      'Upload et validation du fichier',
      'Analyse automatique des métadonnées',
      'Enrichissement optionnel',
      'Sélection du template NFO',
      'Configuration des options',
      'Packaging et finalisation',
    ],
  },
  {
    icon: 'file-earmark-check',
    title: 'Conformité Scene',
    description:
      'Validation automatique selon les règles Scene. Intégration avec scenerules.org pour les règles à jour.',
    details: [
      'Validation automatique du format',
      'Vérification des métadonnées',
      'Conformité aux règles Scene',
      'Téléchargement depuis scenerules.org',
      'Gestion des règles locales',
    ],
  },
  {
    icon: 'file-text',
    title: 'Génération NFO',
    description:
      'Génération automatique de fichiers NFO conformes aux standards Scene. Templates personnalisables.',
    details: [
      'Templates NFO conformes Scene',
      'Personnalisation des templates',
      'Génération automatique',
      'Aperçu avant génération',
      'Export multiple formats',
    ],
  },
  {
    icon: 'people',
    title: 'Gestion Utilisateurs',
    description:
      'Système complet de gestion d\'utilisateurs avec rôles et permissions granulaires.',
    details: [
      'Création et gestion utilisateurs',
      'Système de rôles',
      'Permissions granulaires',
      'Audit trail',
      'Multi-utilisateurs',
    ],
  },
  {
    icon: 'sliders',
    title: 'Configurations',
    description:
      'Configuration flexible des destinations FTP/SSH, APIs d\'enrichissement, et règles de packaging.',
    details: [
      'Destinations FTP/SSH',
      'APIs d\'enrichissement',
      'Règles de packaging',
      'Templates personnalisables',
      'Configuration par environnement',
    ],
  },
  {
    icon: 'graph-up',
    title: 'Dashboard & Statistiques',
    description:
      'Tableau de bord complet avec statistiques en temps réel. Suivi des releases et des jobs.',
    details: [
      'Statistiques en temps réel',
      'Suivi des releases',
      'Historique des jobs',
      'Graphiques et métriques',
      'Export des données',
    ],
  },
];

export default function FeaturesPage() {
  // JSON-LD Structured Data - CollectionPage Schema
  const collectionPageSchema = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'Fonctionnalités - eBook Scene Packer v2',
    description:
      'Découvrez toutes les fonctionnalités de eBook Scene Packer v2.',
    url: `${baseUrl}/features`,
    mainEntity: {
      '@type': 'ItemList',
      itemListElement: features.map((feature, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        item: {
          '@type': 'SoftwareFeature',
          name: feature.title,
          description: feature.description,
        },
      })),
    },
  };

  return (
    <>
      {/* JSON-LD Structured Data */}
      <JsonLd data={collectionPageSchema} />

      <Header />
      <main className="py-5">
        <div className="container">
          <div className="text-center mb-5">
            <h1 className="display-4 fw-bold mb-3">Fonctionnalités</h1>
            <p className="lead text-muted">
              Découvrez toutes les fonctionnalités de eBook Scene Packer v2
            </p>
          </div>

          <div className="row g-4 mb-5">
            {features.map((feature) => (
              <div key={feature.icon} className="col-md-6 col-lg-4">
                <div className="card h-100 shadow-sm">
                  <div className="card-body d-flex flex-column">
                    <div className="mb-3">
                      <i
                        className={`bi bi-${feature.icon} icon-xl text-primary`}
                        aria-hidden="true"
                      />
                    </div>
                    <h2 className="card-title h5 fw-semibold mb-3">{feature.title}</h2>
                    <p className="card-text text-muted flex-grow-1 mb-3">
                      {feature.description}
                    </p>
                    <div className="mt-auto">
                      <h3 className="h6 fw-semibold mb-2">Détails :</h3>
                      <ul className="list-unstyled small mb-0">
                        {feature.details.map((detail, index) => (
                          <li key={index} className="mb-1">
                            <i
                              className="bi bi-check-circle-fill text-success icon-sm me-2"
                              aria-hidden="true"
                            />
                            {detail}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center">
            <a href="/docs" className="btn btn-primary btn-lg">
              <i className="bi bi-book icon-md me-2" aria-hidden="true" />
              Voir la Documentation
            </a>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}

