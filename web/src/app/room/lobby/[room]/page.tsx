'use client';

import { useDebugStore } from '@/stores/useDebugStore';
import { HostView } from './components/HostView';
import { ParticipantView } from './components/ParticipantView';
import { RoomLayout } from '@/components/layout/RoomLayout';
import { useParams } from 'next/navigation';

export default function RoomLobbyPage() {
  const params = useParams();
  const [admin, setAdmin] = useDebugStore((state) => [state.admin, state.setAdmin]);

  return (
    <RoomLayout>
      <main className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <p className="mb-6 text-center text-2xl font-semibold uppercase">Room ID: {params.room}</p>
        {admin ? <HostView /> : <ParticipantView />}
      </main>
      {/* debugging */}
      <input
        type="checkbox"
        onChange={() => setAdmin(!admin)}
        className="toggle toggle-success absolute bottom-1 left-1"
      />
    </RoomLayout>
  );
}
