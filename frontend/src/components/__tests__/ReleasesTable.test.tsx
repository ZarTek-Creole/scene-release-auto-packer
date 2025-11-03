/** Tests for ReleasesTable component. */

import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { ReleasesTable } from '../ReleasesTable';
import { releasesApi } from '../../services/releases';

// Mock releasesApi
vi.mock('../../services/releases', () => ({
  releasesApi: {
    list: vi.fn(),
  },
}));

describe('ReleasesTable', () => {
  it('should render loading state', () => {
    vi.mocked(releasesApi.list).mockResolvedValue({
      data: {
        releases: [],
        pagination: { page: 1, per_page: 20, total: 0, pages: 1 },
      },
    });

    render(
      <BrowserRouter>
        <ReleasesTable />
      </BrowserRouter>
    );

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('should render releases list', async () => {
    const mockReleases = [
      {
        id: 1,
        user_id: 1,
        release_type: 'EBOOK',
        status: 'completed',
        created_at: '2025-01-01T00:00:00Z',
        release_metadata: { title: 'Test Book' },
      },
    ];

    vi.mocked(releasesApi.list).mockResolvedValue({
      data: {
        releases: mockReleases,
        pagination: { page: 1, per_page: 20, total: 1, pages: 1 },
      },
    });

    render(
      <BrowserRouter>
        <ReleasesTable />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Book')).toBeInTheDocument();
    });
  });

  it('should render empty state', async () => {
    vi.mocked(releasesApi.list).mockResolvedValue({
      data: {
        releases: [],
        pagination: { page: 1, per_page: 20, total: 0, pages: 1 },
      },
    });

    render(
      <BrowserRouter>
        <ReleasesTable />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/aucune release trouvée/i)).toBeInTheDocument();
    });
  });
});
