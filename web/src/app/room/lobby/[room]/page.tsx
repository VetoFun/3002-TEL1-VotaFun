'use client';

import { HostView } from './components/HostView';
import { ParticipantView } from './components/ParticipantView';
import { RoomLayout } from '@/components/layout/RoomLayout';
import useGameStore from '@/stores/useGameStore';

export default function RoomLobbyPage() {
  const [user, room] = useGameStore((state) => [state.user, state.room]);

  if (!room.room_id) {
    throw new Error('You are not in a room!');
  }

  const copyToClipboard = () => {
    const domain = window.location.origin;
    const url = `${domain}/room/join/${room.room_id}`;
    navigator.clipboard.writeText(url);
  };

  const host = user.user_id == room.host_id;

  return (
    <RoomLayout>
      <main className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <p className="mb-6 text-center text-2xl font-semibold uppercase">
          Room ID:{' '}
          <code
            className="tooltip ml-2 rounded-md bg-accent p-3 px-4 hover:cursor-pointer"
            data-tip="Copy to Clipboard"
            onClick={copyToClipboard}
          >
            {room.room_id}
          </code>
        </p>
        {host ? <HostView /> : <ParticipantView />}
      </main>
    </RoomLayout>
  );
}
