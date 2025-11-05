/** Debug panel component for displaying HTTP request/response logs. */

import { useState, useEffect } from 'react';
import { getDebugLogs, clearDebugLogs, isDebugMode, setDebugMode } from '../utils/debug';

/**
 * Debug panel component.
 */
export function DebugPanel() {
  const [logs, setLogs] = useState(getDebugLogs());
  const [isOpen, setIsOpen] = useState(false);
  const [debugEnabled, setDebugEnabled] = useState(isDebugMode());

  useEffect(() => {
    const interval = setInterval(() => {
      setLogs([...getDebugLogs()]);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const handleToggleDebug = () => {
    const newValue = !debugEnabled;
    setDebugMode(newValue);
    setDebugEnabled(newValue);
  };

  const handleClear = () => {
    clearDebugLogs();
    setLogs([]);
  };

  if (!isOpen) {
    return (
      <button
        className="btn btn-sm btn-outline-secondary position-fixed"
        style={{ bottom: '20px', right: '20px', zIndex: 9999 }}
        onClick={() => setIsOpen(true)}
        title="Ouvrir le panneau de debug"
      >
        🔍 Debug
      </button>
    );
  }

  return (
    <div
      className="card position-fixed"
      style={{
        bottom: '20px',
        right: '20px',
        width: '600px',
        maxHeight: '70vh',
        zIndex: 9999,
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      }}
    >
      <div className="card-header d-flex justify-content-between align-items-center">
        <h5 className="mb-0">🔍 Panneau de Debug</h5>
        <div className="d-flex gap-2">
          <div className="form-check form-switch">
            <input
              className="form-check-input"
              type="checkbox"
              checked={debugEnabled}
              onChange={handleToggleDebug}
              id="debug-toggle"
            />
            <label className="form-check-label" htmlFor="debug-toggle">
              Activer
            </label>
          </div>
          <button className="btn btn-sm btn-outline-danger" onClick={handleClear}>
            Effacer
          </button>
          <button className="btn btn-sm btn-outline-secondary" onClick={() => setIsOpen(false)}>
            ✕
          </button>
        </div>
      </div>
      <div className="card-body p-0" style={{ overflowY: 'auto', maxHeight: '60vh' }}>
        {logs.length === 0 ? (
          <div className="p-3 text-muted text-center">Aucun log disponible</div>
        ) : (
          <div className="list-group list-group-flush">
            {logs.map((log, index) => (
              <div key={index} className="list-group-item">
                <div className="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <strong className={`badge ${getStatusBadgeClass(log.status || 0)}`}>
                      {log.method} {log.status || '?'}
                    </strong>
                    {log.statusText && (
                      <span className="badge bg-secondary ms-1">{log.statusText}</span>
                    )}
                    <code className="ms-2 small d-block mt-1">{log.url}</code>
                  </div>
                  <small className="text-muted">{new Date(log.timestamp).toLocaleTimeString()}</small>
                </div>
                {log.headers && Object.keys(log.headers).length > 0 && (
                  <details className="mb-2">
                    <summary className="small text-muted">
                      Headers ({Object.keys(log.headers).length})
                    </summary>
                    <pre className="small bg-light p-2 mt-1 mb-0" style={{ fontSize: '0.75rem', maxHeight: '200px', overflow: 'auto' }}>
                      {JSON.stringify(log.headers, null, 2)}
                    </pre>
                  </details>
                )}
                {log.body !== undefined && (
                  <details className="mb-2">
                    <summary className="small text-muted">Body</summary>
                    <pre className="small bg-light p-2 mt-1 mb-0" style={{ fontSize: '0.75rem' }}>
                      {typeof log.body === 'string'
                        ? log.body
                        : JSON.stringify(log.body, null, 2)}
                    </pre>
                  </details>
                )}
                {log.response !== undefined && (
                  <details className="mb-2">
                    <summary className="small text-muted">
                      Response {log.status && `(${log.status})`}
                    </summary>
                    <pre className="small bg-light p-2 mt-1 mb-0" style={{ fontSize: '0.75rem', maxHeight: '200px', overflow: 'auto' }}>
                      {typeof log.response === 'string'
                        ? log.response
                        : JSON.stringify(log.response, null, 2)}
                    </pre>
                  </details>
                )}
                {log.error && (
                  <div className="alert alert-danger py-2 px-3 mb-0 mt-2">
                    <strong>Erreur:</strong> {log.error}
                  </div>
                )}
                {log.status && log.status >= 400 && !log.error && (
                  <div className="alert alert-warning py-2 px-3 mb-0 mt-2">
                    <strong>HTTP {log.status}:</strong> {log.statusText || 'Erreur'}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function getStatusBadgeClass(status: number): string {
  if (status >= 200 && status < 300) return 'bg-success';
  if (status >= 400 && status < 500) return 'bg-warning';
  if (status >= 500) return 'bg-danger';
  return 'bg-secondary';
}


