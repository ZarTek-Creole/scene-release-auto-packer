/** Rule Upload component for uploading local rule files. */

import { useState } from 'react';
import { NFOViewer } from './NFOViewer';
import { rulesApi, Rule } from '../services/rules';

interface RuleUploadProps {
  onUploadSuccess?: (rule: Rule) => void;
  onCancel?: () => void;
}

/**
 * Rule Upload component for uploading local rule files.
 */
export function RuleUpload({
  onUploadSuccess,
  onCancel,
}: RuleUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>('');
  const [metadata, setMetadata] = useState({
    name: '',
    scene: '',
    section: '',
    year: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<Rule | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    // Validate file extension
    const allowedExtensions = ['.nfo', '.txt', '.txt.nfo'];
    const fileName = selectedFile.name.toLowerCase();
    if (
      !allowedExtensions.some(ext => fileName.endsWith(ext))
    ) {
      setError(
        `Type de fichier invalide. Autorisés : ${allowedExtensions.join(', ')}`
      );
      return;
    }

    setFile(selectedFile);
    setError(null);
    setSuccess(null);

    // Set default name from filename
    const nameWithoutExt = selectedFile.name
      .replace(/\.(nfo|txt)$/i, '')
      .replace(/\.txt\.nfo$/i, '');
    setMetadata(prev => ({
      ...prev,
      name: prev.name || nameWithoutExt,
    }));

    // Preview file content
    const reader = new FileReader();
    reader.onload = e => {
      const content = e.target?.result as string;
      setPreview(content);
    };
    reader.onerror = () => {
      setError('Erreur lors de la lecture du fichier');
    };
    reader.readAsText(selectedFile, 'utf-8');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Veuillez sélectionner un fichier');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      if (metadata.name) formData.append('name', metadata.name);
      if (metadata.scene) formData.append('scene', metadata.scene);
      if (metadata.section) formData.append('section', metadata.section);
      if (metadata.year) formData.append('year', metadata.year);

      // Upload via fetch (multipart/form-data)
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/rules/upload', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Erreur lors de l\'upload');
      }

      const data = await response.json();
      setSuccess(data.rule);

      // Update metadata if extracted
      if (data.metadata_extracted) {
        setMetadata(prev => ({
          name: prev.name || data.rule.name,
          scene: prev.scene || data.metadata_extracted.scene || '',
          section:
            prev.section || data.metadata_extracted.section || '',
          year: prev.year || String(data.metadata_extracted.year || ''),
        }));
      }

      if (onUploadSuccess) {
        onUploadSuccess(data.rule);
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Erreur lors de l\'upload'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreview('');
    setMetadata({ name: '', scene: '', section: '', year: '' });
    setError(null);
    setSuccess(null);
  };

  if (success) {
    return (
      <div className="card">
        <div className="card-header bg-success text-white">
          <h5 className="mb-0">Règle uploadée avec succès</h5>
        </div>
        <div className="card-body">
          <p>
            La règle <strong>{success.name}</strong> a été uploadée avec succès.
          </p>
          <div className="d-flex gap-2">
            <button
              className="btn btn-primary"
              onClick={() => {
                handleReset();
                if (onCancel) onCancel();
              }}
            >
              Uploader une autre règle
            </button>
            {onCancel && (
              <button className="btn btn-secondary" onClick={onCancel}>
                Fermer
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header">
        <h5 className="mb-0">Uploader une règle locale</h5>
      </div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="ruleFile" className="form-label">
              Fichier règle <span className="text-danger">*</span>
            </label>
            <input
              id="ruleFile"
              type="file"
              className="form-control"
              accept=".nfo,.txt"
              onChange={handleFileChange}
              required
              aria-describedby="fileHelp"
            />
            <div id="fileHelp" className="form-text">
              Formats acceptés : .nfo, .txt
            </div>
          </div>

          {preview && (
            <div className="mb-3">
              <label className="form-label">Aperçu du contenu</label>
              <div
                className="border rounded p-2"
                style={{ maxHeight: '200px', overflow: 'auto' }}
              >
                <NFOViewer
                  content={preview}
                  maxWidth={80}
                  aria-label="Aperçu du fichier"
                />
              </div>
            </div>
          )}

          <div className="row g-3 mb-3">
            <div className="col-md-6">
              <label htmlFor="ruleName" className="form-label">
                Nom de la règle
              </label>
              <input
                id="ruleName"
                type="text"
                className="form-control"
                value={metadata.name}
                onChange={e =>
                  setMetadata({ ...metadata, name: e.target.value })
                }
                placeholder="Nom de la règle"
              />
            </div>
            <div className="col-md-6">
              <label htmlFor="ruleScene" className="form-label">
                Scene
              </label>
              <input
                id="ruleScene"
                type="text"
                className="form-control"
                value={metadata.scene}
                onChange={e =>
                  setMetadata({ ...metadata, scene: e.target.value })
                }
                placeholder="English, French, etc."
              />
            </div>
            <div className="col-md-6">
              <label htmlFor="ruleSection" className="form-label">
                Section
              </label>
              <input
                id="ruleSection"
                type="text"
                className="form-control"
                value={metadata.section}
                onChange={e =>
                  setMetadata({ ...metadata, section: e.target.value })
                }
                placeholder="eBOOK, TV-720p, etc."
              />
            </div>
            <div className="col-md-6">
              <label htmlFor="ruleYear" className="form-label">
                Année
              </label>
              <input
                id="ruleYear"
                type="number"
                className="form-control"
                value={metadata.year}
                onChange={e =>
                  setMetadata({ ...metadata, year: e.target.value })
                }
                placeholder="2022"
                min="1900"
                max="2100"
              />
            </div>
          </div>

          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}

          <div className="d-flex gap-2">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={!file || loading}
            >
              {loading ? (
                <>
                  <span
                    className="spinner-border spinner-border-sm me-2"
                    role="status"
                    aria-hidden="true"
                  />
                  Upload en cours...
                </>
              ) : (
                'Uploader'
              )}
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleReset}
              disabled={loading}
            >
              Réinitialiser
            </button>
            {onCancel && (
              <button
                type="button"
                className="btn btn-outline-secondary"
                onClick={onCancel}
                disabled={loading}
              >
                Annuler
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
