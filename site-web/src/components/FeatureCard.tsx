/**
 * Composant FeatureCard pour afficher une fonctionnalité.
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 */

import { ReactNode } from 'react';

interface FeatureCardProps {
  icon: string;
  title: string;
  description: string;
  link?: string;
  children?: ReactNode;
}

export function FeatureCard({
  icon,
  title,
  description,
  link,
  children,
}: FeatureCardProps) {
  const content = (
    <div className="card h-100 shadow-sm">
      <div className="card-body d-flex flex-column">
        <div className="mb-3">
          <i className={`bi bi-${icon} icon-xl text-primary`} aria-hidden="true" />
        </div>
        <h3 className="card-title h5 fw-semibold mb-3">{title}</h3>
        <p className="card-text text-muted flex-grow-1">{description}</p>
        {children && <div className="mt-3">{children}</div>}
        {link && (
          <a
            href={link}
            className="card-link mt-auto text-decoration-none"
            aria-label={`En savoir plus sur ${title}`}
          >
            En savoir plus{' '}
            <i className="bi bi-arrow-right icon-sm" aria-hidden="true" />
          </a>
        )}
      </div>
    </div>
  );

  return link ? (
    <a href={link} className="text-decoration-none text-reset">
      {content}
    </a>
  ) : (
    content
  );
}
