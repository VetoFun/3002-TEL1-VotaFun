'use client';

import { useDebugStore } from '@/stores/useDebugStore';
import { RoomLayout } from '@/components/layout/RoomLayout';
import { Prompt } from './components/Prompt';
import { useParams } from 'next/navigation';
import { Vote } from './components/Vote';
import { useState } from 'react';
import { motion } from 'framer-motion';

export default function RoomLobbyPage() {
  const params = useParams();
  const [admin, setAdmin] = useDebugStore((state) => [state.admin, state.setAdmin]);

  const [progress, setProgress] = useState(0);

  // Sample response from /chatgpt:
  //   {
  //     "num_of_options": 4,
  //     "options": {
  //         "1": " Water-based activity",
  //         "2": " Land-based activity",
  //         "3": " I'm not sure",
  //         "4": " None of the above"
  //     },
  //     "question": "Do you want to do a water-based activity or a land-based activity?",
  //     "question_id": "7df85f6853df0ab2e2f91b1bab93ecd0f77d7715",
  //     "success": true
  // }

  const percentageToSeconds = (percentage: number) => {
    return Math.round(percentage * 0.6);
  };

  return (
    <RoomLayout>
      <main className="relative left-1/2 top-1/2 h-screen -translate-x-1/2 -translate-y-1/2 flex-col gap-2 bg-base-100">
        <div className="flex h-full w-full flex-col items-center justify-center gap-2">
          <div className="flex flex-col items-center justify-center gap-4">
            <Prompt text="Do you want to do a water-based activity or a land-based activity?" />
            <div className="my-4 w-full">
              <progress className="progress progress-warning h-4 w-full" value={progress} max="100"></progress>
              <motion.div
                className="text-md relative -inset-1/2 -inset-y-[calc(50%+4px)] flex h-12 w-12 items-center justify-center rounded-full bg-base-300 px-8 text-center font-extrabold text-neutral-focus"
                animate={{ left: `calc(${progress}% - 24px)` }}
                transition={{ type: 'spring', stiffness: 98 }}
              >
                <span className="">{percentageToSeconds(progress)}</span>
              </motion.div>
            </div>
            <div className="relative -inset-y-12 mx-auto grid w-full grid-cols-2 grid-rows-2 gap-2">
              <Vote id="1" color="btn-primary" text="Water-based activity" />
              <Vote id="2" color="btn-secondary" text="Land-based activity" />
              <Vote id="3" color="btn-accent" text="I'm not sure" />
              <Vote id="4" color="btn-error" text="None of the above" />
            </div>
          </div>
        </div>
      </main>
      {/* debugging */}
      <div className="absolute bottom-1 left-1 flex h-16 flex-col gap-4">
        <input
          type="checkbox"
          onChange={() => setAdmin(!admin)}
          className="toggle toggle-success absolute bottom-1 left-1"
        />
        <input
          type="range"
          min="0"
          max="100"
          value={progress}
          className="range"
          onChange={(e) => {
            setProgress(parseFloat(e.target.value));
          }}
        />
      </div>
    </RoomLayout>
  );
}
