import { Select } from './Select';
import useGameStore from '@/stores/useGameStore';
import { useEffect, useState } from 'react';

const HostView = () => {
  const locations = ['Central', 'East', 'North', 'North-East', 'West'];
  const activities = ['Food', 'Fun', 'Leisure'];

  const [room, actions] = useGameStore((state) =>[ state.room, state.actions]);
  const [location, setLocation] = useState('');
  const [activity, setActivity] = useState('');
  const [maxUsers, setMaxUsers] = useState(10);

  useEffect(() => {
    actions.sendRoomProperties(room.room_id, location, activity, maxUsers);
  }, [location, activity, actions, room.room_id, maxUsers]);

  return (
    <div className="flex flex-col gap-2">
      <Select label="Select Location" options={locations} onChange={(e) => setLocation(e.target.value)} />
      <Select label="Select Activity" options={activities} onChange={(e) => setActivity(e.target.value)} />
      <div className='w-full flex align-middle items-center gap-4'>
      <label>Max Users: </label>
      <input type='number' className="input input-lg input-bordered flex-1 py-3 text-xl tracking-widest" placeholder="Max Users" onChange={(e) => setMaxUsers(parseInt(e.target.value))} value={room.max_capacity}/>
      </div>
      <button type="button" className="btn btn-secondary text-lg" onClick={actions.startRoom}>
        Start Room
      </button>
    </div>
  );
};

export { HostView };
