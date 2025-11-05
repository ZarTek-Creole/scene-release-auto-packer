/**
 * Test unitaire pour le composant FeatureCard.
 *
 * Ce test suit les meilleures pratiques Vitest + React Testing Library
 * pour Next.js 15 App Router.
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { FeatureCard } from '@/components/FeatureCard';

describe('FeatureCard', () => {
  const defaultProps = {
    icon: 'magic',
    title: 'Test Feature',
    description: 'Test description for feature',
  };

  it('should render feature card with title and description', () => {
    render(<FeatureCard {...defaultProps} />);
    expect(screen.getByText('Test Feature')).toBeInTheDocument();
    expect(screen.getByText('Test description for feature')).toBeInTheDocument();
  });

  it('should render icon', () => {
    render(<FeatureCard {...defaultProps} />);
    const icon = document.querySelector('.bi-magic');
    expect(icon).toBeInTheDocument();
  });

  it('should render link when provided', () => {
    render(<FeatureCard {...defaultProps} link="/test" />);
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/test');
  });

  it('should not render link when not provided', () => {
    render(<FeatureCard {...defaultProps} />);
    const links = screen.queryAllByRole('link');
    expect(links.length).toBe(0);
  });

  it('should render children when provided', () => {
    render(
      <FeatureCard {...defaultProps}>
        <div data-testid="child">Child content</div>
      </FeatureCard>
    );
    expect(screen.getByTestId('child')).toBeInTheDocument();
  });
});

