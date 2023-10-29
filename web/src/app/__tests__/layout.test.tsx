import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import RootLayout from '../layout';

describe('RootLayout', () => {
  it('renders children and Footer', () => {
    render(
      <RootLayout>
        <div data-testid="child-element">Child Element</div>
      </RootLayout>,
    );

    const childElement = screen.getByTestId('child-element');
    const footer = screen.getByTestId('footer');

    expect(childElement).toBeInTheDocument();
    expect(footer).toBeInTheDocument();
  });
});
