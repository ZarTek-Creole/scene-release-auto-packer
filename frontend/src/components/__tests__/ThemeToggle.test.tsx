/** Tests for ThemeToggle component. */

import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { ThemeProvider } from '../../contexts/ThemeContext';
import { ThemeToggle } from '../ThemeToggle';

describe('ThemeToggle', () => {
  it('should render toggle button', () => {
    render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>
    );

    const button = screen.getByLabelText(/switch to/i);
    expect(button).toBeInTheDocument();
  });

  it('should toggle theme on click', async () => {
    const user = userEvent.setup();
    render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>
    );

    const button = screen.getByLabelText(/switch to/i);
    const initialAriaLabel = button.getAttribute('aria-label');

    await user.click(button);

    const newAriaLabel = button.getAttribute('aria-label');
    expect(newAriaLabel).not.toBe(initialAriaLabel);
  });

  it('should have accessible label', () => {
    render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>
    );

    const button = screen.getByLabelText(/switch to/i);
    expect(button).toHaveAttribute('aria-label');
  });
});
