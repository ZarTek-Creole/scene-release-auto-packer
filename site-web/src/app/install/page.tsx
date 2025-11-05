/**
 * Page Install - Guide d'installation.
 *
 * Cette page suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 */

import type { Metadata } from 'next';
import Link from 'next/link';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Installation',
  description:
    'Guide complet d\'installation de eBook Scene Packer v2 : prérequis, installation locale, Docker, configuration.',
  openGraph: {
    title: 'Installation - eBook Scene Packer v2',
    description: 'Guide complet d\'installation de eBook Scene Packer v2.',
    url: `${baseUrl}/install`,
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'Installation - eBook Scene Packer v2',
    description: 'Guide complet d\'installation de eBook Scene Packer v2.',
  },
};

export default function InstallPage() {
  return (
    <>
      <Header />
      <main className="py-5">
        <div className="container">
          <div className="row">
            <div className="col-lg-8 mx-auto">
              <div className="text-center mb-5">
                <h1 className="display-4 fw-bold mb-3">Installation</h1>
                <p className="lead text-muted">
                  Guide complet pour installer eBook Scene Packer v2 en quelques minutes.
                  Choisissez la méthode qui vous convient : installation locale ou Docker.
                </p>
              </div>

              <div className="alert alert-info">
                <i className="bi bi-info-circle icon-md me-2" aria-hidden="true" />
                Pour un guide détaillé, consultez la{' '}
                <Link href="/docs/installation" className="alert-link">
                  documentation complète
                </Link>
                .
              </div>

              <section className="mb-5">
                <h2 className="h3 fw-semibold mb-3">
                  <i className="bi bi-list-check icon-md me-2 text-primary" aria-hidden="true" />
                  Prérequis
                </h2>
                <ul className="list-unstyled">
                  <li className="mb-2">
                    <i className="bi bi-check-circle-fill text-success icon-sm me-2" aria-hidden="true" />
                    <strong>OS</strong> : Linux (Debian/Ubuntu recommandé), macOS, ou Windows avec WSL2
                  </li>
                  <li className="mb-2">
                    <i className="bi bi-check-circle-fill text-success icon-sm me-2" aria-hidden="true" />
                    <strong>Python</strong> : 3.11 ou supérieur
                  </li>
                  <li className="mb-2">
                    <i className="bi bi-check-circle-fill text-success icon-sm me-2" aria-hidden="true" />
                    <strong>Node.js</strong> : 18.x ou supérieur
                  </li>
                  <li className="mb-2">
                    <i className="bi bi-check-circle-fill text-success icon-sm me-2" aria-hidden="true" />
                    <strong>MySQL</strong> : 8.0 ou supérieur
                  </li>
                  <li className="mb-2">
                    <i className="bi bi-check-circle-fill text-success icon-sm me-2" aria-hidden="true" />
                    <strong>Docker</strong> : 20.10+ (optionnel, pour déploiement Docker)
                  </li>
                </ul>
              </section>

              <section className="mb-5">
                <h2 className="h3 fw-semibold mb-3">
                  <i className="bi bi-download icon-md me-2 text-primary" aria-hidden="true" />
                  Installation Rapide
                </h2>
                <div className="card mb-3">
                  <div className="card-header bg-primary text-white">
                    <i className="bi bi-terminal icon-md me-2" aria-hidden="true" />
                    Installation Locale
                  </div>
                  <div className="card-body">
                    <pre className="bg-dark text-light p-3 rounded mb-0">
                      <code>
                        {`# Cloner le repository
git clone https://github.com/yourusername/ebook-scene-packer.git
cd ebook-scene-packer

# Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install

# Configuration
cp .env.example .env
# Éditer .env avec vos configurations`}
                      </code>
                    </pre>
                  </div>
                </div>

                <div className="card">
                  <div className="card-header bg-success text-white">
                    <i className="bi bi-box icon-md me-2" aria-hidden="true" />
                    Installation Docker (Recommandé)
                  </div>
                  <div className="card-body">
                    <pre className="bg-dark text-light p-3 rounded mb-0">
                      <code>
                        {`# Build et démarrage
docker-compose up -d --build

# Migrations
docker-compose exec backend flask db upgrade`}
                      </code>
                    </pre>
                  </div>
                </div>
              </section>

              <section className="mb-5">
                <h2 className="h3 fw-semibold mb-3">
                  <i className="bi bi-rocket-takeoff icon-md me-2 text-primary" aria-hidden="true" />
                  Premiers Pas
                </h2>
                <p className="mb-3">
                  Une fois l'installation terminée, suivez ces étapes pour démarrer :
                </p>
                <ol>
                  <li className="mb-2">
                    Accédez à l'application :
                    <ul className="mt-2">
                      <li>
                        <strong>Développement</strong> :{' '}
                        <code className="bg-light px-2 py-1 rounded">http://localhost:5173</code>
                      </li>
                      <li>
                        <strong>Docker</strong> :{' '}
                        <code className="bg-light px-2 py-1 rounded">http://localhost:8081</code>
                      </li>
                    </ul>
                  </li>
                  <li className="mb-2">
                    Créez un utilisateur admin via CLI :
                    <pre className="bg-light p-2 rounded mt-2">
                      <code>flask create-admin</code>
                    </pre>
                  </li>
                  <li className="mb-2">
                    Connectez-vous avec vos identifiants admin
                  </li>
                  <li className="mb-2">
                    Suivez le{' '}
                    <Link href="/docs/quick-start" className="text-decoration-none">
                      guide de démarrage rapide
                    </Link>{' '}
                    pour créer votre première release
                  </li>
                </ol>
              </section>

              <section className="mb-5">
                <h2 className="h3 fw-semibold mb-3">
                  <i className="bi bi-question-circle icon-md me-2 text-primary" aria-hidden="true" />
                  Besoin d'Aide ?
                </h2>
                <div className="row g-3">
                  <div className="col-md-6">
                    <div className="card h-100">
                      <div className="card-body">
                        <h3 className="h5 fw-semibold mb-2">
                          <i className="bi bi-book icon-md me-2 text-primary" aria-hidden="true" />
                          Documentation
                        </h3>
                        <p className="text-muted mb-0">
                          Consultez la{' '}
                          <Link href="/docs">documentation complète</Link> pour plus de détails.
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="card h-100">
                      <div className="card-body">
                        <h3 className="h5 fw-semibold mb-2">
                          <i className="bi bi-chat-dots icon-md me-2 text-primary" aria-hidden="true" />
                          FAQ
                        </h3>
                        <p className="text-muted mb-0">
                          Consultez la <Link href="/docs/faq">FAQ</Link> pour les questions
                          fréquentes.
                        </p>
                      </div>
                    </div>
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

