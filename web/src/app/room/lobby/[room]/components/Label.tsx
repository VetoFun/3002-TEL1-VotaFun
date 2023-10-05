'use client';

import styles from '../styles/dots.module.css';

interface LabelProps {
  label: string;
  text: string;
}

const AnimatedDots = () => {
  return (
    <div className="inline-flex gap-1">
      <div className={`h-1 w-1 animate-bounce rounded-full bg-accent-content ${styles['dot-1']}`}></div>
      <div className={`h-1 w-1 animate-bounce rounded-full bg-accent-content ${styles['dot-2']}`}></div>
      <div className={`h-1 w-1 animate-bounce rounded-full bg-accent-content ${styles['dot-3']}`}></div>
    </div>
  );
};

const Label = ({ label, text }: LabelProps) => {
  if (text === '' || text === undefined) {
    text = 'thinking';
  }

  return (
    <div className="flex w-[600px] gap-2 text-2xl font-semibold">
      <label className="w-36 flex-none uppercase leading-loose">{label}: </label>
      <div className="flex-1 rounded-md bg-accent py-2 text-center font-light leading-normal text-accent-content">
        {text} {text === 'thinking' && <AnimatedDots />}
      </div>
    </div>
  );
};

export { Label };
