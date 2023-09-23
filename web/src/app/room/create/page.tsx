'use client'

import { Loader } from '@/components/common/Loader';
import { useRoomStore } from '@/stores/useRoomStore';
import { createRoom } from './hooks/createRoom';
import { useEffect } from 'react';
import { redirect } from 'next/navigation';

export default function CreateRoomPage() {

  const [room, setRoom] = useRoomStore((state) => [state.room, state.setRoom]);
  setRoom(createRoom());

  useEffect(() => {
    redirect(`/room/join/${room?.id}`)
  }, [room])
  
  return (
    <main className="h-screen w-screen bg-base-100">
      <div className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <div className="mx-auto">
          <Loader />
        </div>
      </div>
    </main>
  );
}
