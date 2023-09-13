"use client";

import Link from "next/link";
import { useState } from "react";

export default function Home() {
  const [roomCode, setRoomCode] = useState("");

  return (
    <main className="h-screen w-screen bg-base-100">
      <div className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/2 flex-col gap-2">
        <h1 className="text-center text-4xl font-semibold text-neutral-content">
          VotaFun
        </h1>
        <p className="mx-auto w-2/3 text-center text-xl font-light text-neutral-content">
          Elevate your Singaporean outings with VotaFun, where decision-making
          transforms into thrilling quiz-style adventures!
        </p>
        <div className="mx-auto mt-4 flex w-2/3 flex-col gap-2">
          <Link
            className="btn btn-neutral h-fit w-full py-4 text-lg"
            href={"/room/create"}
          >
            Create Room
          </Link>
          <div className="flex w-full gap-x-2">
            <input
              type="text"
              className="input input-bordered h-auto flex-1 uppercase"
              placeholder="Enter Room Code"
              onChange={(e) => setRoomCode(e.target.value)}
            />
            <Link
              className="btn btn-neutral h-fit flex-none py-4 text-lg"
              href={`/room/join/${roomCode}`}
            >
              Join Room
            </Link>
          </div>
        </div>
      </div>
    </main>
  );