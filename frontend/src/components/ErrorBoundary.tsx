/** Error Boundary pour capturer erreurs React. */

import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

/**
 * Error Boundary pour capturer erreurs React et afficher un fallback.
 * 
 * Ce composant suit les meilleures pratiques React 19 pour la gestion d'erreurs.
 * Il capture les erreurs dans l'arbre de composants enfants et affiche un UI de fallback.
 * 
 * Usage :
 *   <ErrorBoundary>
 *     <YourComponent />
 *   </ErrorBoundary>
 * 
 * Ou avec fallback personnalisé :
 *   <ErrorBoundary fallback={<CustomError />}>
 *     <YourComponent />
 *   </ErrorBoundary>
 */
export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    // Met à jour l'état pour que le prochain rendu affiche le fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log l'erreur pour debugging
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    // Optionnel : envoyer à service de logging (Sentry, LogRocket, etc.)
    // logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Afficher le fallback personnalisé ou le fallback par défaut
      return this.props.fallback || (
        <div className="alert alert-danger m-4">
          <h4 className="alert-heading">Une erreur s'est produite</h4>
          <p className="mb-2">
            {this.state.error?.message || 'Une erreur inattendue s\'est produite.'}
          </p>
          <hr />
          <div className="d-flex gap-2">
            <button
              className="btn btn-primary"
              onClick={() => this.setState({ hasError: false })}
              type="button"
            >
              Réessayer
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => window.location.href = '/'}
              type="button"
            >
              Retour à l'accueil
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

