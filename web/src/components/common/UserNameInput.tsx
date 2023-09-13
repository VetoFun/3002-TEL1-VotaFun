'use client';

import { useRoomStore } from '@/stores/useRoomStore';
import Link from 'next/link';

const UserNameInput = () => {

  const [roomId, userName, setUserName] = useRoomStore((state) => [state.roomId, state.userName, state.setUserName]);

  console.log(userName)

  return (
    <div className="flex w-full gap-x-2">
      <input
        type="text"
        className={`input input-bordered h-auto flex-1 uppercase`}
        placeholder="Enter Username"
        onChange={(e) => {
          setUserName(e.target.value)
        }}
        required={true}
      />
      <Link
        className={`btn btn-neutral h-fit flex-none py-4 text-lg ${userName.length == 0 ? 'btn-disabled' : ''}`}
        data-tip="Room code cannot be empty"
        data-for="room-code-empty"
        href={`/room/lobby/${roomId}`}
      >
        Join ({userName})
      </Link>
    </div>
  );
};

export { UserNameInput };
