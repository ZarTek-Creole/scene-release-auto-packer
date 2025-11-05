/**
 * Composant de recherche pour documentation.
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 */

'use client';

import { useState, useMemo } from 'react';

interface SearchResult {
  title: string;
  path: string;
  excerpt?: string;
}

// Index de recherche simplifié (à améliorer avec algolia ou autre)
const searchIndex: SearchResult[] = [
  { title: 'Installation', path: '/docs/installation', excerpt: 'Guide complet d\'installation' },
  { title: 'Démarrage rapide', path: '/docs/quick-start', excerpt: 'Guide rapide pour démarrer' },
  { title: 'Architecture', path: '/docs/architecture', excerpt: 'Vue d\'ensemble de l\'architecture' },
  { title: 'API Reference', path: '/docs/api', excerpt: 'Documentation complète de l\'API REST' },
  { title: 'Guide Déploiement', path: '/docs/guides/deployment', excerpt: 'Guide de déploiement' },
  { title: 'Guide Performance', path: '/docs/guides/performance', excerpt: 'Optimisations performance' },
  { title: 'Guide Sécurité', path: '/docs/guides/security', excerpt: 'Meilleures pratiques sécurité' },
  { title: 'FAQ', path: '/docs/faq', excerpt: 'Questions fréquentes' },
];

export function DocsSearch() {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);

  const results = useMemo(() => {
    if (!query.trim()) return [];

    const lowerQuery = query.toLowerCase();
    return searchIndex.filter(
      (item) =>
        item.title.toLowerCase().includes(lowerQuery) ||
        item.excerpt?.toLowerCase().includes(lowerQuery)
    );
  }, [query]);

  return (
    <div className="docs-search position-relative">
      <div className="input-group">
        <span className="input-group-text">
          <i className="bi bi-search" aria-hidden="true" />
        </span>
        <input
          type="search"
          className="form-control"
          placeholder="Rechercher dans la documentation..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => setIsOpen(true)}
          onBlur={() => setTimeout(() => setIsOpen(false), 200)}
          aria-label="Rechercher dans la documentation"
        />
      </div>
      {isOpen && query && results.length > 0 && (
        <div className="docs-search-results">
          <ul className="list-group">
            {results.map((result) => (
              <li key={result.path} className="list-group-item">
                <a href={result.path} className="search-result-link">
                  <div className="search-result-title">{result.title}</div>
                  {result.excerpt && (
                    <div className="search-result-excerpt">{result.excerpt}</div>
                  )}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
      {isOpen && query && results.length === 0 && (
        <div className="docs-search-results">
          <div className="text-muted p-3">Aucun résultat trouvé</div>
        </div>
      )}
    </div>
  );
}

