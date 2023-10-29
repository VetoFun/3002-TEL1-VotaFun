import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { RoomLayout } from '../RoomLayout';

describe('RoomLayout', () => {
  it('renders children and RoomParticipants', () => {
    render(
      <RoomLayout>
        <div data-testid="child-element">Child Element</div>
      </RoomLayout>,
    );

    const childElement = screen.getByTestId('child-element');
    const roomParticipants = screen.getByTestId('participants');

    expect(childElement).toBeInTheDocument();
    expect(roomParticipants).toBeInTheDocument();
  });
});
