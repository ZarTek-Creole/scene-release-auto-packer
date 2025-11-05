/** Accessibility tests for Button component. */

import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { expect, describe, it } from 'vitest';
import { ReactNode } from 'react';

interface ButtonProps {
  onClick?: () => void;
  children: ReactNode;
  'aria-label'?: string;
}

// Mock Button component - replace with actual import when Button exists
const Button = ({ onClick, children, 'aria-label': ariaLabel }: ButtonProps) => (
  <button onClick={onClick} aria-label={ariaLabel}>
    {children}
  </button>
);

expect.extend(toHaveNoViolations);

describe('Button Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(
      <Button onClick={() => {}}>Click me</Button>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have accessible label', () => {
    const { getByRole } = render(
      <Button onClick={() => {}} aria-label="Submit form">
        Submit
      </Button>
    );
    expect(getByRole('button', { name: 'Submit form' })).toBeInTheDocument();
  });

  it('should be keyboard accessible', () => {
    const { getByRole } = render(
      <Button onClick={() => {}}>Click me</Button>
    );
    const button = getByRole('button');
    // Buttons are keyboard accessible by default, tabIndex is not required
    expect(button).toBeInTheDocument();
    expect(button).not.toHaveAttribute('tabIndex', '-1');
  });

  it('should have focus visible', () => {
    const { getByRole } = render(
      <Button onClick={() => {}}>Click me</Button>
    );
    const button = getByRole('button');
    button.focus();
    expect(button).toHaveFocus();
  });
});
