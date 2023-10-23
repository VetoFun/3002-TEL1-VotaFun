import useGameStore from '@/stores/useGameStore';
import { CreateTypes } from 'canvas-confetti';
import Link from 'next/link';
import { CSSProperties, useEffect } from 'react';
import ReactCanvasConfetti from 'react-canvas-confetti';

const ResultLayout = () => {
  const [option] = useGameStore((state) => [state.option]);
  let confetti: CreateTypes | null = null;

  const getInstance = (instance: CreateTypes | null) => {
    // saving the instance to an internal property
    confetti = instance;
  };

  const style: CSSProperties = {
    position: 'fixed',
    width: '100%',
    height: '100%',
    zIndex: -1,
  };

  useEffect(() => {
    if (confetti) {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
      });
    }
  });

  setInterval(() => {
    if (!confetti) return;

    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
    });
  }, 800);

  return (
    <>
      <ReactCanvasConfetti refConfetti={getInstance} style={style} fire={true} zIndex={100} />
      <div className="flex flex-col items-center justify-center gap-4">
        <p className="select-none rounded-lg bg-primary p-6 px-8 text-xl text-base-100 transition-all hover:scale-110">
          {option?.option_text}
        </p>
        <Link href="/">
          <button className="btn btn-secondary btn-md">Leave Room</button>
        </Link>
      </div>
    </>
  );
};

export { ResultLayout };
