import { Loader } from '@/components/Loader';
import { UserNameInput } from '@/components/UserNameInput';

interface RoomLobbyPageProps {
  params: {
    room: string;
  };
}

export default function RoomLobbyPage({ params }: RoomLobbyPageProps) {
  return (
    <main className="h-screen w-screen bg-base-100">
      <div className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <div className="mx-auto">
          <Loader />
        </div>
        <p className="text-center text-2xl font-semibold uppercase">Room ID: {params.room}</p>
        <p className="text-center text-xl font-light">
          [todo] route this page to <code className="inline-block rounded-md bg-neutral p-1 px-2">/lobby</code> or use
          this room as lobby
        </p>
        <UserNameInput />
      </div>
    </main>
  );
}
