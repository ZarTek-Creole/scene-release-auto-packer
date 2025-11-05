/** Tests for ReleaseActions component. */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import { ReleaseActions } from '../ReleaseActions';
import * as releasesService from '../../services/releases';
import type { ActionResponse } from '../../services/releases';

interface MockReleasesApi {
  nfofix: ReturnType<typeof vi.fn>;
  readnfo: ReturnType<typeof vi.fn>;
  repack: ReturnType<typeof vi.fn>;
  dirfix: ReturnType<typeof vi.fn>;
}

// Mock releasesApi
vi.mock('../../services/releases', () => ({
  releasesApi: {
    nfofix: vi.fn(),
    readnfo: vi.fn(),
    repack: vi.fn(),
    dirfix: vi.fn(),
  },
}));

const mockReleasesApi = releasesService.releasesApi as unknown as MockReleasesApi;

describe('ReleaseActions', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Mock window.prompt for repack
    window.prompt = vi.fn();
  });

  const renderComponent = (props = {}) => {
    return render(
      <BrowserRouter>
        <ReleaseActions releaseId={1} {...props} />
      </BrowserRouter>
    );
  };

  it('should render all action buttons', () => {
    renderComponent();

    expect(screen.getByLabelText('Corriger le fichier NFO')).toBeInTheDocument();
    expect(screen.getByLabelText('Lire NFO et régénérer')).toBeInTheDocument();
    expect(screen.getByLabelText('Repackager la release')).toBeInTheDocument();
    expect(screen.getByLabelText('Corriger la structure de répertoires')).toBeInTheDocument();
  });

  it('should call nfofix API when NFOFIX button clicked', async () => {
    mockReleasesApi.nfofix.mockResolvedValue({
      message: 'Success',
      job_id: 1,
    } as ActionResponse);

    renderComponent();

    const button = screen.getByLabelText('Corriger le fichier NFO');
    await userEvent.click(button);

    await waitFor(() => {
      expect(mockReleasesApi.nfofix).toHaveBeenCalledWith(1);
    });
  });

  it('should call readnfo API when READNFO button clicked', async () => {
    mockReleasesApi.readnfo.mockResolvedValue({
      message: 'Success',
      job_id: 1,
    } as ActionResponse);

    renderComponent();

    const button = screen.getByLabelText('Lire NFO et régénérer');
    await userEvent.click(button);

    await waitFor(() => {
      expect(mockReleasesApi.readnfo).toHaveBeenCalledWith(1);
    });
  });

  it('should call dirfix API when DIRFIX button clicked', async () => {
    mockReleasesApi.dirfix.mockResolvedValue({
      message: 'Success',
      job_id: 1,
    } as ActionResponse);

    renderComponent();

    const button = screen.getByLabelText('Corriger la structure de répertoires');
    await userEvent.click(button);

    await waitFor(() => {
      expect(mockReleasesApi.dirfix).toHaveBeenCalledWith(1);
    });
  });

  it('should call repack API with options when REPACK button clicked', async () => {
    const mockPrompt = vi.fn().mockReturnValue('100');
    window.prompt = mockPrompt;
    mockReleasesApi.repack.mockResolvedValue({
      message: 'Success',
      job_id: 1,
    } as ActionResponse);

    renderComponent();

    const button = screen.getByLabelText('Repackager la release');
    await userEvent.click(button);

    await waitFor(() => {
      expect(mockReleasesApi.repack).toHaveBeenCalledWith(1, { zip_size: 100 });
    });
  });

  it('should display error message on API error', async () => {
    mockReleasesApi.nfofix.mockRejectedValue(new Error('API Error'));

    renderComponent();

    const button = screen.getByLabelText('Corriger le fichier NFO');
    await userEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText(/erreur/i)).toBeInTheDocument();
    });
  });

  it('should call onActionComplete callback after successful action', async () => {
    const onActionComplete = vi.fn();
    mockReleasesApi.nfofix.mockResolvedValue({
      message: 'Success',
      job_id: 1,
    } as ActionResponse);

    renderComponent({ onActionComplete });

    const button = screen.getByLabelText('Corriger le fichier NFO');
    await userEvent.click(button);

    await waitFor(() => {
      expect(onActionComplete).toHaveBeenCalled();
    });
  });
});
