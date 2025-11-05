/**
 * Composant ScreenshotGallery pour afficher une galerie de screenshots.
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 * Lightbox avec Bootstrap Modal (à améliorer avec librairie dédiée si nécessaire).
 */

'use client';

import { useState, useCallback } from 'react';

interface Screenshot {
  src: string;
  alt: string;
  title: string;
}

interface ScreenshotGalleryProps {
  screenshots: Screenshot[];
  title?: string;
}

export function ScreenshotGallery({
  screenshots,
  title = "Aperçu de l'Application",
}: ScreenshotGalleryProps) {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  const openLightbox = useCallback((index: number) => {
    setSelectedIndex(index);
  }, []);

  const closeLightbox = useCallback(() => {
    setSelectedIndex(null);
  }, []);

  const navigateLightbox = useCallback(
    (direction: 'prev' | 'next') => {
      if (selectedIndex === null) return;

      if (direction === 'prev') {
        setSelectedIndex(
          selectedIndex > 0 ? selectedIndex - 1 : screenshots.length - 1
        );
      } else {
        setSelectedIndex(
          selectedIndex < screenshots.length - 1 ? selectedIndex + 1 : 0
        );
      }
    },
    [selectedIndex, screenshots.length]
  );

  return (
    <>
      <section className="screenshot-gallery py-5">
        <div className="container">
          <div className="text-center mb-5">
            <h2 className="display-5 fw-bold mb-3">{title}</h2>
            <p className="lead text-muted">
              Découvrez l'interface moderne et intuitive de l'application
            </p>
          </div>

          <div className="row g-4">
            {screenshots.map((screenshot, index) => (
              <div key={screenshot.src} className="col-md-6 col-lg-4">
                <div
                  className="card shadow-sm border-0 cursor-pointer"
                  onClick={() => openLightbox(index)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      openLightbox(index);
                    }
                  }}
                  role="button"
                  tabIndex={0}
                  aria-label={`Ouvrir ${screenshot.title} en grand`}
                >
                  <div className="position-relative" style={{ aspectRatio: '16/9' }}>
                    <div className="bg-secondary rounded-top d-flex align-items-center justify-content-center h-100">
                      <i className="bi bi-image icon-xl text-muted" aria-hidden="true" />
                    </div>
                    <div className="position-absolute top-0 end-0 m-2">
                      <span className="badge bg-dark bg-opacity-50">
                        <i className="bi bi-zoom-in icon-sm" aria-hidden="true" />
                      </span>
                    </div>
                  </div>
                  <div className="card-body">
                    <h3 className="card-title h6 mb-0">{screenshot.title}</h3>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Lightbox Modal */}
      {selectedIndex !== null && (
        <div
          className="modal fade show d-block"
          style={{ backgroundColor: 'rgba(0, 0, 0, 0.9)' }}
          onClick={closeLightbox}
          role="dialog"
          aria-modal="true"
          aria-labelledby="lightboxTitle"
        >
          <div className="modal-dialog modal-xl modal-dialog-centered">
            <div className="modal-content bg-transparent border-0">
              <div className="modal-header border-0">
                <h5 id="lightboxTitle" className="modal-title text-white">
                  {screenshots[selectedIndex].title}
                </h5>
                <button
                  type="button"
                  className="btn-close btn-close-white"
                  onClick={closeLightbox}
                  aria-label="Fermer"
                />
              </div>
              <div className="modal-body position-relative">
                <div className="position-relative" style={{ minHeight: '400px' }}>
                  <div className="bg-secondary rounded d-flex align-items-center justify-content-center h-100">
                    <i className="bi bi-image icon-xl text-muted" aria-hidden="true" />
                  </div>
                </div>
                <button
                  type="button"
                  className="btn btn-link text-white position-absolute top-50 start-0 translate-middle-y ms-3"
                  onClick={(e) => {
                    e.stopPropagation();
                    navigateLightbox('prev');
                  }}
                  aria-label="Image précédente"
                >
                  <i className="bi bi-chevron-left icon-lg" aria-hidden="true" />
                </button>
                <button
                  type="button"
                  className="btn btn-link text-white position-absolute top-50 end-0 translate-middle-y me-3"
                  onClick={(e) => {
                    e.stopPropagation();
                    navigateLightbox('next');
                  }}
                  aria-label="Image suivante"
                >
                  <i className="bi bi-chevron-right icon-lg" aria-hidden="true" />
                </button>
              </div>
              <div className="modal-footer border-0 justify-content-center">
                <span className="text-white">
                  {selectedIndex + 1} / {screenshots.length}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
