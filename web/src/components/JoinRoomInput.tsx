'use client';

import Link from 'next/link';
import { useState } from 'react';

const JoinRoomInput = () => {
  const [roomCode, setRoomCode] = useState('');

  return (
    <div className="flex w-full gap-x-2">
      <input
        type="text"
        className={`input input-bordered h-auto flex-1 uppercase`}
        placeholder="Enter Room Code"
        onChange={(e) => setRoomCode(e.target.value)}
        required={true}
        value={roomCode}
      />
      <Link
        className={`btn btn-neutral h-fit flex-none py-4 text-lg ${roomCode.length == 0 ? 'btn-disabled' : ''}`}
        data-tip="Room code cannot be empty"
        data-for="room-code-empty"
        href={`/room/join/${roomCode}`}
      >
        Join Room
      </Link>
    </div>
  );
};

export { JoinRoomInput };
