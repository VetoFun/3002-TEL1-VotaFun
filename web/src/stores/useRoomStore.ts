import { create } from 'zustand';

type UserState = {
  user_id: string;
  user_name: string;
  is_host: boolean;
};

type RoomState = {
  room_id: string;
  users: UserState[];
  location: string;
  activity: string;

  setLocation(location: string): void;
  setActivity(activity: string): void;
  updateUsers(users: UserState[]): void;
  _addUser(user: UserState): void;
  _removeUser(user: UserState): void;
};

const useRoomStore = create<RoomState>()((set) => ({
  room_id: '',
  users: [],

  location: '',
  activity: '',

  setLocation: (location) => {
    set(() => ({ location }));
  },

  setActivity: (activity) => {
    set(() => ({ activity }));
  },

  updateUsers: (users) => {
    set(() => ({ users }));
  },

  _addUser: (user) => {
    set((state: RoomState) => ({ users: [...state.users, user] }));
  },

  _removeUser: (user) => {
    set((state: RoomState) => ({
      users: state.users.filter((u: UserState) => u.user_id !== user.user_id),
    }));
  },
}));

export { useRoomStore };
