import useGameStore from '@/stores/useGameStore';
import { FaBan, FaCrown } from 'react-icons/fa';

interface ParticipantProps {
  initial: string;
  name: string;
  host?: boolean;
}

function Participant({ initial, name }: ParticipantProps) {
  const [user, room] = useGameStore((state) => [state.user, state.room]);

  const host = user.user_id == room.host_id;

  return (
    <div className="group flex w-full gap-2 px-4 py-2 align-middle transition-colors hover:bg-accent group-hover:text-neutral">
      {host && (
        <span className="my-auto text-2xl group-hover:text-warning">
          <FaCrown />
        </span>
      )}
      <div className="avatar placeholder">
        <div className="w-10 rounded-full bg-base-100 text-neutral">
          <span className="inline text-base">{initial}</span>
        </div>
      </div>
      <div className="flex flex-1 justify-between">
        <p className="my-auto group-hover:text-neutral-content">{name}</p>
        {host && (
          <div className="tooltip tooltip-error tooltip-left flex flex-col justify-center" data-tip="Kick User">
            <button className="btn btn-circle btn-error btn-xs">
              <FaBan />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export { Participant };
