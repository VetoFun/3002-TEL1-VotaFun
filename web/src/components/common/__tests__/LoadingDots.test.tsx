import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { LoadingDots } from '../LoadingDots';

describe('LoadingDots', () => {
  it('renders three dots', () => {
    render(<LoadingDots />);
    const dots = screen.getAllByTestId('loading-dot');
    expect(dots).toHaveLength(3);
  });

  it('applies the correct CSS classes from the CSS module', () => {
    render(<LoadingDots />);
    const dots = screen.getAllByTestId('loading-dot');

    for (const dot of dots) {
      expect(dot).toHaveClass('animate-bounce rounded-full bg-accent-content');
    }
  });
});
