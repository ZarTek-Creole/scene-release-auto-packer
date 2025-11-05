/**
 * Page About - À propos du projet.
 *
 * Cette page suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 */

import type { Metadata } from 'next';
import Link from 'next/link';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import { JsonLd } from '@/components/JsonLd';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'À propos',
  description:
    'À propos de eBook Scene Packer v2 : mission, technologies, architecture, contribution, licence.',
  openGraph: {
    title: 'À propos - eBook Scene Packer v2',
    description: 'À propos de eBook Scene Packer v2 : mission, technologies, architecture.',
    url: `${baseUrl}/about`,
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'À propos - eBook Scene Packer v2',
    description: 'À propos de eBook Scene Packer v2.',
  },
};

const technologies = [
  { name: 'Flask 3.1.2', category: 'Backend', icon: 'server' },
  { name: 'React 19.2.0', category: 'Frontend', icon: 'react' },
  { name: 'TypeScript 5.6.3', category: 'Frontend', icon: 'code-slash' },
  { name: 'MySQL 8.0', category: 'Database', icon: 'database' },
  { name: 'SQLAlchemy 2.0', category: 'ORM', icon: 'layers' },
  { name: 'Bootstrap 5.3.8', category: 'UI', icon: 'palette' },
  { name: 'Docker', category: 'Deployment', icon: 'box' },
  { name: 'Next.js 15', category: 'Site Web', icon: 'globe' },
];

