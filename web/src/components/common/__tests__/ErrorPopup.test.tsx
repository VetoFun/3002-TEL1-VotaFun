import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ErrorPopup } from '../ErrorPopup';

HTMLDialogElement.prototype.show = jest.fn(function mock(this: HTMLDialogElement) {
  this.open = true;
});

HTMLDialogElement.prototype.showModal = jest.fn(function mock(this: HTMLDialogElement) {
  this.open = true;
});

HTMLDialogElement.prototype.close = jest.fn(function mock(this: HTMLDialogElement) {
  this.open = false;
});

describe('ErrorPopup', () => {
  it('renders the error message', () => {
    const error = new Error('Test error message');
    render(<ErrorPopup error={error} />);

    const errorMessage = screen.getByText('Test error message');
    expect(errorMessage).toBeInTheDocument();
  });

  it('renders the "Return to Home" link', () => {
    const error = new Error('Test error message');
    render(<ErrorPopup error={error} />);

    const returnLink = screen.getByText('Return to Home');
    expect(returnLink).toBeInTheDocument();
  });
});
