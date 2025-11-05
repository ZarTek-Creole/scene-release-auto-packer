/**
 * Test unitaire pour le composant Header.
 *
 * Ce test suit les meilleures pratiques Vitest + React Testing Library
 * pour Next.js 15 App Router.
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Header } from '@/components/Header';

// Mock usePathname
vi.mock('next/navigation', async () => {
  const actual = await vi.importActual('next/navigation');
  return {
    ...actual,
    usePathname: vi.fn(() => '/'),
  };
});

describe('Header', () => {
  it('should render logo', () => {
    render(<Header />);
    const logo = screen.getByRole('link', {
      name: /eBook Scene Packer v2/i,
    });
    expect(logo).toBeInTheDocument();
    expect(logo).toHaveAttribute('href', '/');
  });

  it('should render navigation links', () => {
    render(<Header />);
    expect(screen.getByRole('link', { name: /Accueil/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Fonctionnalités/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Documentation/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Installation/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /À propos/i })).toBeInTheDocument();
  });

  it('should render mobile menu toggle button', () => {
    render(<Header />);
    const toggleButton = screen.getByRole('button', {
      name: /Toggle navigation/i,
    });
    expect(toggleButton).toBeInTheDocument();
  });
});

