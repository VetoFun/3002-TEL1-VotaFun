'use client';

import { useEffect } from 'react';
import { redirect } from 'next/navigation';
import useGameStore from '@/stores/useGameStore';

export default function CreateRoomPage() {
  const actions = useGameStore((state) => state.actions);
  const roomId = useGameStore((state) => state.roomId);

  actions.createRoom(); // implement

  useEffect(() => {
    actions.createRoom();
    if (roomId) redirect(`/room/join/${roomId}`);
    else redirect('/');
  }, [actions, roomId]);

  return (
    <main className="h-screen w-screen bg-base-100">
      <div className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <div className="mx-auto"></div>
      </div>
    </main>
  );
}
