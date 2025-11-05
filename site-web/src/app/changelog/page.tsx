/**
 * Page Changelog - Historique des versions.
 *
 * Cette page suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 */

import type { Metadata } from 'next';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import { JsonLd } from '@/components/JsonLd';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Changelog',
  description:
    'Historique des versions de eBook Scene Packer v2 : nouvelles fonctionnalités, bugs corrigés, breaking changes.',
  openGraph: {
    title: 'Changelog - eBook Scene Packer v2',
    description: 'Historique des versions de eBook Scene Packer v2.',
    url: `${baseUrl}/changelog`,
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'Changelog - eBook Scene Packer v2',
    description: 'Historique des versions de eBook Scene Packer v2.',
  },
};

const changelog = [
  {
    version: '2.0.0',
    date: '2025-11-01',
    type: 'major',
    changes: {
      features: [
        'Refonte complète de l\'architecture',
        'Wizard 9 étapes avec validation automatique',
        'Système de rôles et permissions granulaires',
        'Intégration scenerules.org',
        'Génération NFO automatique',
        'Dashboard avec statistiques en temps réel',
        'APIs d\'enrichissement configurables',
        'Support multi-destinations FTP/SSH',
      ],
      fixes: [
        'Correction bugs de packaging',
        'Amélioration performance extraction métadonnées',
        'Correction validation règles Scene',
      ],
      breaking: [
        'API REST complètement refactorisée',
        'Structure base de données modifiée',
        'Format de configuration changé',
      ],
    },
  },
];

export default function ChangelogPage() {
  // JSON-LD Structured Data - SoftwareApplication avec versionHistory
  const softwareVersionSchema = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'eBook Scene Packer',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Linux, macOS, Windows',
    softwareVersion: changelog[0]?.version || '2.0.0',
    releaseNotes: changelog[0]?.changes.features.join('. ') || '',
    datePublished: changelog[0]?.date || '2025-11-01',
  };

  return (
    <>
      {/* JSON-LD Structured Data */}
      <JsonLd data={softwareVersionSchema} />

      <Header />
      <main className="py-5">
        <div className="container">
          <div className="row">
            <div className="col-lg-10 mx-auto">
              <div className="text-center mb-5">
                <h1 className="display-4 fw-bold mb-3">Changelog</h1>
                <p className="lead text-muted">
                  Historique des versions et changements de eBook Scene Packer v2
                </p>
              </div>

              {changelog.map((release) => (
                <div key={release.version} className="card shadow-sm mb-4">
                  <div className="card-header bg-primary text-white">
                    <div className="d-flex justify-content-between align-items-center">
                      <h2 className="h4 mb-0 fw-semibold">
                        Version {release.version}
                      </h2>
                      <span className="badge bg-light text-dark">
                        {release.date}
                      </span>
                    </div>
                  </div>
                  <div className="card-body">
                    {release.changes.features.length > 0 && (
                      <section className="mb-4">
                        <h3 className="h5 fw-semibold mb-3 text-success">
                          <i className="bi bi-plus-circle icon-md me-2" aria-hidden="true" />
                          Nouvelles Fonctionnalités
                        </h3>
                        <ul className="list-unstyled">
                          {release.changes.features.map((feature, index) => (
                            <li key={index} className="mb-2">
                              <i
                                className="bi bi-check-circle-fill text-success icon-sm me-2"
                                aria-hidden="true"
                              />
                              {feature}
                            </li>
                          ))}
                        </ul>
                      </section>
                    )}

                    {release.changes.fixes.length > 0 && (
                      <section className="mb-4">
                        <h3 className="h5 fw-semibold mb-3 text-warning">
                          <i className="bi bi-bug icon-md me-2" aria-hidden="true" />
                          Corrections de Bugs
                        </h3>
                        <ul className="list-unstyled">
                          {release.changes.fixes.map((fix, index) => (
                            <li key={index} className="mb-2">
                              <i
                                className="bi bi-check-circle-fill text-success icon-sm me-2"
                                aria-hidden="true"
                              />
                              {fix}
                            </li>
                          ))}
                        </ul>
                      </section>
                    )}

                    {release.changes.breaking.length > 0 && (
                      <section className="mb-4">
                        <h3 className="h5 fw-semibold mb-3 text-danger">
                          <i className="bi bi-exclamation-triangle icon-md me-2" aria-hidden="true" />
                          Breaking Changes
                        </h3>
                        <ul className="list-unstyled">
                          {release.changes.breaking.map((breaking, index) => (
                            <li key={index} className="mb-2">
                              <i
                                className="bi bi-x-circle-fill text-danger icon-sm me-2"
                                aria-hidden="true"
                              />
                              {breaking}
                            </li>
                          ))}
                        </ul>
                      </section>
                    )}
                  </div>
                </div>
              ))}

              <section className="card shadow-sm">
                <div className="card-header bg-secondary">
                  <h2 className="h4 mb-0 fw-semibold">Roadmap Future</h2>
                </div>
                <div className="card-body">
                  <ul className="list-unstyled">
                    <li className="mb-2">
                      <i className="bi bi-circle icon-sm me-2 text-muted" aria-hidden="true" />
                      Support de nouveaux formats eBook
                    </li>
                    <li className="mb-2">
                      <i className="bi bi-circle icon-sm me-2 text-muted" aria-hidden="true" />
                      Amélioration des performances
                    </li>
                    <li className="mb-2">
                      <i className="bi bi-circle icon-sm me-2 text-muted" aria-hidden="true" />
                      API GraphQL (optionnel)
                    </li>
                    <li className="mb-2">
                      <i className="bi bi-circle icon-sm me-2 text-muted" aria-hidden="true" />
                      Mode CLI avancé
                    </li>
                  </ul>
                </div>
              </section>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}

