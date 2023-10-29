// import React from 'react';
// import { render, screen } from '@testing-library/react';
// import '@testing-library/jest-dom';
// import { ErrorPopup } from '../ErrorPopup';

// describe('ErrorPopup', () => {
//   it('renders the error message', () => {
//     const error = new Error('Test error message');
//     render(<ErrorPopup error={error} />);

//     const errorMessage = screen.getByText('Test error message');
//     expect(errorMessage).toBeInTheDocument();
//   });

//   it('renders the "Return to Home" link', () => {
//     const error = new Error('Test error message');
//     render(<ErrorPopup error={error} />);

//     const returnLink = screen.getByText('Return to Home');
//     expect(returnLink).toBeInTheDocument();
//   });

//   it('shows the modal when mounted', () => {
//     const error = new Error('Test error message');
//     render(<ErrorPopup error={error} />);

//     const modalElement = screen.getByRole('dialog');
//     expect(modalElement).toHaveAttribute('open', 'true');
//   });
// });
