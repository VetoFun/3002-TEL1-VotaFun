import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../page';

describe('Home', () => {
  it('renders the "Create Room" link and "JoinRoomInput"', () => {
    render(<Home />);

    const createRoomLink = screen.getByText('Create Room');
    expect(createRoomLink).toBeInTheDocument();

    const joinButton = screen.getByText('Join Room');
    expect(joinButton).toBeInTheDocument();
  });
});
