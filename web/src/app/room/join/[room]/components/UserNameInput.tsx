'use client';

import { useEffect, useState } from 'react';
import { RedirectType, redirect, useParams } from 'next/navigation';
import useGameStore from '@/stores/useGameStore';
import { ConnectionStatus } from '@/types/Connection';

const UserNameInput = () => {
  const params = useParams();
  const roomId = params.room as string;
  const [username, setUsername] = useState('');

  const actions = useGameStore((state) => state.actions);
  const [status] = useGameStore((state) => [state.status]);

  useEffect(() => {
    if (username && roomId && status == ConnectionStatus.IN_LOBBY) {
      redirect(`/room/lobby/${roomId}`, RedirectType.replace);
    }
  }, [username, roomId, status]);

  return (
    <div className="flex w-full gap-x-2">
      <input
        type="text"
        className={`input input-bordered h-auto flex-1`}
        placeholder="ENTER USERNAME"
        onChange={(e) => {
          setUsername(e.target.value);
        }}
        required={true}
      />
      <button
        className={`text-md btn btn-neutral h-fit flex-none py-2 ${username.length == 0 ? 'btn-disabled' : ''}`}
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
