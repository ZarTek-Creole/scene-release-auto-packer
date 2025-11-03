/** Release detail page component. */

import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { PageLayout } from '../components/PageLayout';
import { releasesApi, Release } from '../services/releases';

/**
 * Release detail page component.
 */
export function ReleaseDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [release, setRelease] = useState<Release | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRelease = async () => {
      if (!id) {
        setError('ID de release manquant');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await releasesApi.get(parseInt(id, 10));
        setRelease(response.data?.release || null);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : 'Erreur lors du chargement'
        );
      } finally {
        setLoading(false);
      }
    };

    fetchRelease();
  }, [id]);

  if (loading) {
    return (
      <PageLayout title="Détail Release" description="Chargement...">
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </PageLayout>
    );
  }

  if (error || !release) {
    return (
      <PageLayout title="Détail Release" description="Erreur">
        <div className="alert alert-danger" role="alert">
          {error || 'Release non trouvée'}
        </div>
      </PageLayout>
    );
  }

  const metadata = release.release_metadata || {};
  const title = (metadata.title as string) || `Release #${release.id}`;
  const author = (metadata.author as string) || 'Non spécifié';

  return (
    <PageLayout title={`Release : ${title}`} description={`Auteur : ${author}`}>
      <div className="row">
        <div className="col-md-6">
          <div className="card mb-3">
            <div className="card-header">
              <h5 className="mb-0">Informations Générales</h5>
            </div>
            <div className="card-body">
              <dl className="row">
                <dt className="col-sm-4">ID</dt>
                <dd className="col-sm-8">{release.id}</dd>

                <dt className="col-sm-4">Type</dt>
                <dd className="col-sm-8">
                  <span className="badge bg-primary">
                    {release.release_type}
                  </span>
                </dd>

                <dt className="col-sm-4">Statut</dt>
                <dd className="col-sm-8">
                  <span
                    className={`badge bg-${
                      release.status === 'completed'
                        ? 'success'
                        : release.status === 'draft'
                          ? 'warning'
                          : 'secondary'
                    }`}
                  >
                    {release.status}
                  </span>
                </dd>

                <dt className="col-sm-4">Créé le</dt>
                <dd className="col-sm-8">
                  {new Date(release.created_at).toLocaleString()}
                </dd>

                {release.file_path && (
                  <>
                    <dt className="col-sm-4">Chemin fichier</dt>
                    <dd className="col-sm-8">
                      <code>{release.file_path}</code>
                    </dd>
                  </>
                )}
              </dl>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card mb-3">
            <div className="card-header">
              <h5 className="mb-0">Métadonnées</h5>
            </div>
            <div className="card-body">
              <pre className="bg-light p-3 rounded">
                {JSON.stringify(metadata, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-3">
        <button
          className="btn btn-secondary me-2"
          onClick={() => navigate('/releases')}
          aria-label="Retour à la liste"
        >
          <i className="bi bi-arrow-left" aria-hidden="true" /> Retour
        </button>
        <button
          className="btn btn-primary me-2"
          onClick={() => {
            navigate(`/releases/${release.id}/edit`);
          }}
          aria-label="Éditer cette release"
        >
          <i className="bi bi-pencil" aria-hidden="true" /> Éditer
        </button>
        <button
          className="btn btn-outline-info me-2"
          onClick={async () => {
            try {
              const response = await fetch(
                `/api/releases/${release.id}/actions/nfofix`,
                {
                  method: 'POST',
                  headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                  },
                }
              );
              if (response.ok) {
                alert('NFOFIX job créé avec succès');
              } else {
                alert('Erreur lors de la création du job NFOFIX');
              }
            } catch (err) {
              alert('Erreur lors de la création du job NFOFIX');
            }
          }}
          aria-label="Corriger le fichier NFO"
        >
          <i className="bi bi-file-text" aria-hidden="true" /> NFOFIX
        </button>
        <button
          className="btn btn-outline-warning me-2"
          onClick={async () => {
            try {
              const response = await fetch(
                `/api/releases/${release.id}/actions/repack`,
                {
                  method: 'POST',
                  headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({}),
                }
              );
              if (response.ok) {
                alert('REPACK job créé avec succès');
              } else {
                alert('Erreur lors de la création du job REPACK');
              }
            } catch (err) {
              alert('Erreur lors de la création du job REPACK');
            }
          }}
          aria-label="Repackager cette release"
        >
          <i className="bi bi-arrow-repeat" aria-hidden="true" /> REPACK
        </button>
      </div>
    </PageLayout>
  );
}
