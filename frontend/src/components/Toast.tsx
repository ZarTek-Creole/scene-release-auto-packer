/** Toast notification component for displaying HTTP messages. */

import { useEffect, useState } from 'react';

export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  details?: string;
  timestamp: Date;
}

interface ToastProps {
  message: ToastMessage;
  onClose: (id: string) => void;
}

/**
 * Single toast notification component.
 */
function Toast({ message, onClose }: ToastProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Animation d'entrée
    setTimeout(() => setIsVisible(true), 10);

    // Auto-fermeture après 5 secondes (10 secondes pour les erreurs)
    const timeout = setTimeout(
      () => {
        setIsVisible(false);
        setTimeout(() => onClose(message.id), 300);
      },
      message.type === 'error' ? 10000 : 5000
    );

    return () => clearTimeout(timeout);
  }, [message.id, message.type, onClose]);

  const getIcon = () => {
    switch (message.type) {
      case 'success':
        return '✅';
      case 'error':
        return '❌';
      case 'warning':
        return '⚠️';
      case 'info':
        return 'ℹ️';
      default:
        return 'ℹ️';
    }
  };

  const getAlertClass = () => {
    switch (message.type) {
      case 'success':
        return 'alert-success';
      case 'error':
        return 'alert-danger';
      case 'warning':
        return 'alert-warning';
      case 'info':
        return 'alert-info';
      default:
        return 'alert-info';
    }
  };

  return (
    <div
      className={`alert ${getAlertClass()} alert-dismissible fade ${isVisible ? 'show' : ''}`}
      role="alert"
      style={{
        minWidth: '300px',
        maxWidth: '500px',
        marginBottom: '10px',
        transition: 'opacity 0.3s ease-out, transform 0.3s ease-out',
        opacity: isVisible ? 1 : 0,
        transform: isVisible ? 'translateX(0)' : 'translateX(100%)',
      }}
    >
      <div className="d-flex align-items-start">
        <span className="me-2" style={{ fontSize: '1.2rem' }}>
          {getIcon()}
        </span>
        <div className="flex-grow-1">
          <strong>{message.message}</strong>
          {message.details && (
            <details className="mt-2">
              <summary className="small" style={{ cursor: 'pointer' }}>
                Détails
              </summary>
              <pre className="small mt-2 mb-0 bg-light p-2" style={{ fontSize: '0.75rem' }}>
                {message.details}
              </pre>
            </details>
          )}
          <small className="d-block text-muted mt-1" style={{ fontSize: '0.7rem' }}>
            {message.timestamp.toLocaleTimeString()}
          </small>
        </div>
        <button
          type="button"
          className="btn-close"
          onClick={() => {
            setIsVisible(false);
            setTimeout(() => onClose(message.id), 300);
          }}
          aria-label="Fermer"
        />
      </div>
    </div>
  );
}

/**
 * Toast container component.
 */
export function ToastContainer() {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  useEffect(() => {
    // Écouter les événements de toast depuis n'importe où dans l'app
    const handleToast = (event: CustomEvent<Omit<ToastMessage, 'id' | 'timestamp'>>) => {
      const toast: ToastMessage = {
        ...event.detail,
        id: `toast-${Date.now()}-${Math.random()}`,
        timestamp: new Date(),
      };
      setToasts((prev) => [...prev, toast]);
    };

    window.addEventListener('show-toast', handleToast as EventListener);

    return () => {
      window.removeEventListener('show-toast', handleToast as EventListener);
    };
  }, []);

  const handleClose = (id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  };

  if (toasts.length === 0) return null;

  return (
    <div
      className="position-fixed"
      style={{
        top: '20px',
        right: '20px',
        zIndex: 10000,
        maxWidth: '500px',
      }}
    >
      {toasts.map((toast) => (
        <Toast key={toast.id} message={toast} onClose={handleClose} />
      ))}
    </div>
  );
}

/**
 * Show a toast notification.
 */
export function showToast(
  type: ToastMessage['type'],
  message: string,
  details?: string
): void {
  const event = new CustomEvent('show-toast', {
    detail: { type, message, details },
  });
  window.dispatchEvent(event);
}

