/** Tests for ReleaseEdit component. */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import { ReleaseEdit } from '../ReleaseEdit';
import * as releasesService from '../../services/releases';

// Mock releasesApi
vi.mock('../../services/releases', () => ({
  releasesApi: {
    get: vi.fn(),
    update: vi.fn(),
  },
}));

interface MockReleasesApi {
  get: ReturnType<typeof vi.fn>;
  update: ReturnType<typeof vi.fn>;
}

const mockReleasesApi = releasesService.releasesApi as unknown as MockReleasesApi;
const mockNavigate = vi.fn();

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
    useParams: () => ({ id: '1' }),
  };
});

describe('ReleaseEdit', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render loading state initially', () => {
    mockReleasesApi.get.mockImplementation(() => new Promise(() => {}));

    render(
      <BrowserRouter>
        <ReleaseEdit />
      </BrowserRouter>
    );

    expect(screen.getByText(/chargement/i)).toBeInTheDocument();
  });

  it('should render edit form when release loaded', async () => {
    mockReleasesApi.get.mockResolvedValue({
      release: {
        id: 1,
        user_id: 1,
        release_type: 'EBOOK',
        status: 'draft',
        release_metadata: { title: 'Test Book' },
        config: { zip_size: 50 },
        created_at: '2025-01-01T00:00:00',
      },
    });

    render(
      <BrowserRouter>
        <ReleaseEdit />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByLabelText(/titre/i)).toBeInTheDocument();
    });

    expect(screen.getByDisplayValue('Test Book')).toBeInTheDocument();
  });

  it('should submit form and navigate on save', async () => {
    mockReleasesApi.get.mockResolvedValue({
      release: {
        id: 1,
        user_id: 1,
        release_type: 'EBOOK',
        status: 'draft',
        release_metadata: { title: 'Original' },
        config: {},
        created_at: '2025-01-01T00:00:00',
      },
    });

    mockReleasesApi.update.mockResolvedValue({
      release: {
        id: 1,
        user_id: 1,
        release_type: 'EBOOK',
        status: 'completed',
        release_metadata: { title: 'Updated' },
        config: {},
        created_at: '2025-01-01T00:00:00',
      },
      message: 'Updated',
    });

    render(
      <BrowserRouter>
        <ReleaseEdit />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByLabelText(/titre/i)).toBeInTheDocument();
    });

    const titleInput = screen.getByLabelText(/titre/i);
    await userEvent.clear(titleInput);
    await userEvent.type(titleInput, 'Updated Title');

    const submitButton = screen.getByRole('button', { name: /sauvegarder/i });
    await userEvent.click(submitButton);

    await waitFor(() => {
      expect(mockReleasesApi.update).toHaveBeenCalledWith(1, expect.objectContaining({
        release_metadata: expect.objectContaining({ title: 'Updated Title' }),
      }));
    });

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/releases/1');
    });
  });
});
