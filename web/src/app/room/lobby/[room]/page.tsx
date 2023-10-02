'use client';

import { HostView } from './components/HostView';
import { ParticipantView } from './components/ParticipantView';
import { RoomLayout } from '@/components/layout/RoomLayout';
import { useParams } from 'next/navigation';
import useGameStore from '@/stores/useGameStore';
import { useRoomStore } from '@/stores/useRoomStore';

export default function RoomLobbyPage() {
  const params = useParams();
  const users = useRoomStore((state) => state.users);
  const userId = useGameStore((state) => state.userId);

  console.log('page:' + users);

  const isRoomHost = users.find((user) => user.user_id === userId)?.is_host;

  return (
    <RoomLayout>
      <main className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <p className="mb-6 text-center text-2xl font-semibold uppercase">Room ID: {params.room}</p>
        {isRoomHost ? <HostView /> : <ParticipantView />}
      </main>
    </RoomLayout>
  );
}
