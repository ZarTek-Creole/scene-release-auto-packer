/** Releases API service. */

import { apiRequest } from './api';

export interface Release {
  id: number;
  user_id: number;
  group_id?: number;
  release_type: string;
  status: string;
  release_metadata?: Record<string, unknown>;
  config?: Record<string, unknown>;
  file_path?: string;
  created_at: string;
}

export interface ReleaseListParams {
  page?: number;
  per_page?: number;
  release_type?: string;
  status?: string;
  user_id?: number;
  group_id?: number;
  search?: string;
  sort?: string;
  order?: 'asc' | 'desc';
}

export interface ReleaseListResponse {
  releases: Release[];
  pagination: {
    page: number;
    per_page: number;
    total: number;
    pages: number;
  };
}

export const releasesApi = {
  /**
   * List releases with filters and pagination.
   */
  async list(params: ReleaseListParams = {}) {
    const queryParams = new URLSearchParams();
    if (params.page) queryParams.append('page', params.page.toString());
    if (params.per_page) queryParams.append('per_page', params.per_page.toString());
    if (params.release_type) queryParams.append('release_type', params.release_type);
    if (params.status) queryParams.append('status', params.status);
    if (params.user_id) queryParams.append('user_id', params.user_id.toString());
    if (params.group_id) queryParams.append('group_id', params.group_id.toString());
    if (params.search) queryParams.append('search', params.search);
    if (params.sort) queryParams.append('sort', params.sort);
    if (params.order) queryParams.append('order', params.order);

    return apiRequest<ReleaseListResponse>(
      `/releases?${queryParams.toString()}`
    );
  },

  /**
   * Get release by ID.
   */
  async get(releaseId: number) {
    return apiRequest<{ release: Release }>(`/releases/${releaseId}`);
  },

  /**
   * Update release.
   */
  async update(releaseId: number, data: Partial<Release>) {
    return apiRequest<{ release: Release }>(`/releases/${releaseId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete release.
   */
  async delete(releaseId: number) {
    return apiRequest<{ message: string }>(`/releases/${releaseId}`, {
      method: 'DELETE',
    });
  },
};
