/** Login page component. */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authApi } from '../services/api';
import { PageLayout } from '../components/PageLayout';

/**
 * Login page component.
 */
export function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await authApi.login(username, password);
      
      // Success message already displayed by authApi.login via toast
      // Navigate to dashboard après un court délai pour voir le toast
      setTimeout(() => {
        navigate('/');
      }, 500);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erreur de connexion';
      setError(errorMessage);
      // Toast d'erreur déjà affiché par authApi.login
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageLayout title="Connexion">
      <div className="row justify-content-center">
        <div className="col-md-4">
          <div className="card border rounded-lg shadow-sm">
            <div className="card-body p-4">
              <h2 className="card-title mb-4 text-center">Connexion</h2>
              
              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="username" className="form-label">
                    Nom d'utilisateur
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    autoFocus
                    autoComplete="username"
                    aria-describedby="username-help"
                  />
                  <div id="username-help" className="form-text">
                    Entrez votre nom d'utilisateur
                  </div>
                </div>

                <div className="mb-3">
                  <label htmlFor="password" className="form-label">
                    Mot de passe
                  </label>
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    autoComplete="current-password"
                    aria-describedby="password-help"
                  />
                  <div id="password-help" className="form-text">
                    Entrez votre mot de passe
                  </div>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary w-100"
                  disabled={loading}
                  aria-busy={loading}
                >
                  {loading ? (
                    <>
                      <span
                        className="spinner-border spinner-border-sm me-2"
                        role="status"
                        aria-hidden="true"
                      />
                      Connexion...
                    </>
                  ) : (
                    'Se connecter'
                  )}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

