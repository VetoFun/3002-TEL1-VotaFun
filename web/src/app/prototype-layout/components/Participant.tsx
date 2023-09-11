interface ParticipantProps {
  initial: string;
  name: string;
}

function Participant({ initial, name }: ParticipantProps) {
  return (
    <div className="flex w-full gap-4 px-4 py-2 align-middle transition-colors hover:bg-base-content hover:text-neutral-focus">
      <div className="avatar placeholder">
        <div className="w-10 rounded-full bg-neutral-focus text-neutral-content">
          <span className="inline text-base">{initial}</span>
        </div>
      </div>
      <div className="flex grow">
        <p className="my-auto">{name}</p>
      </div>
    </div>
  );z
}

export { Participant };
