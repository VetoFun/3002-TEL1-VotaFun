import { useRoomStore } from '@/stores/useRoomStore';
import { Select } from './Select';

const HostView = () => {
  const locations = ['Central', 'East', 'North', 'North-East', 'West'];
  const activities = ['Food', 'Games', 'Leisure'];

  const [setActivity, setLocation] = useRoomStore((state) => [state.setActivity, state.setLocation]);

  return (
    <div className="flex flex-col gap-2">
      <Select label="Select Location" options={locations} onChange={(e) => setLocation(e.target.value)} />
      <Select label="Select Activity" options={activities} onChange={(e) => setActivity(e.target.value)} />
      <button className="btn btn-neutral text-lg">Start Room</button>
    </div>
  );
};

export { HostView };
