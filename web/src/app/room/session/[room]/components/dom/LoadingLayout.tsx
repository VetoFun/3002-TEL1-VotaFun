import { LoadingPrompt } from '../LoadingPrompt';

const LoadingLayout = () => {
  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <LoadingPrompt />
    </div>
  );
};

export { LoadingLayout };
