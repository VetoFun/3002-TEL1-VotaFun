import { LoadingDots } from '@/components/common/LoadingDots';

const LoadingPrompt = () => {
  return (
    <div className="chat chat-start">
      <div className="chat-bubble mx-auto w-full px-8 py-6 pr-10 text-2xl">
        <LoadingDots />
      </div>
    </div>
  );
};

export { LoadingPrompt };
