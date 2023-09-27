// socketStore.js
import { create } from 'zustand';
import { io } from 'socket.io-client';

type GameState = {
  roomId: string;
  userId: string;
  actions: {
    createRoom: () => void;
    joinRoom: (roomId: string, username: string) => void;
  };
};

export const useGameStore = create<GameState>((set) => {
  const socket = io('http://localhost:5001/room-management');
  socket
    .on('connect', () => {})
    .on('disconnect', () => {
      set(() => ({ roomId: '', userId: '' }));
    })
    .on('create_room', (resp) => {
      set(() => ({ roomId: resp.room_id }));
    })
    .on('join_room', (resp) => {
      set(() => ({ userId: resp.user_id }));
    });

  return {
    roomId: '',
    userId: '',
    actions: {
      createRoom: () => {
        socket.emit('create_room', {});
      },
      joinRoom: (roomId: string, username: string) => {
        socket.emit('join_room', { room_id: roomId, user_name: username });
      },
    },
  };
});

export default useGameStore;
