import { useRoomStore } from '@/stores/useRoomStore';
import { Select } from './Select';
import Link from 'next/link';
import useGameStore from '@/stores/useGameStore';

const HostView = () => {
  const locations = ['Central', 'East', 'North', 'North-East', 'West'];
  const activities = ['Food', 'Games', 'Leisure'];

  const roomId = useGameStore((state) => state.roomId);
  const [setLocation] = useRoomStore((state) => [state.setLocation]);
  const [setActivity] = useRoomStore((state) => [state.setActivity]);

  return (
    <div className="flex flex-col gap-2">
      <Select label="Select Location" options={locations} onChange={(e) => setLocation(e.target.value)} />
      <Select label="Select Activity" options={activities} onChange={(e) => setActivity(e.target.value)} />
      <Link className="btn btn-secondary text-lg" href={`/room/session/${roomId}`}>
        Start Room
      </Link>
    </div>
  );
};

export { HostView };
