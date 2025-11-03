/** Theme toggle component. */

import { useTheme } from '../contexts/ThemeContext';

/**
 * Theme toggle button component with Bootstrap Icons.
 */
export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(resolvedTheme === 'light' ? 'dark' : 'light');
  };

  return (
    <button
      type="button"
      className="btn btn-outline-secondary d-flex align-items-center justify-content-center"
      onClick={toggleTheme}
      aria-label={`Switch to ${resolvedTheme === 'light' ? 'dark' : 'light'} mode`}
      style={{ minWidth: '44px', minHeight: '44px' }}
    >
      {resolvedTheme === 'light' ? (
        <i
          className="bi bi-moon"
          style={{ fontSize: '1.25rem', width: '1.25rem', height: '1.25rem' }}
          aria-hidden="true"
        />
      ) : (
        <i
          className="bi bi-sun"
          style={{ fontSize: '1.25rem', width: '1.25rem', height: '1.25rem' }}
          aria-hidden="true"
        />
      )}
    </button>
  );
}
