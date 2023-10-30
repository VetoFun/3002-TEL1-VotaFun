import { act } from 'react-dom/test-utils';
import { useErrorStore } from '../useErrorStore';

describe('useErrorStore', () => {
  it('should initialize with an empty message', () => {
    const { message } = useErrorStore.getState();
    expect(message).toBe('');
  });

  it('should return an empty message when calling getMessage initially', () => {
    const result = useErrorStore.getState().getMessage();
    expect(result).toBe('');
  });

  it('should return the message when calling getMessage after setting a message', () => {
    const newErrorMessage = 'This is an error message';

    act(() => {
      useErrorStore.getState().message = newErrorMessage;
    });

    const result = useErrorStore.getState().getMessage();
    expect(result).toBe(newErrorMessage);
  });

  it('should clear the message after calling getMessage', () => {
    const newErrorMessage = 'This is an error message';

    act(() => {
      useErrorStore.getState().message = newErrorMessage;
    });

    useErrorStore.getState().getMessage();

    const { message } = useErrorStore.getState();
    expect(message).toBe('');
  });
});
