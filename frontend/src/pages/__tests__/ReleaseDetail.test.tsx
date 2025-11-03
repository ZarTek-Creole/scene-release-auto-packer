/** Tests for ReleaseDetail component. */

import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { ReleaseDetail } from '../ReleaseDetail';
import { releasesApi } from '../../services/releases';

// Mock releasesApi
vi.mock('../../services/releases', () => ({
  releasesApi: {
    get: vi.fn(),
  },
}));

// Mock useParams
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useParams: () => ({ id: '1' }),
  };
});

describe('ReleaseDetail', () => {
  it('should render loading state', () => {
    vi.mocked(releasesApi.get).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    render(
      <BrowserRouter>
        <ReleaseDetail />
      </BrowserRouter>
    );

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('should render release details', async () => {
    const mockRelease = {
      id: 1,
      user_id: 1,
      release_type: 'EBOOK',
      status: 'completed',
      created_at: '2025-01-01T00:00:00Z',
      release_metadata: { title: 'Test Book', author: 'Test Author' },
    };

    vi.mocked(releasesApi.get).mockResolvedValue({
      data: { release: mockRelease },
    });

    render(
      <BrowserRouter>
        <ReleaseDetail />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/test book/i)).toBeInTheDocument();
    });
  });

  it('should render error state', async () => {
    vi.mocked(releasesApi.get).mockRejectedValue(new Error('Not found'));

    render(
      <BrowserRouter>
        <ReleaseDetail />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/erreur/i)).toBeInTheDocument();
    });
  });
});
