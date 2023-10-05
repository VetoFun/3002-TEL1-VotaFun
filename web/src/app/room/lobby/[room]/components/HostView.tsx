import { Select } from './Select';
import Link from 'next/link';
import useGameStore from '@/stores/useGameStore';
import { useEffect, useState } from 'react';

const HostView = () => {
  const locations = ['Central', 'East', 'North', 'North-East', 'West'];
  const activities = ['Food', 'Games', 'Leisure'];

  const room = useGameStore((state) => state.room);
  const [location, setLocation] = useState('');
  const [activity, setActivity] = useState('');

  useEffect(() => {
    room.room_location = location;
    room.room_activity = activity;
    useGameStore.setState({ room: room });
  }, [location, activity, room]);
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
