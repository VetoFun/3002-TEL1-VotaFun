import { useGameStore } from '../useGameStore';
import { ConnectionStatus } from '@/types/Connection';

describe('useGameStore', () => {
  it('should initialize with the correct default state', () => {
    const { status, room, user, question, option } = useGameStore.getState();

    expect(status).toBe(ConnectionStatus.DISCONNECTED);
    expect(room.room_id).toBe('');
    expect(user.user_id).toBe('');
    expect(question.question_id).toBe('');
    expect(option.option_id).toBe('');
  });
});
