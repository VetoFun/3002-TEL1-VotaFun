interface PromptProps {
  text: string;
}

const Prompt = ({ text }: PromptProps) => {
  return (
    <div className="w-full rounded-lg bg-neutral-content p-8 px-12 text-center text-2xl font-light text-neutral-focus">
      {text}
    </div>
  );
};

export { Prompt };
