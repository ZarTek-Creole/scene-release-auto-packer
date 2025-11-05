/** Scenerules.org rules list component. */

import { useEffect, useState } from 'react';
import { NFOViewer } from './NFOViewer';
import { rulesApi } from '../services/rules';

interface ScenerulesRule {
  name: string;
  section: string;
  year: number;
  scene: string;
  url_nfo: string;
  url_html: string;
  is_downloaded?: boolean;
  local_rule_id?: number;
}

interface ScenerulesRulesListProps {
  filters?: {
    scene?: string;
    section?: string;
    year?: number;
  };
  onDownloadSuccess?: () => void;
}

/**
 * Scenerules.org rules list component.
 */
export function ScenerulesRulesList({
  filters = {},
  onDownloadSuccess,
}: ScenerulesRulesListProps) {
  const [rules, setRules] = useState<ScenerulesRule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState<Set<string>>(new Set());
  const [previewRule, setPreviewRule] = useState<ScenerulesRule | null>(null);
  const [previewContent, setPreviewContent] = useState<string>('');

  useEffect(() => {
    const fetchRules = async () => {
      try {
        setLoading(true);
        const response = await rulesApi.listScenerules(filters);
        setRules(response.rules || []);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : 'Failed to load scenerules.org rules'
        );
      } finally {
        setLoading(false);
      }
    };

    fetchRules();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters]);

  const handleDownload = async (rule: ScenerulesRule) => {
    const key = `${rule.section}-${rule.year}`;
    if (downloading.has(key)) return;

    try {
      setDownloading(prev => new Set(prev).add(key));
      setError(null);

      await rulesApi.downloadFromScenerules({
        section: rule.section,
        year: rule.year,
        scene: rule.scene,
      });

      // Refresh list to update is_downloaded status
      const response = await rulesApi.listScenerules(filters);
      setRules(response.rules || []);

      if (onDownloadSuccess) {
        onDownloadSuccess();
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to download rule'
      );
    } finally {
      setDownloading(prev => {
        const next = new Set(prev);
        next.delete(key);
        return next;
      });
    }
  };

  const handlePreview = async (rule: ScenerulesRule) => {
    try {
      setPreviewRule(rule);
      // Fetch preview content from URL
      const response = await fetch(rule.url_nfo);
      if (response.ok) {
        const content = await response.text();
        setPreviewContent(content);
      } else {
        setPreviewContent('Failed to load preview content.');
      }
    } catch (err) {
      setPreviewContent(
        err instanceof Error ? err.message : 'Failed to load preview'
      );
    }
  };

  if (loading) {
    return (
      <div className="text-center">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        {error}
      </div>
    );
  }

  return (
    <div>
      <h3 className="h5 mb-3">Rules disponibles sur scenerules.org</h3>

      {rules.length === 0 ? (
        <div className="alert alert-info" role="alert">
          Aucune règle trouvée avec les filtres sélectionnés.
        </div>
      ) : (
        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead>
              <tr>
                <th>Nom</th>
                <th>Scene</th>
                <th>Section</th>
                <th>Année</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {rules.map((rule, index) => {
                const key = `${rule.section}-${rule.year}-${index}`;
                const isDownloading = downloading.has(
                  `${rule.section}-${rule.year}`
                );

                return (
                  <tr key={key}>
                    <td>{rule.name}</td>
                    <td>{rule.scene}</td>
                    <td>{rule.section}</td>
                    <td>{rule.year}</td>
                    <td>
                      {rule.is_downloaded ? (
                        <span className="badge bg-success">
                          <i className="bi bi-check-circle me-1" aria-hidden="true" />
                          Téléchargée
                        </span>
                      ) : (
                        <span className="badge bg-secondary">Disponible</span>
                      )}
                    </td>
                    <td>
                      <div className="btn-group" role="group">
                        <button
                          className="btn btn-sm btn-outline-info"
                          onClick={() => handlePreview(rule)}
                          aria-label={`Prévisualiser ${rule.name}`}
                        >
                          <i className="bi bi-eye me-1" aria-hidden="true" />
                          Voir
                        </button>
                        <button
                          className="btn btn-sm btn-primary"
                          onClick={() => handleDownload(rule)}
                          disabled={rule.is_downloaded || isDownloading}
                          aria-label={`Télécharger ${rule.name}`}
                        >
                          {isDownloading ? (
                            <>
                              <span
                                className="spinner-border spinner-border-sm me-1"
                                role="status"
                                aria-hidden="true"
                              />
                              Téléchargement...
                            </>
                          ) : (
                            <>
                              <i className="bi bi-download me-1" aria-hidden="true" />
                              Télécharger
                            </>
                          )}
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {previewRule && (
        <div
          className="modal show d-block"
          style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}
          role="dialog"
          aria-modal="true"
          aria-labelledby="previewModalLabel"
        >
          <div className="modal-dialog modal-lg">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="previewModalLabel">
                  {previewRule.name}
                </h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => {
                    setPreviewRule(null);
                    setPreviewContent('');
                  }}
                  aria-label="Fermer"
                />
              </div>
              <div className="modal-body">
                <div className="mb-3">
                  <strong>Source:</strong>{' '}
                  <a
                    href={previewRule.url_html}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {previewRule.url_html}
                  </a>
                </div>
                {previewContent ? (
                  <NFOViewer
                    content={previewContent}
                    maxWidth={80}
                    aria-label={`Contenu de la règle ${previewRule.name}`}
                  />
                ) : (
                  <div className="text-center">
                    <div className="spinner-border" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                  </div>
                )}
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => handleDownload(previewRule)}
                  disabled={
                    previewRule.is_downloaded ||
                    downloading.has(`${previewRule.section}-${previewRule.year}`)
                  }
                >
                  <i className="bi bi-download me-1" aria-hidden="true" />
                  Télécharger
                </button>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setPreviewRule(null);
                    setPreviewContent('');
                  }}
                >
                  Fermer
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
