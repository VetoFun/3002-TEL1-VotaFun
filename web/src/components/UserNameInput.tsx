'use client';

import Link from 'next/link';
import { useState } from 'react';

const UserNameInput = () => {
  const [username, setUsername] = useState('');

  return (
    <div className="flex w-full gap-x-2">
      <input
        type="text"
        className={`input input-bordered h-auto flex-1 uppercase`}
        placeholder="Enter Username"
        onChange={(e) => setUsername(e.target.value)}
        required={true}
        value={username}
      />
      <Link
        className={`btn btn-neutral h-fit flex-none py-4 text-lg ${username.length == 0 ? 'btn-disabled' : ''}`}
        data-tip="Room code cannot be empty"
        data-for="room-code-empty"
        href={`/room/lobby/${username}`}
      >
        Join
      </Link>
    </div>
  );
};

export { UserNameInput };
