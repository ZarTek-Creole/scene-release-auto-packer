/** NFO Viewer component for displaying rule content in monospace format. */

import { useMemo, useState } from 'react';
import './NFOViewer.css';

interface NFOViewerProps {
  content: string;
  lineNumbers?: boolean;
  maxWidth?: number;
  className?: string;
  'aria-label'?: string;
}

/**
 * NFO Viewer component for displaying Scene rules in monospace format.
 */
export function NFOViewer({
  content,
  lineNumbers = false,
  maxWidth = 80,
  className = '',
  'aria-label': ariaLabel = 'NFO Viewer',
}: NFOViewerProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [zoom, setZoom] = useState(100);

  const lines = useMemo(() => content.split('\n'), [content]);

  const highlightedContent = useMemo(() => {
    if (!searchTerm) return content;

    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return content.replace(regex, '<mark>$1</mark>');
  }, [content, searchTerm]);

  const filteredLines = useMemo(() => {
    if (!searchTerm) return lines;

    return lines.filter(line =>
      line.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [lines, searchTerm]);

  return (
    <div className={`nfo-viewer-container ${className}`}>
      <div className="nfo-viewer-toolbar mb-2 d-flex justify-content-between align-items-center">
        <div className="d-flex gap-2 align-items-center">
          <input
            type="text"
            className="form-control form-control-sm"
            placeholder="Rechercher dans le contenu..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            style={{ width: '250px' }}
            aria-label="Recherche dans le contenu NFO"
          />
          <button
            className="btn btn-sm btn-outline-secondary"
            onClick={() => setSearchTerm('')}
            disabled={!searchTerm}
            aria-label="Effacer la recherche"
          >
            ✕
          </button>
        </div>
        <div className="d-flex gap-2 align-items-center">
          <button
            className="btn btn-sm btn-outline-secondary"
            onClick={() => setZoom(Math.max(50, zoom - 10))}
            aria-label="Réduire le zoom"
          >
            −
          </button>
          <span className="small">{zoom}%</span>
          <button
            className="btn btn-sm btn-outline-secondary"
            onClick={() => setZoom(Math.min(200, zoom + 10))}
            aria-label="Augmenter le zoom"
          >
            +
          </button>
          <button
            className="btn btn-sm btn-outline-primary"
            onClick={() => {
              navigator.clipboard.writeText(content);
            }}
            aria-label="Copier le contenu"
          >
            Copier
          </button>
        </div>
      </div>

      <pre
        className="nfo-viewer"
        style={{
          maxWidth: `${maxWidth}ch`,
          fontSize: `${zoom}%`,
        }}
        role="textbox"
        aria-label={ariaLabel}
        aria-readonly="true"
        dangerouslySetInnerHTML={
          searchTerm
            ? { __html: highlightedContent.replace(/\n/g, '<br>') }
            : undefined
        }
      >
        {!searchTerm && content}
      </pre>

      {searchTerm && (
        <div className="mt-2 small text-muted">
          {filteredLines.length} ligne(s) trouvée(s) sur {lines.length}
        </div>
      )}
    </div>
  );
}
