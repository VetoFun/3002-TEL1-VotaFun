'use client'
import { Loader } from '@/components/common/Loader';
import { UserNameInput } from '@/app/room/join/[room]/components/UserNameInput';

interface JoinRoomPageProps {
  params: {
    room: number;
  };
}

export default function JoinRoomPage({ params }: JoinRoomPageProps) {

  return (
    <main className="h-screen w-screen bg-base-100">
      <div className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <div className="mx-auto">
          <Loader />
        </div>
        <p className="text-center text-2xl font-semibold uppercase">Room ID: {params.room}</p>
        <UserNameInput />
      </div>
    </main>
  );
}
