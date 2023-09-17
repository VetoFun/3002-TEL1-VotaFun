'use client';

import { useParams, useSearchParams } from 'next/navigation';
import { useRoomStore } from '@/stores/useRoomStore';
import { HostView } from './components/HostView';
import { ParticipantView } from './components/ParticipantView';
import { RoomLayout } from '@/components/layout/RoomLayout';

export default function RoomLobbyPage() {
  const params = useParams();
  const query = useSearchParams();

  const isRoomHost = useRoomStore((state) => state.isHost) || query.get('host') === 'true'; // [todo: remove (debugging purposes)]

  return (
    <RoomLayout>
        <main className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
          <p className="mb-6 text-center text-2xl font-semibold uppercase">Room ID: {params.room}</p>
          {isRoomHost ? <HostView /> : <ParticipantView />}
        </main>
    </RoomLayout>
  );
}
