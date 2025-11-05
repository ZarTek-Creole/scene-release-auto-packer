/**
 * Composant Breadcrumb pour navigation documentation.
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 * Optimisé avec useMemo pour performance.
 */

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useMemo } from 'react';

interface BreadcrumbItem {
  label: string;
  href: string;
}

export function DocsBreadcrumb() {
  const pathname = usePathname();

  // Générer les breadcrumbs à partir du pathname avec useMemo
  const breadcrumbs = useMemo(() => {
    if (!pathname) return [];

    const segments = pathname.split('/').filter(Boolean);
    const breadcrumbsList: BreadcrumbItem[] = [
      { label: 'Accueil', href: '/' },
    ];

    // Mapping des segments aux labels
    const segmentLabels: Record<string, string> = {
      docs: 'Documentation',
      installation: 'Installation',
      prerequisites: 'Prérequis',
      local: 'Installation locale',
      docker: 'Installation Docker',
      configuration: 'Configuration',
      'quick-start': 'Démarrage rapide',
      architecture: 'Architecture',
      overview: 'Vue d\'ensemble',
      backend: 'Backend (Flask)',
      frontend: 'Frontend (React)',
      database: 'Base de données',
      api: 'API Reference',
      introduction: 'Introduction',
      auth: 'Authentification',
      wizard: 'Wizard',
      releases: 'Releases',
      guides: 'Guides',
      deployment: 'Déploiement',
      performance: 'Performance',
      security: 'Sécurité',
      monitoring: 'Monitoring',
      examples: 'Exemples',
      faq: 'FAQ',
    };

    let currentPath = '';
    segments.forEach((segment) => {
      currentPath += `/${segment}`;
      const label = segmentLabels[segment] || segment.charAt(0).toUpperCase() + segment.slice(1);
      breadcrumbsList.push({
        label,
        href: currentPath,
      });
    });

    return breadcrumbsList;
  }, [pathname]);

  if (breadcrumbs.length <= 1) return null;

  return (
    <nav aria-label="Fil d'Ariane" className="docs-breadcrumb">
      <ol className="breadcrumb">
        {breadcrumbs.map((item, index) => {
          const isLast = index === breadcrumbs.length - 1;
          return (
            <li
              key={item.href}
              className={`breadcrumb-item ${isLast ? 'active' : ''}`}
              aria-current={isLast ? 'page' : undefined}
            >
              {index === 0 ? (
                <Link href={item.href} className="breadcrumb-link">
                  <i className="bi bi-house icon-sm" aria-hidden="true" />
                  <span className="visually-hidden">{item.label}</span>
                </Link>
              ) : isLast ? (
                <span>{item.label}</span>
              ) : (
                <Link href={item.href} className="breadcrumb-link">
                  {item.label}
                </Link>
              )}
              {!isLast && (
                <i
                  className="bi bi-chevron-right breadcrumb-separator icon-sm"
                  aria-hidden="true"
                />
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

