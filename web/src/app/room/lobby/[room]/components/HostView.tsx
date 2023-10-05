import { Select } from './Select';
import Link from 'next/link';
import useGameStore from '@/stores/useGameStore';
import { useEffect, useState } from 'react';

const HostView = () => {
  const locations = ['Central', 'East', 'North', 'North-East', 'West'];
  const activities = ['Food', 'Games', 'Leisure'];

  const room = useGameStore((state) => state.room);
  const actions = useGameStore((state) => state.actions);
  const [location, setLocation] = useState('');
  const [activity, setActivity] = useState('');

  useEffect(() => {
    actions.sendRoomProperties(room.room_id, location, activity);
  }, [location, activity, actions, room.room_id]);

  return (
    <div className="flex flex-col gap-2">
      <Select label="Select Location" options={locations} onChange={(e) => setLocation(e.target.value)} />
      <Select label="Select Activity" options={activities} onChange={(e) => setActivity(e.target.value)} />
      <Link className="btn btn-secondary text-lg" href={`/room/session/${room.room_id}`}>
        Start Room
      </Link>
    </div>
  );
};

export { HostView };
