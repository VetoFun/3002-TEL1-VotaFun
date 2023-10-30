import { render, screen, fireEvent } from '@testing-library/react';
import { JoinRoomInput } from '../JoinRoomInput';

test('it enables the join button when the input is not empty', () => {
  render(<JoinRoomInput />);
  const inputElement = screen.getByPlaceholderText('GAME CODE');
  const joinButton = screen.getByText('Join Room');

  fireEvent.change(inputElement, { target: { value: '12345' } });

  expect(joinButton.classList.contains('btn-disabled')).toBe(false);
});
