/** Rules page component. */

import { useState } from 'react';
import { PageLayout } from '../components/PageLayout';
import { RulesTable } from '../components/RulesTable';
import { NFOViewer } from '../components/NFOViewer';
import { RuleUpload } from '../components/RuleUpload';
import { Rule } from '../services/rules';

/**
 * Rules page component.
 */
export function Rules() {
  const [filters, setFilters] = useState<{
    scene?: string;
    section?: string;
    year?: number;
    search?: string;
  }>({});
  const [selectedRule, setSelectedRule] = useState<Rule | null>(null);
  const [showUpload, setShowUpload] = useState(false);

  return (
    <PageLayout title="Règles" description="Gérer les règles Scene">
      <div className="mb-4 d-flex justify-content-between align-items-center">
        <h2 className="h4 mb-0">Règles locales</h2>
        <button
          className="btn btn-primary"
          onClick={() => setShowUpload(!showUpload)}
          aria-label="Uploader une règle"
        >
          <i className="bi bi-upload me-2" aria-hidden="true" />
          Uploader une règle
        </button>
      </div>

      {showUpload && (
        <div className="mb-4">
          <RuleUpload
            onUploadSuccess={rule => {
              setShowUpload(false);
              setSelectedRule(null);
              // Refresh table by resetting filters
              setFilters({ ...filters });
            }}
            onCancel={() => setShowUpload(false)}
          />
        </div>
      )}

      <div className="mb-4">
        <div className="row g-3 mb-3">
          <div className="col-md-12">
            <label htmlFor="filterSearch" className="form-label">
              Recherche
            </label>
            <input
              id="filterSearch"
              type="text"
              className="form-control"
              value={filters.search || ''}
              onChange={e =>
                setFilters({ ...filters, search: e.target.value || undefined })
              }
              placeholder="Rechercher dans le nom ou le contenu..."
            />
          </div>
        </div>
        <div className="row g-3">
          <div className="col-md-4">
            <label htmlFor="filterScene" className="form-label">
              Scene
            </label>
            <input
              id="filterScene"
              type="text"
              className="form-control"
              value={filters.scene || ''}
              onChange={e =>
                setFilters({ ...filters, scene: e.target.value || undefined })
              }
              placeholder="Filtrer par scene"
            />
          </div>
          <div className="col-md-4">
            <label htmlFor="filterSection" className="form-label">
              Section
            </label>
            <input
              id="filterSection"
              type="text"
              className="form-control"
              value={filters.section || ''}
              onChange={e =>
                setFilters({ ...filters, section: e.target.value || undefined })
              }
              placeholder="Filtrer par section"
            />
          </div>
          <div className="col-md-4">
            <label htmlFor="filterYear" className="form-label">
              Année
            </label>
            <input
              id="filterYear"
              type="number"
              className="form-control"
              value={filters.year || ''}
              onChange={e =>
                setFilters({
                  ...filters,
                  year: e.target.value
                    ? parseInt(e.target.value, 10)
                    : undefined,
                })
              }
              placeholder="Filtrer par année"
            />
          </div>
        </div>
        <div className="mt-3">
          <button className="btn btn-secondary" onClick={() => setFilters({})}>
            Réinitialiser
          </button>
        </div>
      </div>

      <RulesTable
        filters={filters}
        onEdit={rule => setSelectedRule(rule)}
        onDelete={() => setSelectedRule(null)}
      />

      {selectedRule && (
        <div
          className="modal show d-block"
          style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}
        >
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">{selectedRule.name}</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setSelectedRule(null)}
                ></button>
              </div>
              <div className="modal-body">
                <NFOViewer
                  content={selectedRule.content}
                  lineNumbers={false}
                  maxWidth={80}
                  aria-label={`Contenu de la règle ${selectedRule.name}`}
                />
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setSelectedRule(null)}
                >
                  Fermer
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </PageLayout>
  );
}
