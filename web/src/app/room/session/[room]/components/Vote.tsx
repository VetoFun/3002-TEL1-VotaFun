interface VoteButtonProps {
  id: string;
  text: string;
  color: string;
}

function Vote({ id, text, color }: VoteButtonProps) {
  return (
    <button className={`btn ${color} h-24 max-w-md py-4 text-lg`} value={id}>
      {text}
    </button>
  );
}

export { Vote };
