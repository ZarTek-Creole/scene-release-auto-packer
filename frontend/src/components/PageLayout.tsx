/** Page layout component. */

interface PageLayoutProps {
  title: string;
  description?: string;
  children: React.ReactNode;
}

/**
 * Page layout component with consistent structure according to Design System.
 */
export function PageLayout({ title, description, children }: PageLayoutProps) {
  return (
    <div className="container-fluid py-4">
      <div className="row">
        <div className="col-12">
          <h1
            className="mb-3 fw-bold"
            style={{
              fontSize: '1.875rem',
              lineHeight: '1.25',
              color: 'var(--text-primary)',
            }}
          >
            {title}
          </h1>
          {description && (
            <p
              className="mb-4"
              style={{
                fontSize: '1rem',
                lineHeight: '1.75',
                color: 'var(--text-secondary)',
              }}
            >
              {description}
            </p>
          )}
          {children}
        </div>
      </div>
    </div>
  );
}
