/**
 * Composant Footer pour le site web.
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 */

import Link from 'next/link';

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-dark text-light py-5 mt-5">
      <div className="container">
        <div className="row g-4">
          <div className="col-lg-4">
            <h5 className="fw-semibold mb-3">eBook Scene Packer v2</h5>
            <p className="text-muted">
              Application moderne pour packaging automatique de releases eBook
              conformes aux règles Scene.
            </p>
            <div className="d-flex gap-3">
              <a
                href="https://github.com/yourusername/ebook-scene-packer"
                target="_blank"
                rel="noopener noreferrer"
                className="text-light"
                aria-label="GitHub"
              >
                <i className="bi bi-github icon-lg" aria-hidden="true" />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-light"
                aria-label="Twitter"
              >
                <i className="bi bi-twitter icon-lg" aria-hidden="true" />
              </a>
              <a
                href="https://discord.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-light"
                aria-label="Discord"
              >
                <i className="bi bi-discord icon-lg" aria-hidden="true" />
              </a>
            </div>
          </div>

          <div className="col-lg-2 col-md-6">
            <h6 className="fw-semibold mb-3">Navigation</h6>
            <ul className="list-unstyled">
              <li className="mb-2">
                <Link href="/" className="text-muted text-decoration-none">
                  Accueil
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/features" className="text-muted text-decoration-none">
                  Fonctionnalités
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/docs" className="text-muted text-decoration-none">
                  Documentation
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/install" className="text-muted text-decoration-none">
                  Installation
                </Link>
              </li>
            </ul>
          </div>

          <div className="col-lg-3 col-md-6">
            <h6 className="fw-semibold mb-3">Documentation</h6>
            <ul className="list-unstyled">
              <li className="mb-2">
                <Link
                  href="/docs/quick-start"
                  className="text-muted text-decoration-none"
                >
                  Démarrage rapide
                </Link>
              </li>
              <li className="mb-2">
                <Link
                  href="/docs/installation"
                  className="text-muted text-decoration-none"
                >
                  Installation
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/docs/api" className="text-muted text-decoration-none">
                  API Reference
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/docs/faq" className="text-muted text-decoration-none">
                  FAQ
                </Link>
              </li>
            </ul>
          </div>

          <div className="col-lg-3 col-md-6">
            <h6 className="fw-semibold mb-3">Ressources</h6>
            <ul className="list-unstyled">
              <li className="mb-2">
                <Link href="/about" className="text-muted text-decoration-none">
                  À propos
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/changelog" className="text-muted text-decoration-none">
                  Changelog
                </Link>
              </li>
              <li className="mb-2">
                <a
                  href="https://github.com/yourusername/ebook-scene-packer/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-muted text-decoration-none"
                >
                  Signaler un bug
                </a>
              </li>
              <li className="mb-2">
                <a
                  href="https://github.com/yourusername/ebook-scene-packer"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-muted text-decoration-none"
                >
                  Contribuer
                </a>
              </li>
            </ul>
          </div>
        </div>

        <hr className="my-4 border-secondary" />

        <div className="row align-items-center">
          <div className="col-md-6">
            <p className="text-muted mb-0 small">
              © {currentYear} eBook Scene Packer v2. Tous droits réservés.
            </p>
          </div>
          <div className="col-md-6 text-md-end">
            <Link href="/about" className="text-muted text-decoration-none small me-3">
              Licence
            </Link>
            <Link href="/about" className="text-muted text-decoration-none small">
              Confidentialité
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
