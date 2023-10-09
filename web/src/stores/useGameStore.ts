// socketStore.js
import { create } from 'zustand';
import { io } from 'socket.io-client';
import { User } from '@/types/User';
import { Room } from '@/types/Room';
import { ConnectionStatus } from '@/types/Connection';
import { Question } from '@/types/Question';
import { Option } from '@/types/Option';

type GameStore = {
  status: ConnectionStatus;
  room: Room;
  user: User;
  question: Question;
  option: Option;
  actions: {
    createRoom: () => void;
    joinRoom: (roomId: string, username: string) => void;
    startRoom: () => void;
    vote: (option: string) => void;
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
      question: { question_id: '', question_text: '', options: [], voted: false},
      option: {option_id: '', option_text:'', option_count:0, current_votes:0},
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

  socket.on('client_vote_option_event', (resp) => {
    if (resp.success) {
      set((state) => ({ question: {...state.question, voted: true}}));
    }
  });

  // Socket Global Custom Events
  socket.on('join_room_event', (resp) => {
    if (resp.success) {
      set(() => ({ room: resp.data.room }));
    }
  });

  socket.on('leave_room_event', (resp) => {
    if (resp.success) {
      set(() => ({ room: resp.data.room }));
    }
  });

  socket.on('start_room_event', (resp) => {
    if (resp.success) {
      set(() => ({ status: ConnectionStatus.IN_GAME_WAITING_FOR_SERVER, room: resp.data.room }));
    }
  });

  socket.on('start_round_event', (resp) => {
    if (resp.success) {
      set(() => ({ status: ConnectionStatus.IN_GAME, question: resp.data }));
    }
  });

  socket.on('end_round_event', (resp) => {
    if (resp.success) {
      set(() => ({ status: ConnectionStatus.IN_GAME_WAITING_FOR_SERVER, 
        question: {
          question_id: '',
          question_text: '',
          options: [],
          voted: false,
        },
      }));
    }
  });

  socket.on('end_room_event', (resp) => {
    if(resp.success) {
      // console.log('end room event');
      set(() => ({ status: ConnectionStatus.POST_GAME, option: resp.data.room_result }));
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
    question: { question_id: '', question_text: '', options: [], voted: false},
    option: {option_id: '', option_text:'', option_count:0, current_votes:0},
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
      startRoom() {
        checkConnection();
        const room_id = get().room.room_id;
        const location = get().room.room_location;
        const activity = get().room.room_activity;
        // console.log(room_id, location, activity);
        socket.emit('start_room', { "room_id": room_id, "room_location": location, "room_activity": activity });
      },
      vote(option: string) {
        // console.log(option);
        checkConnection();
        const room_id = get().room.room_id;
        const user_name = get().user.user_name;
        const question_id = get().question.question_id;
        socket.emit('vote_option', { "room_id": room_id, "question_id": question_id, "user_name": user_name, "option_id": option });
      },
    },
  };
});

export default useGameStore;
