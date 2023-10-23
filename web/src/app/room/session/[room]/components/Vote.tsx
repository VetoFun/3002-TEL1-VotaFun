import useGameStore from "@/stores/useGameStore";

interface VoteButtonProps {
  id: string;
  text: string;
  color: string;
  disabled: boolean;
}

function Vote({ id, text, color, disabled }: VoteButtonProps) {

  const actions = useGameStore((state) => state.actions);

  return (
    <button type='button' className={`btn ${color} h-24 max-w-md leading-relaxed text-md`} value={id} onClick={() => actions.vote(id)} disabled={disabled}>
      {text}
    </button>
  );
}

export { Vote };
