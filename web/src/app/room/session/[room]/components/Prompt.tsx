interface PromptProps {
  text: string;
}

const Prompt = ({ text }: PromptProps) => {
  return (
    <div className="chat chat-start">
      <div className="chat-bubble mx-auto w-full px-8 py-6 text-2xl">{text}</div>
    </div>
  );
};

export { Prompt };
