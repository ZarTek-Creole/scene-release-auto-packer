/**
 * Composant Header pour navigation principale.
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 * Optimisé avec useCallback pour performance.
 */

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useCallback, useMemo } from 'react';

export function Header() {
  const pathname = usePathname();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = useCallback(() => {
    setIsMenuOpen((prev) => !prev);
  }, []);

  const closeMenu = useCallback(() => {
    setIsMenuOpen(false);
  }, []);

  const isActive = useCallback(
    (path: string) => pathname === path,
    [pathname]
  );

  const navLinks = useMemo(
    () => [
      { href: '/', label: 'Accueil' },
      { href: '/features', label: 'Fonctionnalités' },
      { href: '/docs', label: 'Documentation' },
      { href: '/install', label: 'Installation' },
      { href: '/about', label: 'À propos' },
    ],
    []
  );

  return (
    <header className="navbar navbar-expand-lg navbar-light bg-light sticky-top shadow-sm">
      <div className="container">
        <Link href="/" className="navbar-brand d-flex align-items-center">
          <i className="bi bi-book icon-lg me-2" aria-hidden="true" />
          <span className="fw-semibold">eBook Scene Packer v2</span>
        </Link>

        <button
          type="button"
          className="navbar-toggler"
          onClick={toggleMenu}
          aria-label="Toggle navigation"
          aria-expanded={isMenuOpen}
          aria-controls="navbarNav"
        >
          <span className="navbar-toggler-icon" />
        </button>

        <nav
          id="navbarNav"
          className={`collapse navbar-collapse ${isMenuOpen ? 'show' : ''}`}
        >
          <ul className="navbar-nav ms-auto">
            {navLinks.map((link) => (
              <li key={link.href} className="nav-item">
                <Link
                  href={link.href}
                  className={`nav-link ${isActive(link.href) ? 'active' : ''}`}
                  onClick={closeMenu}
                >
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
}
