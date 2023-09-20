import { useRoomStore } from '@/stores/useRoomStore';
import { Select } from './Select';
import { useEffect, useState } from 'react';
import Link from 'next/link';

const HostView = () => {
  const locations = ['Central', 'East', 'North', 'North-East', 'West'];
  const activities = ['Food', 'Games', 'Leisure'];

  const [location, setLocation] = useState('');
  const [activity, setActivity] = useState('');

  const [setRoom] = useRoomStore((state) => [state.setRoom]);

  useEffect(() => {
    const room = useRoomStore.getState().room!;
    room.activity = activity;
    room.location = location;
    setRoom(room);
  }, [location, activity, setRoom]);

  return (
    <div className="flex flex-col gap-2">
      <Select label="Select Location" options={locations} onChange={(e) => setLocation(e.target.value)} />
      <Select label="Select Activity" options={activities} onChange={(e) => setActivity(e.target.value)} />
      <Link className="btn btn-neutral text-lg" href={`/room/session/${useRoomStore.getState().room!.id}`}>
        Start Room
      </Link>
    </div>
  );
};

export { HostView };
