'use client';

import { LoadingDots } from '@/components/common/LoadingDots';

interface LabelProps {
  label: string;
  text: string;
}
const Label = ({ label, text }: LabelProps) => {
  if (text === '' || text === undefined) {
    text = 'thinking';
  }

  return (
    <div className="flex w-full gap-2 text-2xl font-semibold">
      <label className="w-36 flex-none uppercase leading-loose">{label}: </label>
      <div className="flex-1 rounded-md bg-accent py-2 text-center font-light leading-normal text-accent-content">
        {text} {text === 'thinking' && <LoadingDots />}
      </div>
    </div>
  );
};

export { Label };
