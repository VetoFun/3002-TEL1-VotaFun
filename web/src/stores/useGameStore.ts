// socketStore.js
import { create } from 'zustand';
import { io } from 'socket.io-client';
import { useRoomStore } from './useRoomStore';
import { use } from 'react';

type GameState = {
  roomId: string;
  userId: string;
  actions: {
    createRoom: () => void;
    joinRoom: (roomId: string, username: string) => void;
  };
};

export const useGameStore = create<GameState>((set, get) => {
  const socket = io('http://localhost:5001/room-management');
  socket
    .onAny((event, ...args) => {
      console.log(event, args);
    })
    .on('connect', () => {})
    .on('disconnect', () => {
      // set(() => ({ roomId: '', userId: '' }));
      // useRoomStore.getState().(resp);
    })
    .on('create_room', (resp) => {
      if (!get().roomId) set(() => ({ roomId: resp.room_id })); // bug - may change whenever anyone joins
    })
    .on('join_room', (resp) => {
      if (!get().userId) set(() => ({ userId: resp.user_id })); // bug - may change whenever anyone joins
    })
    .on('update_room', (resp) => {
      useRoomStore.getState().updateUsers(resp);
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
