'use client';

import { useEffect } from 'react';
import { io } from 'socket.io-client';

export default function Home() {
  useEffect(() => {
    // Replace 'http://localhost:5000' with your Flask SocketIO server URL
    const socket = io('http://127.0.0.1:5001');

    // Event handler for when the client is connected to the server
    socket.on('connect', () => {
      console.log('Connected to Flask SocketIO server');
    });

    // Event handler for custom events from the server
    socket.on('custom_event', (data) => {
      console.log('Received custom event:', data);
    });

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
