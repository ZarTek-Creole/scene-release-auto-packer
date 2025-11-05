/**
 * Test unitaire pour le composant Hero.
 *
 * Ce test suit les meilleures pratiques Vitest + React Testing Library
 * pour Next.js 15 App Router.
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Hero } from '@/components/Hero';

describe('Hero', () => {
  it('should render hero title', () => {
    render(<Hero />);
    const title = screen.getByRole('heading', {
      level: 1,
      name: /Packaging Automatique de Releases eBook/i,
    });
    expect(title).toBeInTheDocument();
  });

  it('should render hero description', () => {
    render(<Hero />);
    const description = screen.getByText(/Créez automatiquement des packages/i);
    expect(description).toBeInTheDocument();
  });

  it('should render CTA buttons', () => {
    render(<Hero />);
    const startButton = screen.getByRole('link', {
      name: /Commencer maintenant/i,
    });
    const docsButton = screen.getByRole('link', {
      name: /Documentation/i,
    });

    expect(startButton).toBeInTheDocument();
    expect(docsButton).toBeInTheDocument();
    expect(startButton).toHaveAttribute('href', '/docs/quick-start');
    expect(docsButton).toHaveAttribute('href', '/docs');
  });

  it('should render validation badges', () => {
    render(<Hero />);
    expect(screen.getByText(/100% Conforme Scene/i)).toBeInTheDocument();
    expect(screen.getByText(/Production Ready/i)).toBeInTheDocument();
    expect(screen.getByText(/Open Source/i)).toBeInTheDocument();
  });
});

