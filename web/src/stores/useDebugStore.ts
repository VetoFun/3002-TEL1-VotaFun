import { create } from 'zustand'

type DebugState = {
    admin : boolean;
    setAdmin : (value: boolean) => void;
}

const useDebugStore = create<DebugState>((set) => ({
  admin: false,
  setAdmin: (value : boolean) => set(() => ({ admin: value })),
}))

export {useDebugStore}