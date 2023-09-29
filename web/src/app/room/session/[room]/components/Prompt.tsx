interface PromptProps {
  text: string;
}

const Prompt = ({ text }: PromptProps) => {
  return <div className="w-full rounded-lg p-8 px-12 text-center text-3xl font-light text-neutral-focus">{text}</div>;
};

export { Prompt };
