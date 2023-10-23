import { motion } from 'framer-motion';
import { Prompt } from '../Prompt';
import { Vote } from '../Vote';
import { useEffect, useState } from 'react';
import useGameStore from '@/stores/useGameStore';

const VotingLayout = () => {
  const question = useGameStore((state) => state.question);
  const [progress, setProgress] = useState(100);
  const [countdown, setCountdown] = useState(15);

  const initial_time = 15;
  
  setTimeout(() => {
    setCountdown(countdown - 0.1);
    if (countdown <= 0) clearTimeout(this);
  }, 100);

  useEffect(() => {
    const newProgress = (countdown / initial_time) * 100;
    setProgress(Math.round(newProgress));
  }, [countdown, initial_time]);


  const getVoteColor = (id: number) => {
    const selection = id % 4;

    switch(selection) {
        case 0:
            return "btn-primary";
        case 1:
            return "btn-info";
        case 2:
            return "btn-success";
        case 3:
            return "btn-warning";
    }

    return "btn-primary";
}
  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <Prompt text={question.question_text} />
      <div className="my-4 w-2/3">
        <progress className="progress progress-warning h-4 w-full" value={progress} max="100"></progress>
        <motion.div
          className="text-md relative -inset-1/2 -inset-y-[calc(50%+4px)] flex h-12 w-12 items-center justify-center rounded-full bg-warning px-8 text-center font-extrabold text-base-100"
          initial={{ left: `calc(100% - 24px)` }}
          animate={{ left: `calc(${progress}% - 24px)` }}
          transition={{ type: 'spring', stiffness: 98 }}
        >
          <span className="">{Math.round(countdown)}</span>
        </motion.div>
      </div>
      <div className="relative -inset-y-12 mx-auto grid w-2/3 grid-cols-2 grid-rows-2 gap-3">
        {question.options.map((option, index) =>
            <Vote
                key={index}
                id={option.option_id}
                color={getVoteColor(index)}
                text={option.option_text}
                disabled={progress <= 0 || question.voted}
                />
        )}
      </div>
    </div>
  );
};

export { VotingLayout };
