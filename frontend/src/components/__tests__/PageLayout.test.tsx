/** Tests for PageLayout component. */

import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { PageLayout } from '../PageLayout';

describe('PageLayout', () => {
  it('should render title', () => {
    render(
      <PageLayout title="Test Page">
        <div>Content</div>
      </PageLayout>
    );

    expect(screen.getByText('Test Page')).toBeInTheDocument();
  });

  it('should render description when provided', () => {
    render(
      <PageLayout title="Test Page" description="Test description">
        <div>Content</div>
      </PageLayout>
    );

    expect(screen.getByText('Test description')).toBeInTheDocument();
  });

  it('should render children', () => {
    render(
      <PageLayout title="Test Page">
        <div data-testid="content">Content</div>
      </PageLayout>
    );

    expect(screen.getByTestId('content')).toBeInTheDocument();
  });

  it('should not render description when not provided', () => {
    render(
      <PageLayout title="Test Page">
        <div>Content</div>
      </PageLayout>
    );

    expect(screen.queryByText(/description/i)).not.toBeInTheDocument();
  });
});
