import { useRoomStore } from '@/stores/useRoomStore';
import { Label } from './Label';

const ParticipantView = () => {
  const [activity, location] = useRoomStore((state) => [state.activity, state.location]);

  return (
    <>
      <Label label="Location" text={location} />
      <Label label="Activity" text={activity} />
    </>
  );
};

export { ParticipantView };
