/** Rules API service. */

import { apiRequest } from './api';

export interface Rule {
  id: number;
  name: string;
  content: string;
  scene?: string;
  section?: string;
  year?: number;
  created_at: string;
  updated_at: string;
}

export interface ListRulesParams {
  page?: number;
  per_page?: number;
  scene?: string;
  section?: string;
  year?: number;
  search?: string;
}

export interface CreateRuleData {
  name: string;
  content: string;
  scene?: string;
  section?: string;
  year?: number;
}

export interface UpdateRuleData {
  name?: string;
  content?: string;
  scene?: string;
  section?: string;
  year?: number;
}

export const rulesApi = {
  /**
   * List rules.
   */
  async list(params: ListRulesParams = {}) {
    const queryParams = new URLSearchParams();
    if (params.page) queryParams.append('page', params.page.toString());
    if (params.per_page)
      queryParams.append('per_page', params.per_page.toString());
    if (params.scene) queryParams.append('scene', params.scene);
    if (params.section) queryParams.append('section', params.section);
    if (params.year) queryParams.append('year', params.year.toString());
    if (params.search) queryParams.append('search', params.search);

    const queryString = queryParams.toString();
    return apiRequest<{
      rules: Rule[];
      pagination: {
        page: number;
        per_page: number;
        total: number;
        pages: number;
      };
    }>(`/rules${queryString ? `?${queryString}` : ''}`);
  },

  /**
   * Get rule by ID.
   */
  async get(ruleId: number) {
    return apiRequest<{ rule: Rule }>(`/rules/${ruleId}`);
  },

  /**
   * Create rule.
   */
  async create(data: CreateRuleData) {
    return apiRequest<{ rule: Rule }>('/rules', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update rule.
   */
  async update(ruleId: number, data: UpdateRuleData) {
    return apiRequest<{ rule: Rule }>(`/rules/${ruleId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete rule.
   */
  async delete(ruleId: number) {
    return apiRequest<{ message: string }>(`/rules/${ruleId}`, {
      method: 'DELETE',
    });
  },

  /**
   * List available rules on scenerules.org.
   */
  async listScenerules(params?: {
    scene?: string;
    section?: string;
    year?: number;
  }) {
    const queryParams = new URLSearchParams();
    if (params?.scene) queryParams.append('scene', params.scene);
    if (params?.section) queryParams.append('section', params.section);
    if (params?.year) queryParams.append('year', params.year.toString());

    const queryString = queryParams.toString();
    return apiRequest<{
      rules: Array<{
        name: string;
        section: string;
        year: number;
        scene: string;
        url_nfo: string;
        url_html: string;
        is_downloaded?: boolean;
        local_rule_id?: number;
      }>;
      total: number;
    }>(`/rules/scenerules${queryString ? `?${queryString}` : ''}`);
  },

  /**
   * Download rule from scenerules.org.
   */
  async downloadFromScenerules(data: {
    section?: string;
    year?: number;
    scene?: string;
    url?: string;
  }) {
    return apiRequest<{
      rule: Rule;
      message: string;
      was_existing: boolean;
    }>('/rules/scenerules/download', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};
