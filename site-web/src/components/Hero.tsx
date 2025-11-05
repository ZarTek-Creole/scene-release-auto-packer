/**
 * Composant Hero pour landing page.
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 * Design moderne 2025 avec animations subtiles.
 */

import Link from 'next/link';

export function Hero() {
  return (
    <section className="hero-section py-5">
      <div className="container">
        <div className="row align-items-center min-vh-75">
          <div className="col-lg-6">
            <h1 className="display-4 fw-bold mb-4">
              Packaging Automatique de Releases eBook
            </h1>
            <p className="lead mb-4">
              Créez automatiquement des packages de releases eBook conformes aux
              règles Scene avec notre application moderne. Wizard guidé en 9 étapes,
              validation automatique, génération NFO. Tout ce dont vous avez besoin
              pour un packaging professionnel et conforme.
            </p>
            <div className="d-flex flex-wrap gap-3 mb-4">
              <Link
                href="/docs/quick-start"
                className="btn btn-primary btn-lg"
                aria-label="Commencer maintenant - Accéder au guide de démarrage rapide"
              >
                <i className="bi bi-play-circle icon-md me-2" aria-hidden="true" />
                Commencer maintenant
              </Link>
              <Link
                href="/docs"
                className="btn btn-outline-secondary btn-lg"
                aria-label="Voir la documentation complète"
              >
                <i className="bi bi-book icon-md me-2" aria-hidden="true" />
                Documentation
              </Link>
            </div>
            <div className="d-flex flex-wrap gap-4 text-muted">
              <div className="d-flex align-items-center">
                <i className="bi bi-check-circle-fill text-success icon-sm me-2" aria-hidden="true" />
                <span>100% Conforme Scene</span>
              </div>
              <div className="d-flex align-items-center">
                <i className="bi bi-check-circle-fill text-success icon-sm me-2" aria-hidden="true" />
                <span>Production Ready</span>
              </div>
              <div className="d-flex align-items-center">
                <i className="bi bi-check-circle-fill text-success icon-sm me-2" aria-hidden="true" />
                <span>Open Source</span>
              </div>
            </div>
          </div>
          <div className="col-lg-6 mt-5 mt-lg-0">
            <div className="hero-image-wrapper">
              <div className="hero-placeholder bg-secondary rounded-lg p-5 d-flex align-items-center justify-content-center">
                <i className="bi bi-laptop icon-xl text-muted" aria-hidden="true" />
                <span className="visually-hidden">Screenshot de l'application</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
