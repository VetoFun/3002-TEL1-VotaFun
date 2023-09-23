import { Room } from '@/types/Room';
import { User } from '@/types/User';
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

type RoomState = {
  room: Room | null;
  user: User | null;
  setRoom(value: Room): void;
  setUser(value: User): void;
};

const useRoomStore = create<RoomState>()(
  persist(
    (set) => ({
      room: null,
      user: null,
      setRoom: (value: Room) => set(() => ({ room: value })),
      setUser: (value: User) => set(() => ({ user: value })),
    }),
    {
      name: 'room-storage',
    },
  ),
);

export { useRoomStore };
