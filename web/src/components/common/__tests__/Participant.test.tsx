import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Participant } from '../Participant';

describe('Participant', () => {
  it('renders the participant name', () => {
    const participantProps = {
      userId: '1',
      initial: 'A',
      name: 'Alice',
      host: false,
      isCurrUserHost: false,
    };

    render(<Participant {...participantProps} />);

    const participantName = screen.getByText('Alice');
    expect(participantName).toBeInTheDocument();
  });

  it('renders the crown icon for the host', () => {
    const participantProps = {
      userId: '1',
      initial: 'A',
      name: 'Alice',
      host: true,
      isCurrUserHost: false,
    };

    render(<Participant {...participantProps} />);

    const crownIcon = screen.getByTestId('crown-icon');
    expect(crownIcon).toBeInTheDocument();
  });

  it('renders the kick button for the current user host', () => {
    const participantProps = {
      userId: '1',
      initial: 'A',
      name: 'Alice',
      host: false,
      isCurrUserHost: true,
    };

    render(<Participant {...participantProps} />);

    const kickButton = screen.getByTestId('kick-button');
    expect(kickButton).toBeInTheDocument();
  });
});
