import { JoinRoomInput } from '@/components/JoinRoomInput';
import Link from 'next/link';

export default function Home() {
  return (
    <main className="bg-scroll-animated h-screen w-screen bg-gradient-to-r from-purple-400 via-yellow-300 to-red-600">
      <div className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <div className="animate-bounce-slow hero rounded-lg bg-base-200 p-8 px-12">
          <div className="hero-content text-center">
            <div className="max-w-md">
              <h1 className="text-5xl font-bold">VotaFun</h1>
              <p className="py-6">
                Elevate your Singaporean outings with VotaFun, where decision-making transforms into thrilling
                quiz-style adventures!
              </p>
            </div>
          </div>
        </div>
        <div className="mx-auto mt-4 flex w-[600px] flex-col gap-2">
          <Link className="btn btn-neutral h-fit w-full py-4 text-lg" href={'/room/create'}>
            Create Room
          </Link>
          <JoinRoomInput />
        </div>
      </div>
    </main>
  );
}
