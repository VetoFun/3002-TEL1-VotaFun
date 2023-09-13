import { create } from 'zustand'

interface RoomState {
    roomId: string;
    userName: string;
    setRoomId: (roomId: string) => void;
    setUserName: (userName: string) => void;
}

const useRoomStore = create<RoomState>((set) => ({
  roomId: '',
  userName: '',
  setRoomId: (value : string) => set(() => ({ roomId: value })),
  setUserName: (value : string) => set(() => ({ userName: value }))
}))

export {useRoomStore}