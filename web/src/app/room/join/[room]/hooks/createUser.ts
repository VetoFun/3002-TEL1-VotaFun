import { User } from '@/types/User';
import { io } from 'socket.io-client';

const SOCKET_SERVER_URL = 'http://localhost:5001/room-management'; // Replace with your server URL

const createUser = (roomId: string, username: string): Promise<User> => {
  return new Promise((resolve, reject) => {
    // Create the Socket.IO connection
    const socket = io(SOCKET_SERVER_URL);

    socket.on('connect', () => {
      console.log(`Connected to Socket.IO server, socketID: ${socket.id}`);

      // Emit a custom event to inform the server about the user (you can define your own event)
      socket.emit('join_room', { room_id: roomId, user_name: username });

      // Create the user object with the socket ID
      const newUser: User = {
        id: socket.id,
        username: username,
      };

      // Resolve the promise with the user object
      resolve(newUser);
    });

    socket.on('connect_error', (err) => {
      console.log(`connect_error due to ${err.message}`);
      // Reject the promise in case of an error
      reject(err);
    });
  });
};

export { createUser };
