import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Loader } from '../Loader';

describe('Loader', () => {
  it('renders the "Joining Room" text', () => {
    render(<Loader />);
    const textElement = screen.getByText('Joining Room');
    expect(textElement).toBeInTheDocument();
  });

  it('renders the loader component', () => {
    render(<Loader />);
    const loaderElement = screen.getByTestId('loader');
    expect(loaderElement).toBeInTheDocument();
  });
});
