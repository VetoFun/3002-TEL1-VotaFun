// socketStore.js
import { create } from 'zustand';
import { io } from 'socket.io-client';
import { User } from '@/types/User';
import { Room } from '@/types/Room';
import { ConnectionStatus } from '@/types/Connection';

type GameStore = {
  status: ConnectionStatus;
  room: Room;
  user: User;
  actions: {
    createRoom: () => void;
    joinRoom: (roomId: string, username: string) => void;
    kickUser: (roomId: string, userId: string, userName: string) => void;
    sendRoomProperties: (roomId: string, location: string, activity: string) => void;
  };
};

export const useGameStore = create<GameStore>((set, get) => {
  const socket = io('http://localhost:5001/room-management');

  const checkConnection = () => {
    // if (get().status == ConnectionStatus.DISCONNECTED) throw new Error('You are not connected');
  };

  const reset = () => {
    socket.disconnect();

    set(() => ({
      status: ConnectionStatus.DISCONNECTED,
      room: {
        room_id: '',
        number_of_user: 0,
        max_capacity: 0,
        last_activity: '',
        questions: [],
        host_id: '',
        status: '',
        room_location: '',
        room_activity: '',
        users: [],
      },
      user: {
        user_id: '',
        user_name: '',
      },
    }));
  };

  // Socket Standard Events
  // socket.onAny((event, ...args) => {
  //   console.debug(event, args);
  // });

  socket.on('connect', () => {
    if (get().status == ConnectionStatus.DISCONNECTED && socket.connected) {
      set(() => ({ status: ConnectionStatus.CONNECTED, user: { user_id: socket.id, user_name: '' } }));
    }
  });

  socket.on('disconnect', () => {
    if (socket.disconnected) reset();
  });

  // Socket Client Custom Events
  // client_create_room_event : resp.success, resp.message, resp.room_id
  socket.on('client_create_room_event', (resp) => {
    if (resp.success) {
      // console.log(resp);
      set(() => ({ room: resp.data.room }));
    } else {
      throw new Error(resp.message);
    }
  });

  // client_join_room_event : resp.success, resp.message, resp.room
  socket.on('client_join_room_event', (resp) => {
    if (resp.success) {
      set(() => ({
        room: resp.data.room,
        status: ConnectionStatus.IN_LOBBY,
      }));
    } else {
      // console.error(resp.message);
      throw new Error(resp.message);
    }
  });

  // Socket Global Custom Events
  socket.on('join_room_event', (resp) => {
    if (resp.success) {
      set(() => ({ room: resp.data.room }));
    }
  });

  socket.on('kick_user_event', (resp) => {
    if (resp.success) {
      set(() => ({ room: resp.data.room }));
    }
  });

  socket.on('leave_room_event', (resp) => {
    if (resp.success) {
      set(() => ({ room: resp.data.room }));
    }
  });

  socket.on('set_room_properties_event', (resp) => {
    if (resp.success) {
      set(() => ({ room: resp.data.room }));
    }
  });

  return {
    status: ConnectionStatus.DISCONNECTED,
    room: {
      room_id: '',
      number_of_user: 0,
      max_capacity: 0,
      last_activity: '',
      questions: [],
      host_id: '',
      status: '',
      room_location: '',
      room_activity: '',
      users: [],
    },
    user: {
      user_id: '',
      user_name: '',
    },
    actions: {
      createRoom() {
        checkConnection();
        socket.emit('create_room', {});
      },
      joinRoom(roomId: string, userName: string) {
        checkConnection();
        // if (get().room.room_id) throw new Error('You are already in a room');
        if (!roomId) throw new Error('Room ID is not provided when joining a room');
        if (!userName) throw new Error('Username is not provided when joining a room');

        socket.emit('join_room', { room_id: roomId, user_name: userName });
        set(() => ({ user: { user_id: socket.id, user_name: userName } }));
      },
      kickUser(roomId: string, userId: string, userName: string) {
        if (!roomId) throw new Error('Room ID is not provided when kicking user');
        if (!userId) throw new Error('UserId is not provided when kicking user');
        if (!userName) throw new Error('Username is not provided when kicking user');
        socket.emit('kick_user', { room_id: roomId, user_id: userId, user_name: userName });
      },
      sendRoomProperties(roomId: string, location: string, activity: string) {
        if (!roomId) throw new Error('Room ID is not provided when setting room properties');
        socket.emit('set_room_properties', { room_id: roomId, room_activity: activity, room_location: location });
      },
    },
  };
});

export default useGameStore;
