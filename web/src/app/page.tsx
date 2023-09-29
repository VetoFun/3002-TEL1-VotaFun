import { JoinRoomInput } from '@/components/JoinRoomInput';
import Link from 'next/link';

export default function Home() {
  return (
    <main className="h-screen w-screen">
      <div className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <div className="hero rounded-lg p-8 px-12 text-base-100">
          <div className="hero-content text-center">
            <div className="max-w-md">
              <h1 className="text-6xl font-bold text-neutral">Vota Fun</h1>
            </div>
          </div>
        </div>
        <div className="mx-auto mt-4 flex w-[600px] flex-col gap-2 transition-all">
          <Link className="btn btn-primary h-fit w-full py-4 text-lg hover:scale-105" href={'/room/create'}>
            Create Room
          </Link>
          <JoinRoomInput />
        </div>
      </div>
    </main>
  );
}
