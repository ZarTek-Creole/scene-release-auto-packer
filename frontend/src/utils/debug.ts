/** Debug utilities for HTTP requests and responses. */

// Mode debug activé par défaut en développement, ou si explicitement activé
const DEBUG_MODE =
  import.meta.env.DEV ||
  import.meta.env.VITE_DEBUG === 'true' ||
  localStorage.getItem('debug_mode') === 'true';

export interface DebugInfo {
  url: string;
  method: string;
  headers: Record<string, string>;
  body?: unknown;
  status?: number;
  statusText?: string;
  response?: unknown;
  error?: string;
  timestamp: string;
}

const debugLog: DebugInfo[] = [];
const MAX_DEBUG_ENTRIES = 50;

/**
 * Log debug information about an HTTP request/response.
 */
export function logDebug(info: DebugInfo): void {
  // Toujours logger en mémoire (même si debug désactivé) pour le panneau debug
  debugLog.unshift(info);
  if (debugLog.length > MAX_DEBUG_ENTRIES) {
    debugLog.pop();
  }

  // Log to console seulement si debug activé
  if (DEBUG_MODE) {
    console.group(`🔍 [DEBUG] ${info.method} ${info.url}`);
    console.log('Headers:', info.headers);
    if (info.body) console.log('Body:', info.body);
    if (info.status) {
      console.log(`Status: ${info.status} ${info.statusText || ''}`);
    }
    if (info.response) console.log('Response:', info.response);
    if (info.error) console.error('Error:', info.error);
    console.log('Timestamp:', info.timestamp);
    console.groupEnd();
  }
}

/**
 * Get all debug logs.
 */
export function getDebugLogs(): DebugInfo[] {
  return debugLog;
}

/**
 * Clear debug logs.
 */
export function clearDebugLogs(): void {
  debugLog.length = 0;
}

/**
 * Check if debug mode is enabled.
 */
export function isDebugMode(): boolean {
  return DEBUG_MODE;
}

/**
 * Toggle debug mode.
 */
export function setDebugMode(enabled: boolean): void {
  localStorage.setItem('debug_mode', enabled.toString());
  // Reload to apply changes
  if (enabled !== DEBUG_MODE) {
    window.location.reload();
  }
}


