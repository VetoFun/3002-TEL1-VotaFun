import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { RoomParticipants } from '../RoomParticipants';

describe('RoomParticipants', () => {
  it('renders the RoomParticipants component', () => {
    render(<RoomParticipants />);
    const roomParticipantsElement = screen.getByTestId('participants');
    expect(roomParticipantsElement).toBeInTheDocument();
  });
});
