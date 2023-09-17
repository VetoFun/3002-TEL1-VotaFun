'use client';

import { useRoomStore } from '@/stores/useRoomStore';
import { useEffect, useState } from 'react';
import { createUser } from '../hooks/createUser';
import { redirect, useParams } from 'next/navigation';
import { joinRoom } from '../hooks/joinRoom';

const UserNameInput = () => {

  const params = useParams();
  const roomId = params.room as string;

  const [username, setUsername] = useState('');
  const [ready, setReady] = useState(false);

  const [setRoom, setUser] = useRoomStore((state) => [state.setRoom, state.setUser]);

  function onClickJoin() {
    if(!username) return;
    const user = createUser(username);
    const room = joinRoom(user, roomId);

    setUser(user);
    setRoom(room);
    setReady(true);
  }

  useEffect(() => {
    if(ready)
      redirect(`/room/lobby/${params.room}`);
 }, [params.room, ready]);

  return (
    <div className="flex w-full gap-x-2">
      <input
        type="text"
        className={`input input-bordered h-auto flex-1`}
        placeholder="Enter Username"
        onChange={(e) => {
          setUsername(e.target.value)
        }}
        required={true}
      />
      <button
        className={`btn btn-neutral h-fit flex-none py-4 text-lg ${username.length == 0 ? 'btn-disabled' : ''}`}
        data-tip="Room code cannot be empty"
        data-for="room-code-empty"
        onClick={() => onClickJoin()}
      >
        Join
      </button>
    </div>
  );
};

export { UserNameInput };
