'use client';

import { RoomLayout } from '@/components/layout/RoomLayout';
import { LoadingLayout } from './components/dom/LoadingLayout';
import { ConnectionStatus } from '@/types/Connection';
import { VotingLayout } from './components/dom/VotingLayout';
import useGameStore from '@/stores/useGameStore';

export default function RoomSessionPage() {

  const status = useGameStore((state) => state.status);

  const getLayout = () => {
    switch (status) {
      case ConnectionStatus.IN_GAME_WAITING_FOR_SERVER:
        return <LoadingLayout />;
      case ConnectionStatus.IN_GAME:
        return <VotingLayout />;
      default:
        return <LoadingLayout />;
    }
  }

  return (
    <RoomLayout>
      <main className="relative left-1/2 top-1/2 h-screen -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <div className="flex h-full w-full flex-col items-center justify-center gap-2">
          {getLayout()}
        </div>
      </main>
    </RoomLayout>
  );
}
