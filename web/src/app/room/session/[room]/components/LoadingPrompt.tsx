import { LoadingDots } from "@/components/common/LoadingDots";

const LoadingPrompt = () => {
  return (
    <div className="chat chat-start">
      <div className="chat-bubble mx-auto w-full px-8 pr-10 py-6 text-2xl"><LoadingDots /></div>
    </div>
  );
};

export { LoadingPrompt };
