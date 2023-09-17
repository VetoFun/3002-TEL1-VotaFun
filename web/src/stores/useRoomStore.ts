import { create } from 'zustand'

interface RoomState {
    roomId: string;
    userName: string;
    activity: string;
    location: string;
    isHost: boolean;
    setRoomId: (value: string) => void;
    setUserName: (value: string) => void;
    setActivity: (value: string) => void;
    setLocation: (value: string) => void;
    setIsHost: (value: boolean) => void;
}

const useRoomStore = create<RoomState>((set) => ({
  roomId: '',
  userName: '',
  activity: '',
  location: '',
  isHost: false,
  setRoomId: (value : string) => set(() => ({ roomId: value })),
  setUserName: (value : string) => set(() => ({ userName: value })),
  setActivity: (value : string) => set(() => ({ activity: value })),
  setLocation: (value : string) => set(() => ({ location: value })),
  setIsHost: (value : boolean) => set(() => ({ isHost: value }))
}))

export {useRoomStore}