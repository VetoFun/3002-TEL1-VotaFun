'use client';

import { useEffect } from 'react';
import { io } from 'socket.io-client';

export default function Home() {
  useEffect(() => {
    // Replace 'http://localhost:5000' with your Flask SocketIO server URL
    const socket = io('http://localhost:5001/room-management');

    // Event handler for when the client is connected to the server
    socket.on('connect', () => {
      console.log('Connected to Flask SocketIO server');
    });

    // Event handler for custom events from the server
    socket.emit('join_room', { RoomID: 'room1', UserName: 'm_sifii' });

    socket.on('connect_error', (err) => {
      console.log(`connect_error due to ${err.message}`);
    });

    // Clean up the socket connection when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, []);

  return <main className="h-screen w-screen bg-base-100"></main>;
}