export default function AboutPage() {
  // JSON-LD Structured Data - AboutPage Schema
  const aboutPageSchema = {
    '@context': 'https://schema.org',
    '@type': 'AboutPage',
    name: 'À propos - eBook Scene Packer v2',
    description:
      'À propos de eBook Scene Packer v2 : mission, technologies, architecture, contribution, licence.',
    url: `${baseUrl}/about`,
    publisher: {
      '@type': 'Organization',
      name: 'eBook Scene Packer Team',
      url: baseUrl,
    },
  };

  return (
    <>
      {/* JSON-LD Structured Data */}
      <JsonLd data={aboutPageSchema} />

      <Header />
      <main className="py-5">
        <div className="container">
          <div className="row">
            <div className="col-lg-10 mx-auto">
              <div className="text-center mb-5">
                <h1 className="display-4 fw-bold mb-3">À propos</h1>
                <p className="lead text-muted">
                  Découvrez eBook Scene Packer v2 et son équipe
                </p>
              </div>

              <section className="mb-5">
                <h2 className="h3 fw-semibold mb-3">
                  <i className="bi bi-bullseye icon-md me-2 text-primary" aria-hidden="true" />
                  Mission du Projet
                </h2>
                <p className="lead">
                  eBook Scene Packer v2 est une application moderne conçue pour automatiser
                  la création de packages de releases eBook conformes aux règles Scene.
                </p>
                <p>
                  Notre objectif est de simplifier le processus de packaging tout en garantissant
                  une conformité stricte aux standards Scene, réduisant les erreurs humaines et
                  économisant du temps précieux. Nous croyons en la qualité, la conformité et
                  l'efficacité dans le packaging de releases eBook.
                </p>
                <p>
                  L'application est construite avec les meilleures pratiques de développement
                  moderne : architecture modulaire, tests complets, documentation exhaustive,
                  et sécurité renforcée.
                </p>
              </section>

              <section className="mb-5">
                <h2 className="h3 fw-semibold mb-3">
                  <i className="bi bi-code-slash icon-md me-2 text-primary" aria-hidden="true" />
                  Technologies
                </h2>
                <div className="row g-3">
                  {technologies.map((tech) => (
                    <div key={tech.name} className="col-md-6 col-lg-4">
                      <div className="card h-100 shadow-sm">
                        <div className="card-body">
                          <div className="d-flex align-items-center mb-2">
                            <i
                              className={`bi bi-${tech.icon} icon-lg text-primary me-2`}
                              aria-hidden="true"
                            />
                            <h3 className="h6 fw-semibold mb-0">{tech.name}</h3>
                          </div>
                          <span className="badge bg-secondary">{tech.category}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              <section className="mb-5">
                <h2 className="h3 fw-semibold mb-3">
                  <i className="bi bi-diagram-3 icon-md me-2 text-primary" aria-hidden="true" />
                  Architecture
                </h2>
                <div className="card shadow-sm">
                  <div className="card-body">
                    <p>
                      eBook Scene Packer v2 suit une architecture moderne et modulaire :
                    </p>
                    <ul>
                      <li className="mb-2">
                        <strong>Backend</strong> : Flask avec Application Factory Pattern, Blueprints
                        modulaires, SQLAlchemy ORM
                      </li>
                      <li className="mb-2">
                        <strong>Frontend</strong> : React 19 avec TypeScript strict, Context API,
                        React Router v6
                      </li>
                      <li className="mb-2">
                        <strong>Base de données</strong> : MySQL 8.0 avec migrations Flask-Migrate
                      </li>
                      <li className="mb-2">
                        <strong>Déploiement</strong> : Docker, Gunicorn, Nginx
                      </li>
                    </ul>
                    <Link href="/docs/architecture" className="btn btn-primary mt-3">
                      <i className="bi bi-book icon-md me-2" aria-hidden="true" />
                      Voir Documentation Architecture
                    </Link>
                  </div>
                </div>
              </section>

              <section className="mb-5">
                <h2 className="h3 fw-semibold mb-3">
                  <i className="bi bi-heart icon-md me-2 text-primary" aria-hidden="true" />
                  Contribuer
                </h2>
                <div className="card shadow-sm">
                  <div className="card-body">
                    <p>
                      eBook Scene Packer v2 est un projet open source. Nous accueillons
                      chaleureusement les contributions !
                    </p>
                    <div className="d-flex flex-wrap gap-3 mt-3">
                      <a
                        href="https://github.com/yourusername/ebook-scene-packer"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-primary"
                      >
                        <i className="bi bi-github icon-md me-2" aria-hidden="true" />
                        GitHub
                      </a>
                      <a
                        href="https://github.com/yourusername/ebook-scene-packer/issues"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-outline-secondary"
                      >
                        <i className="bi bi-bug icon-md me-2" aria-hidden="true" />
                        Signaler un Bug
                      </a>
                      <a
                        href="https://github.com/yourusername/ebook-scene-packer/discussions"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-outline-secondary"
                      >
                        <i className="bi bi-chat-dots icon-md me-2" aria-hidden="true" />
                        Discussions
                      </a>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-5">
                <h2 className="h3 fw-semibold mb-3">
                  <i className="bi bi-shield-check icon-md me-2 text-primary" aria-hidden="true" />
                  Licence
                </h2>
                <div className="card shadow-sm">
                  <div className="card-body">
                    <p>
                      eBook Scene Packer v2 est sous licence{' '}
                      <strong>MIT License</strong>. Vous êtes libre d'utiliser, modifier et
                      distribuer ce logiciel selon les termes de la licence.
                    </p>
                    <a
                      href="https://github.com/yourusername/ebook-scene-packer/blob/main/LICENSE"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-outline-primary"
                    >
                      <i className="bi bi-file-text icon-md me-2" aria-hidden="true" />
                      Voir la Licence
                    </a>
                  </div>
                </div>
              </section>

              <section className="mb-5">
                <h2 className="h3 fw-semibold mb-3">
                  <i className="bi bi-envelope icon-md me-2 text-primary" aria-hidden="true" />
                  Contact
                </h2>
                <div className="card shadow-sm">
                  <div className="card-body">
                    <p>Pour toute question ou suggestion :</p>
                    <ul className="list-unstyled">
                      <li className="mb-2">
                        <i className="bi bi-github icon-md me-2" aria-hidden="true" />
                        <a
                          href="https://github.com/yourusername/ebook-scene-packer"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-decoration-none"
                        >
                          GitHub Issues
                        </a>
                      </li>
                      <li className="mb-2">
                        <i className="bi bi-chat-dots icon-md me-2" aria-hidden="true" />
                        <a
                          href="https://github.com/yourusername/ebook-scene-packer/discussions"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-decoration-none"
                        >
                          GitHub Discussions
                        </a>
                      </li>
                    </ul>
                  </div>
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

