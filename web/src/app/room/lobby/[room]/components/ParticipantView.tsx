import { Label } from './Label';
import useGameStore from '@/stores/useGameStore';

const ParticipantView = () => {
  const room = useGameStore((state) => state.room);

  return (
    <>
      <Label label="Location" text={room.room_location || ''} />
      <Label label="Activity" text={room.room_activity || ''} />
    </>
  );
};

export { ParticipantView };
