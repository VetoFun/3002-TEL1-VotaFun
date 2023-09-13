'use client'
import { Loader } from '@/components/common/Loader';
import { useRoomStore } from '@/stores/useRoomStore';

interface RoomLobbyPageProps {
  params: {
    room: string;
  };
}

export default function RoomLobbyPage({ params }: RoomLobbyPageProps) {

  const [roomId, userName] = useRoomStore((state) => [state.roomId, state.userName]);
  
  return (
    <main className="h-screen w-screen bg-base-100">
      <div className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <div className="mx-auto">
          <Loader />
        </div>
        <p className="text-center text-2xl font-semibold uppercase">Room ID: {roomId}</p>
        <p className="text-center text-2xl font-semibold uppercase">Username: {userName}</p>
        <p className="text-center text-xl font-light">
          [todo] implement lobby
        </p>
      </div>
    </main>
  );
}
