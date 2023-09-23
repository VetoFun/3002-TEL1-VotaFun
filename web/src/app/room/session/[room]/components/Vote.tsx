interface VoteButtonProps {
  id: string;
  text: string;
}

function Vote({ id, text }: VoteButtonProps) {
  return (
    <button className="btn btn-neutral h-24 max-w-md py-4 text-lg" value={id}>
      {text}
    </button>
  );
}

export { Vote };
