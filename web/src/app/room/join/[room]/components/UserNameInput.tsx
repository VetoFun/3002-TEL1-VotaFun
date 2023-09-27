'use client';

import { useRoomStore } from '@/stores/useRoomStore';
import { useEffect, useState } from 'react';
import { createUser } from '../hooks/createUser';
import { redirect, useParams } from 'next/navigation';
import { joinRoom } from '../hooks/joinRoom';
import useSocketStore, { useGameStore } from '@/stores/useSocketStore';
import { shallow } from 'zustand/shallow';

const UserNameInput = () => {
  const params = useParams();
  const roomId = params.room as string;
  const [username, setUsername] = useState('');

  const actions = useGameStore((state) => state.actions);
  const userId = useGameStore((state) => state.userId);

  useEffect(() => {
    console.log(username, userId);
    if (username && userId) {
      redirect(`/room/lobby/${roomId}`);
    }
  }, [username, roomId, userId]);

  return (
    <div className="flex w-full gap-x-2">
      <input
        type="text"
        className={`input input-bordered h-auto flex-1`}
        placeholder="Enter Username"
        onChange={(e) => {
          setUsername(e.target.value);
        }}
        required={true}
      />
      <button
        className={`btn btn-neutral h-fit flex-none py-4 text-lg ${username.length == 0 ? 'btn-disabled' : ''}`}
        data-tip="Room code cannot be empty"
        data-for="room-code-empty"
        onClick={() => actions.joinRoom(roomId, username)}
      >
        Join
      </button>
    </div>
  );
};

export { UserNameInput };
