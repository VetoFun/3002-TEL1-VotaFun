import { useRoomStore } from '@/stores/useRoomStore';
import { Label } from './Label';

const ParticipantView = () => {
  const room = useRoomStore((state) => state.room);

  return (
    <>
      <Label label="Location" text={room?.location || ''} />
      <Label label="Activity" text={room?.activity || ''} />
    </>
  );
};

export { ParticipantView };
