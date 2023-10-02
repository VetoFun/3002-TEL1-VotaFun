// socketStore.js
import { create } from 'zustand';
import { io } from 'socket.io-client';
import { UserState, useRoomStore } from './useRoomStore';
import { use } from 'react';
import { User } from '@/types/User';

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
    .on('create_room_event', (resp) => {
      if (resp.success) {
        set(() => ({ roomId: resp.room_id }));
        console.log(resp.message);
      } else {
        console.error(resp.message);
      }
    })
    .on('join_room_event', (resp) => {
      if (resp.success) {
        const userId = resp.user_id as string;
        set(() => ({ userId: userId }));
        console.log(resp.message);
      } else {
        console.error(resp.message);
      }
    })
    .on('update_room_state_event', (resp) => {
      if (resp.success) {
        const users = resp.room.users as UserState[];
        for (let i = 0; i < users.length; i++) {
          if (resp.room.host_id == users[i].user_id) {
            users[i].is_host = true;
          }
        }
        console.log(resp, users);
        useRoomStore.getState().updateUsers(users);
      }
    })
    .on('disconnect_event', (resp) => {
      // if (resp.success) {
      //   const users = resp.users as UserState[];
      //   useRoomStore.getState().updateUsers(users);
      // }
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
