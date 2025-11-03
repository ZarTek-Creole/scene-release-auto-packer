/** Navigation bar component. */

import { Link, useLocation } from 'react-router-dom';
// Bootstrap Icons via CSS classes
import { ThemeToggle } from './ThemeToggle';

/**
 * Navigation bar component with Bootstrap Icons.
 */
export function Navbar() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/releases/new', label: 'Nouvelle Release' },
    { path: '/releases', label: 'Liste Releases' },
    { path: '/rules', label: 'Rules' },
    { path: '/users', label: 'Utilisateurs' },
    { path: '/roles', label: 'Rôles' },
    { path: '/config', label: 'Configurations' },
  ];

  function getIconName(path: string): string {
    const iconMap: Record<string, string> = {
      '/': 'house',
      '/releases/new': 'plus',
      '/releases': 'list',
      '/rules': 'file-text',
      '/users': 'people',
      '/roles': 'shield',
      '/config': 'gear',
    };
    return iconMap[path] || 'circle';
  }

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary border-bottom border-primary">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          eBook Scene Packer v2
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto" role="tablist">
            {navItems.map(item => {
              const isActive = location.pathname === item.path;
              return (
                <li key={item.path} className="nav-item" role="presentation">
                  <Link
                    className={`nav-link d-flex align-items-center gap-2 ${
                      isActive ? 'active' : ''
                    }`}
                    to={item.path}
                    role="tab"
                    aria-selected={isActive}
                    aria-controls={`panel-${item.path}`}
                    tabIndex={isActive ? 0 : -1}
                  >
                    <i
                      className={`bi bi-${getIconName(item.path)}`}
                      style={{
                        fontSize: '1.25rem',
                        width: '1.25rem',
                        height: '1.25rem',
                      }}
                      aria-hidden="true"
                    />
                    <span>{item.label}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
          <div className="d-flex">
            <ThemeToggle />
          </div>
        </div>
      </div>
    </nav>
  );
}
