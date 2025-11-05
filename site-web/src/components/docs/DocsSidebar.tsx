/**
 * Composant Sidebar pour navigation documentation.
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 * Optimisé avec useCallback et useMemo pour performance.
 */

'use client';

import { FC, useState, useCallback, useMemo } from 'react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';

interface DocSection {
  title: string;
  path: string;
  icon?: string;
  children?: DocSection[];
}

const docsStructure: DocSection[] = [
  {
    title: 'Vue d\'ensemble',
    path: '/docs',
    icon: 'list',
  },
  {
    title: 'Installation',
    path: '/docs/installation',
    icon: 'download',
    children: [
      { title: 'Prérequis', path: '/docs/installation/prerequisites' },
      { title: 'Installation locale', path: '/docs/installation/local' },
      { title: 'Installation Docker', path: '/docs/installation/docker' },
      { title: 'Configuration', path: '/docs/installation/configuration' },
    ],
  },
  {
    title: 'Démarrage rapide',
    path: '/docs/quick-start',
    icon: 'play-circle',
  },
  {
    title: 'Architecture',
    path: '/docs/architecture',
    icon: 'diagram-3',
    children: [
      { title: 'Vue d\'ensemble', path: '/docs/architecture/overview' },
      { title: 'Backend (Flask)', path: '/docs/architecture/backend' },
      { title: 'Frontend (React)', path: '/docs/architecture/frontend' },
      { title: 'Base de données', path: '/docs/architecture/database' },
    ],
  },
  {
    title: 'API Reference',
    path: '/docs/api',
    icon: 'code-slash',
    children: [
      { title: 'Introduction', path: '/docs/api/introduction' },
      { title: 'Authentification', path: '/docs/api/auth' },
      { title: 'Wizard', path: '/docs/api/wizard' },
      { title: 'Releases', path: '/docs/api/releases' },
    ],
  },
  {
    title: 'Guides',
    path: '/docs/guides',
    icon: 'book',
    children: [
      { title: 'Déploiement', path: '/docs/guides/deployment' },
      { title: 'Performance', path: '/docs/guides/performance' },
      { title: 'Sécurité', path: '/docs/guides/security' },
      { title: 'Monitoring', path: '/docs/guides/monitoring' },
    ],
  },
  {
    title: 'Exemples',
    path: '/docs/examples',
    icon: 'file-earmark-code',
  },
  {
    title: 'FAQ',
    path: '/docs/faq',
    icon: 'question-circle',
  },
];

interface SidebarItemProps {
  section: DocSection;
  currentPath: string;
  level?: number;
}

function SidebarItem({ section, currentPath, level = 0 }: SidebarItemProps) {
  const [isOpen, setIsOpen] = useState(
    currentPath.startsWith(section.path) || level === 0
  );
  
  const isActive = useMemo(() => currentPath === section.path, [currentPath, section.path]);
  const hasChildren = useMemo(
    () => section.children && section.children.length > 0,
    [section.children]
  );

  const toggleOpen = useCallback(() => {
    setIsOpen((prev) => !prev);
  }, []);

  return (
    <li className={`sidebar-item ${isActive ? 'active' : ''}`}>
      <div className="d-flex align-items-center">
        <Link
          href={section.path}
          className={`sidebar-link ${isActive ? 'active' : ''}`}
          style={{ paddingLeft: `${level * 1.5}rem` }}
        >
          {section.icon && (
            <i className={`bi bi-${section.icon} sidebar-icon`} aria-hidden="true" />
          )}
          <span>{section.title}</span>
        </Link>
        {hasChildren && (
          <button
            type="button"
            className="sidebar-toggle"
            onClick={toggleOpen}
            aria-label={isOpen ? 'Réduire' : 'Développer'}
            aria-expanded={isOpen}
          >
            <i
              className={`bi bi-chevron-${isOpen ? 'down' : 'right'} icon-sm`}
              aria-hidden="true"
            />
          </button>
        )}
      </div>
      {hasChildren && isOpen && (
        <ul className="sidebar-children">
          {section.children!.map((child) => (
            <SidebarItem
              key={child.path}
              section={child}
              currentPath={currentPath}
              level={level + 1}
            />
          ))}
        </ul>
      )}
    </li>
  );
}

export function DocsSidebar() {
  const pathname = usePathname();

  return (
    <aside className="docs-sidebar" aria-label="Navigation documentation">
      <nav className="sidebar-nav">
        <ul className="sidebar-list">
          {docsStructure.map((section) => (
            <SidebarItem
              key={section.path}
              section={section}
              currentPath={pathname || ''}
            />
          ))}
        </ul>
      </nav>
    </aside>
  );
}

