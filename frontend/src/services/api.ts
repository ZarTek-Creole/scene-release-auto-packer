/** API service for backend communication. */

import { logDebug } from '../utils/debug';
import { showToast } from '../components/Toast';

// In Docker, use relative path for nginx proxy, otherwise use full URL
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || '/api';

export interface ApiResponse<T> {
  data?: T;
  message?: string;
}

/**
 * Get authorization token from localStorage.
 */
function getAuthToken(): string | null {
  return localStorage.getItem('access_token');
}

/**
 * API request with authentication.
 */
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };

  // Don't set Content-Type for FormData (browser sets it automatically)
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const url = `${API_BASE_URL}${endpoint}`;
  const timestamp = new Date().toISOString();

  // Log request
  logDebug({
    url,
    method: options.method || 'GET',
    headers,
    body: options.body ? (options.body instanceof FormData ? '[FormData]' : JSON.parse(options.body as string)) : undefined,
    timestamp,
  });

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Log response
    const responseData = await response.json().catch(() => ({}));
    logDebug({
      url,
      method: options.method || 'GET',
      headers,
      status: response.status,
      statusText: response.statusText,
      response: responseData,
      timestamp,
    });

    if (!response.ok) {
      const errorMessage = responseData.message || `HTTP ${response.status}`;
      const errorDetails = JSON.stringify({
        status: response.status,
        statusText: response.statusText,
        response: responseData,
      }, null, 2);

      // Afficher toast d'erreur
      showToast('error', `Erreur HTTP ${response.status}`, errorDetails);

      // Log error
      logDebug({
        url,
        method: options.method || 'GET',
        headers,
        status: response.status,
        statusText: response.statusText,
        response: responseData,
        error: errorMessage,
        timestamp,
      });

      throw new Error(errorMessage);
    }

    // Afficher toast de succès pour les méthodes non-GET
    if (options.method && options.method !== 'GET') {
      const successMessage = responseData.message || `${options.method} réussi`;
      showToast('success', successMessage);
    }

    return responseData;
  } catch (error) {
    // Log error
    const errorMessage = error instanceof Error ? error.message : String(error);
    logDebug({
      url,
      method: options.method || 'GET',
      headers,
      error: errorMessage,
      timestamp,
    });

    // Afficher toast d'erreur réseau
    if (error instanceof TypeError && error.message.includes('fetch')) {
      showToast('error', 'Erreur de connexion', 'Impossible de se connecter au serveur');
    } else {
      showToast('error', 'Erreur', errorMessage);
    }

    throw error;
  }
}

/**
 * Dashboard API.
 */
export const dashboardApi = {
  /**
   * Get dashboard statistics.
   */
  async getStats() {
    return apiRequest<{
      total_releases: number;
      total_jobs: number;
      user_releases: number;
      user_jobs: number;
      user: {
        id: number;
        username: string;
        email: string;
        active: boolean;
      };
    }>('/dashboard/stats');
  },
};

/**
 * Auth API.
 */
export const authApi = {
  /**
   * Login.
   */
  async login(username: string, password: string) {
    const url = `${API_BASE_URL}/auth/login`;
    const timestamp = new Date().toISOString();
    const body = JSON.stringify({ username, password });

    // Log request
    logDebug({
      url,
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: { username, password: '***' }, // Hide password in logs
      timestamp,
    });

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
    });

    const responseData = await response.json().catch(() => ({}));

    // Log response
    logDebug({
      url,
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      status: response.status,
      statusText: response.statusText,
      response: responseData,
      timestamp,
    });

    if (!response.ok) {
      const errorMessage = responseData.message || 'Échec de la connexion';
      const errorDetails = JSON.stringify({
        status: response.status,
        statusText: response.statusText,
        response: responseData,
      }, null, 2);

      // Afficher toast d'erreur
      showToast('error', errorMessage, errorDetails);

      throw new Error(errorMessage);
    }

    const data = responseData;
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token || '');
      
      // Afficher toast de succès
      showToast('success', 'Connexion réussie', `Bienvenue ${data.user?.username || ''}`);
    }
    return data;
  },

  /**
   * Logout.
   */
  async logout() {
    await apiRequest('/auth/logout', { method: 'POST' });
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  /**
   * Get current user.
   */
  async getCurrentUser() {
    return apiRequest<{
      user: { id: number; username: string; email: string };
    }>('/auth/me');
  },
};
