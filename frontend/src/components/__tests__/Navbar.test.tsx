/** Tests for Navbar component. */

import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';
import { ThemeProvider } from '../../contexts/ThemeContext';
import { Navbar } from '../Navbar';

describe('Navbar', () => {
  it('should render navigation links', () => {
    render(
      <ThemeProvider>
        <BrowserRouter>
          <Navbar />
        </BrowserRouter>
      </ThemeProvider>
    );

    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Nouvelle Release')).toBeInTheDocument();
    expect(screen.getByText('Liste Releases')).toBeInTheDocument();
  });

  it('should render theme toggle', () => {
    render(
      <ThemeProvider>
        <BrowserRouter>
          <Navbar />
        </BrowserRouter>
      </ThemeProvider>
    );

    const toggleButton = screen.getByLabelText(/switch to/i);
    expect(toggleButton).toBeInTheDocument();
  });

  it('should render icons for navigation items', () => {
    render(
      <ThemeProvider>
        <BrowserRouter>
          <Navbar />
        </BrowserRouter>
      </ThemeProvider>
    );

    // Check that Bootstrap Icons classes are present
    const navLinks = screen.getAllByRole('tab');
    expect(navLinks.length).toBeGreaterThan(0);

    // Check that icons are rendered (Bootstrap Icons use <i> tags)
    const icons = document.querySelectorAll('.bi');
    expect(icons.length).toBeGreaterThan(0);
  });
});
